import asyncio
import csv
import logging
import os
import random
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageMediaContact

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency fallback
    load_dotenv = None


# =====================================================================
# CONFIGURATION
# =====================================================================
DEFAULT_BASE_DIR = Path(r"D:\ZALO_MOVE\userbot_scanner")
DEFAULT_RESULT_THRESHOLD = 50
DEFAULT_DELAY_MIN = 0.8
DEFAULT_DELAY_MAX = 2.0

# Candidate detector for Vietnamese phone-like sequences.
PHONE_CANDIDATE_RE = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){8,10}(?!\d)")

# Strict mobile prefixes plus a fallback generic VN number pattern.
VN_MOBILE_RE = re.compile(r"^0(?:3[2-9]|5[256789]|7[06789]|8[1-9]|9\d)\d{7}$")
VN_GENERIC_RE = re.compile(r"^0\d{9,10}$")


@dataclass
class ScanStats:
    total_candidates: int = 0
    valid_candidates: int = 0
    duplicates_removed: int = 0
    unique_valid: int = 0


def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _to_int(value: str, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _setup_env() -> None:
    env_path = Path(__file__).with_name(".env")
    if load_dotenv is not None:
        load_dotenv(dotenv_path=env_path, override=False)


_setup_env()

API_ID = _to_int(os.getenv("API_ID", ""), 0)
API_HASH = (os.getenv("API_HASH", "") or "").strip()
ADMIN_ID = _to_int(os.getenv("ADMIN_ID", ""), 0)

BASE_DIR = Path((os.getenv("BASE_DIR", "") or "").strip() or DEFAULT_BASE_DIR)
TEMP_DIR = BASE_DIR / "temp"
RESULTS_DIR = BASE_DIR / "results"
SESSIONS_DIR = BASE_DIR / "sessions"
LOGS_DIR = BASE_DIR / "logs"

RESULT_THRESHOLD = _to_int(os.getenv("RESULT_THRESHOLD", ""), DEFAULT_RESULT_THRESHOLD)
RANDOM_DELAY_MIN = _to_float(os.getenv("RANDOM_DELAY_MIN", ""), DEFAULT_DELAY_MIN)
RANDOM_DELAY_MAX = _to_float(os.getenv("RANDOM_DELAY_MAX", ""), DEFAULT_DELAY_MAX)
FLOOD_SLEEP_THRESHOLD = _to_int(os.getenv("FLOOD_SLEEP_THRESHOLD", ""), 60)


def ensure_directories() -> None:
    for path in (BASE_DIR, TEMP_DIR, RESULTS_DIR, SESSIONS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    ensure_directories()
    log_file = LOGS_DIR / "userbot_scanner.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def normalize_vn_phone(raw: str) -> str:
    digits = "".join(ch for ch in str(raw or "") if ch.isdigit())
    if not digits:
        return ""

    # Common variants for country prefix.
    if digits.startswith("0084"):
        digits = "0" + digits[4:]
    elif digits.startswith("84"):
        digits = "0" + digits[2:]

    return digits


def is_valid_vn_phone(phone: str) -> bool:
    p = normalize_vn_phone(phone)
    return bool(VN_MOBILE_RE.match(p) or VN_GENERIC_RE.match(p))


def extract_numbers_from_text(text: str) -> tuple[list[str], ScanStats]:
    stats = ScanStats()
    if not text:
        return [], stats

    matches = PHONE_CANDIDATE_RE.findall(text)
    stats.total_candidates = len(matches)

    seen: set[str] = set()
    output: list[str] = []
    duplicates = 0
    valid_count = 0

    for item in matches:
        normalized = normalize_vn_phone(item)
        if not is_valid_vn_phone(normalized):
            continue
        valid_count += 1
        if normalized in seen:
            duplicates += 1
            continue
        seen.add(normalized)
        output.append(normalized)

    stats.valid_candidates = valid_count
    stats.duplicates_removed = duplicates
    stats.unique_valid = len(output)
    return output, stats


def merge_stats(base: ScanStats, addon: ScanStats) -> None:
    base.total_candidates += addon.total_candidates
    base.valid_candidates += addon.valid_candidates
    base.duplicates_removed += addon.duplicates_removed
    # unique_valid is set at the end based on final set size.


def extract_numbers_from_vcf_text(vcf_text: str) -> tuple[list[str], ScanStats]:
    stats = ScanStats()
    if not vcf_text:
        return [], stats

    seen: set[str] = set()
    output: list[str] = []

    for line in vcf_text.splitlines():
        line = line.strip()
        if not line or not line.upper().startswith("TEL"):
            continue
        _, _, value = line.partition(":")
        if not value:
            continue
        nums, line_stats = extract_numbers_from_text(value)
        merge_stats(stats, line_stats)
        for n in nums:
            if n not in seen:
                seen.add(n)
                output.append(n)
            else:
                stats.duplicates_removed += 1

    stats.unique_valid = len(output)
    return output, stats


def _read_file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_numbers_from_file(path: Path) -> tuple[list[str], ScanStats]:
    suffix = path.suffix.lower()
    stats = ScanStats()
    seen: set[str] = set()
    output: list[str] = []

    if suffix == ".txt":
        for line in _read_file_text(path).splitlines():
            nums, line_stats = extract_numbers_from_text(line)
            merge_stats(stats, line_stats)
            for n in nums:
                if n not in seen:
                    seen.add(n)
                    output.append(n)
                else:
                    stats.duplicates_removed += 1

    elif suffix == ".csv":
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                row_text = " ".join(str(col or "") for col in row)
                nums, row_stats = extract_numbers_from_text(row_text)
                merge_stats(stats, row_stats)
                for n in nums:
                    if n not in seen:
                        seen.add(n)
                        output.append(n)
                    else:
                        stats.duplicates_removed += 1

    elif suffix == ".vcf":
        nums, vcf_stats = extract_numbers_from_vcf_text(_read_file_text(path))
        output.extend(nums)
        merge_stats(stats, vcf_stats)
    else:
        raise ValueError("File format not supported. Only .txt, .csv, .vcf are accepted.")

    stats.unique_valid = len(output)
    return output, stats


def format_summary(source_label: str, stats: ScanStats, numbers: list[str]) -> str:
    lines = [
        "=== KET QUA QUET SDT ===",
        f"Nguon: {source_label}",
        f"Tong chuoi phat hien: {stats.total_candidates}",
        f"So hop le: {stats.valid_candidates}",
        f"So trung da loai: {stats.duplicates_removed}",
        f"So duy nhat tra ve: {len(numbers)}",
    ]
    return "\n".join(lines)


def render_numbers_preview(numbers: list[str], limit: int = 50) -> str:
    if not numbers:
        return "Khong tim thay so dien thoai hop le."
    preview = numbers[:limit]
    lines = [f"- {n}" for n in preview]
    if len(numbers) > limit:
        lines.append(f"... va {len(numbers) - limit} so khac.")
    return "\n".join(lines)


def write_result_file(numbers: Iterable[str], source_name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", source_name or "scan")
    out_path = RESULTS_DIR / f"result_{safe_name}_{timestamp}.txt"
    out_path.write_text("\n".join(numbers), encoding="utf-8")
    return out_path


def is_scan_command(text: str) -> bool:
    t = (text or "").strip().lower()
    return t.startswith("/scan")


async def random_delay() -> None:
    low = min(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
    high = max(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
    await asyncio.sleep(random.uniform(low, high))


def cleanup_file(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except Exception as exc:
        logging.warning("Khong the xoa file tam %s: %s", path, exc)


ensure_directories()
setup_logging()

async def handle_new_message(event: events.NewMessage.Event) -> None:
    sender_id = int(event.sender_id or 0)
    if sender_id != ADMIN_ID:
        return

    # C) Shared / forwarded contact
    if event.media and isinstance(event.media, MessageMediaContact):
        await random_delay()
        media = event.media
        raw_phone = str(getattr(media, "phone_number", "") or "")
        phone = normalize_vn_phone(raw_phone)
        first_name = str(getattr(media, "first_name", "") or "").strip()
        last_name = str(getattr(media, "last_name", "") or "").strip()

        if phone and is_valid_vn_phone(phone):
            await event.reply(
                "Da nhan danh ba.\n"
                f"Ten: {(first_name + ' ' + last_name).strip() or '(khong ro)'}\n"
                f"SDT: {phone}"
            )
        else:
            await event.reply("Da nhan danh ba nhung SDT khong hop le theo dinh dang VN.")
        return

    raw_text = (event.raw_text or "").strip()

    # A) Direct text scan (no command required).
    if raw_text and not raw_text.startswith("/"):
        await random_delay()
        numbers, stats = extract_numbers_from_text(raw_text)
        summary = format_summary("text", stats, numbers)
        preview = render_numbers_preview(numbers)

        if len(numbers) > RESULT_THRESHOLD:
            result_file = write_result_file(numbers, "text")
            await event.client.send_file(
                event.chat_id,
                result_file,
                caption=f"{summary}\n\nDanh sach dai, gui file ket qua dinh kem.",
                reply_to=event.id,
            )
        else:
            await event.reply(f"{summary}\n\n{preview}")
        return

    # B) File scan requires /scan either in the same message or reply command.
    command_in_this_msg = is_scan_command(raw_text)
    reply_msg = await event.get_reply_message() if command_in_this_msg else None
    file_message = None

    if command_in_this_msg and event.message and event.message.file:
        file_message = event.message
    elif command_in_this_msg and reply_msg and getattr(reply_msg, "file", None):
        file_message = reply_msg

    if not file_message:
        return

    file_name = str(getattr(file_message.file, "name", "") or "upload.bin")
    suffix = Path(file_name).suffix.lower()
    if suffix not in {".txt", ".csv", ".vcf"}:
        await event.reply("Chi ho tro quet file .txt, .csv, .vcf voi lenh /scan.")
        return

    downloading_msg = await event.reply("Dang tai file va quet du lieu, vui long doi...")
    temp_path = TEMP_DIR / f"tmp_{random.randint(1000, 9999)}_{Path(file_name).name}"

    try:
        await event.client.download_media(file_message, file=str(temp_path))
        await random_delay()
        numbers, stats = extract_numbers_from_file(temp_path)
        summary = format_summary(f"file:{file_name}", stats, numbers)
        preview = render_numbers_preview(numbers)

        if len(numbers) > RESULT_THRESHOLD:
            result_file = write_result_file(numbers, Path(file_name).stem)
            await event.client.send_file(
                event.chat_id,
                result_file,
                caption=f"{summary}\n\nDanh sach dai, gui file ket qua dinh kem.",
                reply_to=event.id,
            )
        else:
            await event.reply(f"{summary}\n\n{preview}")

    except errors.FloodWaitError as flood:
        logging.warning("FloodWaitError: wait %s seconds", flood.seconds)
        await asyncio.sleep(int(flood.seconds))
        await event.reply(f"Telegram gioi han tan suat. Da tu dong cho {flood.seconds} giay.")
    except Exception as exc:
        logging.exception("Loi khi xu ly file")
        await event.reply(f"Loi khi xu ly file: {exc}")
    finally:
        cleanup_file(temp_path)
        try:
            await event.client.delete_messages(event.chat_id, downloading_msg.id)
        except Exception:
            pass


def validate_required_config() -> None:
    missing = []
    if API_ID <= 0:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if ADMIN_ID <= 0:
        missing.append("ADMIN_ID")

    if missing:
        raise RuntimeError(
            "Thieu cau hinh bat buoc trong .env: " + ", ".join(missing)
        )


async def main() -> None:
    validate_required_config()
    session_path = str(SESSIONS_DIR / "userbot_session")
    client = TelegramClient(session_path, API_ID, API_HASH)
    client.flood_sleep_threshold = FLOOD_SLEEP_THRESHOLD
    client.add_event_handler(handle_new_message, events.NewMessage(incoming=True))

    logging.info("==========================================")
    logging.info("Khoi dong userbot_scanner")
    logging.info("BASE_DIR=%s", BASE_DIR)
    logging.info("ADMIN_ID=%s", ADMIN_ID)
    logging.info("==========================================")

    await client.start()
    me = await client.get_me()
    logging.info(
        "Dang nhap thanh cong: %s (@%s) id=%s",
        getattr(me, "first_name", "") or "(unknown)",
        getattr(me, "username", "") or "no_username",
        getattr(me, "id", 0),
    )
    logging.info("Dang lang nghe tin nhan tu ADMIN_ID=%s", ADMIN_ID)
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Dung chuong trinh theo yeu cau nguoi dung.")
    except Exception as fatal:
        logging.exception("Khoi dong that bai: %s", fatal)
        raise SystemExit(1)
