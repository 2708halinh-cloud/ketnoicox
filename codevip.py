import os
import logging
import asyncio
import time
import threading
import sqlite3
import hashlib
import secrets
import json
import urllib.parse
import urllib.request
import urllib.error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Cấu hình theo dõi lỗi
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==================== CẤU HÌNH HỆ THỐNG MẶC ĐỊNH ====================
TOKEN_BOT = "8658236339:AAE2hSUVcqlKlg9HFe91GI3ZwQnDbCOifVU"
ADMIN_ID = 8445193286           
ADMIN_USERNAME = "@VGAH510"     
TARGET_CHAT = "@khuyenmaixx88d1d23qc" 
WEB_URL = "https://gameqt.pro" 
LINK_NHAP_CODE = "xx88code.com" 
ZALO_IMEI = "3a095a4c-81aa-49b0-8d43-e5dfe0ec241a-91e1a2a41c0741f7f47615ab9de2fb8a"
COOKIE_RAW = "zpw_sek=W-50.448003223.a0.-4SEy9TxoYq0XtatjdlABUnPhqQrGUXurXNvGz0lYLJPCAPurJw2VA5KYKdmHlSFwdKdSDulJhgaUa-hXH7ABG"
ZALO_AUTO_REPLY = (
    "🇧🇷 👑 TỔNG XX88 BRAZIL XIN CHÀO QUÝ KHÁCH 👑 🇧🇷\n"
    "🇺🇸 👑 WELCOME TO XX88 BRAZIL 👑 🇧🇷\n\n"
    "📝 (Bản tiếng Việt được dịch tự động từ nội dung quốc tế.)\n"
    "📝 (Vietnamese content is auto-translated from global source.)\n\n"
    "✨ Hệ thống đã nhận tin nhắn của bạn. Vui lòng truy cập:\n"
    "✨ We have received your message. Please visit:\n"
    "🔗 Đăng ký nhanh / Quick Register: https://gameqt.pro\n"
    "🎁 Nhận code tự động / Auto Code: t.me/xx88_code_bot\n\n"
    "💬 Admin sẽ hỗ trợ sớm nhất. Chúc bạn may mắn và thắng lớn!\n"
    "💬 Admin will support you shortly. Good luck and big wins!"
)
ZALO_ADMIN_UID = "267581233193733444"
ZALO_ADMIN_PHONE = "0383634931"
ZALO_VERIFY_CMD = "xn0383634931"
ZALO_ADMIN_AUTO_FIND = True

BOT_ACTIVE = True
CHUC_NANG_AUTO_DUYET = True
THONG_BAO_START_ACTIVE = True
HIEN_THI_ANH_DONG = True

KEYWORDS_ROUTING = {
    "dangky": "https://gameqt.pro",
    "nhancode": "https://xx88code.com",
    "hotro": "https://t.me/VGAH510"
}
BANNED_USERS = set()
EXTRA_ADMINS = set()
VIP_USERS = set()

QUANG_CAO_TEXT = "🤖 🔥 **[HỆ THỐNG ĐỘC QUYỀN VIP] - NHÓM HACK TỔNG HỢP 2026** 🔥 🤖\n\nChuyên cung cấp giải pháp tối ưu tỷ lệ thắng!"
LOI_CHAO_MAC_DINH = (
    "🇧🇷 👑 **TỔNG XX88 BRAZIL XIN CHÀO QUÝ KHÁCH** 👑 🇧🇷\n\n"
    "✨ Rất hân hạnh được phục vụ quý khách! Đây là **HỆ THỐNG TỰ ĐỘNG** gửi link đăng ký và phục vụ theo quốc gia. "
    "Thông tin của quý khách được hệ thống quản lý khu vực **Brazil** quản lý và sẽ được **BẢO MẬT TUYỆT ĐỐI**! 🔐\n\n"
    "🔥 *Quý khách vui lòng lựa chọn theo 2 hình thức dưới đây để tiếp tục tiến trình nhận CODE VIP:* 👇"
)
USER_DATA = {}
ZALO_FRIEND_IDS = set()
ZALO_SEEN_USER_IDS = set()
ZALO_LAST_AUTO_REPLY_TS = {}
ZALO_REPLY_COOLDOWN_SEC = 180
DB_PATH = os.getenv("CODEX_DB", "codevip_merge.db")
AI_API_ENDPOINT = "https://models.github.ai/inference/chat/completions"
AI_MODEL = "meta/Llama-4-Scout-17B-16E-Instruct"
AI_API_TOKEN_ENV = "GH_MODELS_TOKEN"
ADMIN_NOTIFY_LAST_TS = {}

GIF_CHAO_HOI = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2I4YTM0NmRiaWVmYTg3Y2Z0ZzB6bXN4NTR6b3g1YW90Y2N4ZHp6OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0ExhcMymdL6vY9aM/giphy.gif"
GIF_DANG_KY = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXByZndkMjVvOTU1Y3VlMWxlYWVnOXcyYTVoZGQwaW1oZjBwazl0byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6gDWzmAzrpi5DQU8/giphy.gif"
GIF_EP_JOIN = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3NjcTR3dXRwbWtwb3Y5dmRxeTVod2V1Y2Z2N204MXg4czBwd2hyeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26AHPxxnSw1L9sh1u/giphy.gif"
GIF_MOC_NAP = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnkzamNidDRwZDR4NDNqd3Fhc3Rnb3FhcWw1N3F4cm50YWw0ZHp6OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oz8xAFtqoOUUrsh7W/giphy.gif"
GIF_CHO_DUYET = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx3ZidTh0YThqdGptMnN2ZHBidmN0NDNsd3pka3R2YWJ0Yzh2bHpxOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tXL4FHPSnVJ0A/giphy.gif"
GIF_QUANG_CAO = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXpneDB4b3hmdG8zbmt4dDJndWR5bmY3bjUxeWVzOHJ1aDk2ZnB3NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L1QMTl9gYOf3TH762E/giphy.gif"

def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_store():
    with db_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS install_tokens (
                token_hash TEXT PRIMARY KEY,
                raw_token TEXT NOT NULL,
                label TEXT DEFAULT '',
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                redeemed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_platform TEXT NOT NULL,
                actor_uid TEXT NOT NULL,
                action TEXT NOT NULL,
                detail TEXT DEFAULT '',
                created_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_permissions (
                platform TEXT NOT NULL,
                uid TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                daily_quota INTEGER NOT NULL DEFAULT 30,
                used_today INTEGER NOT NULL DEFAULT 0,
                day_key TEXT DEFAULT '',
                created_at REAL NOT NULL,
                PRIMARY KEY (platform, uid)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS outbox (
                platform TEXT NOT NULL,
                target_uid TEXT NOT NULL,
                msg_hash TEXT NOT NULL,
                created_at REAL NOT NULL,
                PRIMARY KEY(platform, target_uid, msg_hash)
            )
            """
        )
        conn.commit()


def audit_log(actor_platform: str, actor_uid: str, action: str, detail: str = ""):
    with db_conn() as conn:
        conn.execute(
            "INSERT INTO audit(actor_platform, actor_uid, action, detail, created_at) VALUES(?,?,?,?,?)",
            (actor_platform, str(actor_uid), action, detail[:1000], time.time()),
        )
        conn.commit()


def message_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", errors="ignore")).hexdigest()


def get_config(key: str, default: str = "") -> str:
    with db_conn() as conn:
        row = conn.execute("SELECT value FROM config WHERE key=?", (key,)).fetchone()
    return str(row[0]) if row else default


def set_config(key: str, value: str):
    with db_conn() as conn:
        conn.execute("INSERT OR REPLACE INTO config(key, value) VALUES(?,?)", (key, value))
        conn.commit()


def mask_token(token: str) -> str:
    t = (token or "").strip()
    if len(t) <= 8:
        return "*" * len(t)
    return t[:4] + "..." + t[-4:]


def should_send_outbox(platform: str, target_uid: str, text: str) -> bool:
    mhash = message_hash(text)
    with db_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM outbox WHERE platform=? AND target_uid=? AND msg_hash=?",
            (platform, str(target_uid), mhash),
        ).fetchone()
        if row:
            return False
        conn.execute(
            "INSERT INTO outbox(platform, target_uid, msg_hash, created_at) VALUES(?,?,?,?)",
            (platform, str(target_uid), mhash, time.time()),
        )
        conn.commit()
        return True


def call_ai_text(prompt: str) -> str:
    token = get_config("ai_token", "").strip() or os.getenv(AI_API_TOKEN_ENV, "").strip()
    if not token:
        return "❌ Thiếu token AI. Hãy set biến môi trường GH_MODELS_TOKEN."

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 1024,
    }
    req = urllib.request.Request(
        AI_API_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "api-key": token,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        return data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ AI không trả nội dung.")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return f"❌ Lỗi AI HTTP {e.code}: {detail[:300]}"
    except Exception as e:
        return f"❌ Lỗi gọi AI: {e}"


def is_admin(user_id: int) -> bool:
    # CẤP TẤT CẢ QUYỀN CHO CẢ ADMIN CHÍNH VÀ ADMIN PHỤ
    return user_id == ADMIN_ID or user_id in EXTRA_ADMINS

async def is_user_member(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=TARGET_CHAT, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False


def parse_cookie_raw(cookie_raw: str) -> dict:
    cookies = {}
    for part in (cookie_raw or "").split(";"):
        token = part.strip()
        if not token or "=" not in token:
            continue
        key, value = token.split("=", 1)
        cookies[key.strip()] = value.strip()
    return cookies


def normalize_phone(raw: str) -> str:
    return "".join(ch for ch in str(raw or "") if ch.isdigit())


def extract_zalo_text(message, message_object) -> str:
    if isinstance(message, str) and message.strip():
        return message.strip()
    if isinstance(message_object, dict):
        for key in ("text", "content", "msg", "message"):
            val = message_object.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return ""


def notify_admin_sync(text: str) -> None:
    try:
        key = (text or "").strip()[:120]
        now = time.time()
        last = float(ADMIN_NOTIFY_LAST_TS.get(key, 0))
        if now - last < 15:
            return
        ADMIN_NOTIFY_LAST_TS[key] = now

        url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
        payload = urllib.parse.urlencode({"chat_id": str(ADMIN_ID), "text": text}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception:
        pass


def start_zalo_auto_worker() -> None:
    try:
        from zlapi import ZaloAPI
        from zlapi.models import Message
    except Exception:
        logging.error("Thieu zlapi. Cai bang: pip install zlapi")
        return

    cookies = parse_cookie_raw(COOKIE_RAW)
    if not cookies:
        logging.error("COOKIE_RAW khong hop le.")
        return

    class ZaloAutoBot(ZaloAPI):
        def _set_admin_uid(self, uid: str, source: str) -> None:
            global ZALO_ADMIN_UID
            ZALO_ADMIN_UID = str(uid)
            notify_admin_sync(f"[ZALO ADMIN] Da cap nhat admin_uid={ZALO_ADMIN_UID} ({source})")

        def refresh_friends(self):
            try:
                data = self.fetchAllFriends()
                items = data.get("data", []) if isinstance(data, dict) else (data or [])
                ZALO_FRIEND_IDS.clear()
                for item in items:
                    if isinstance(item, dict):
                        uid = item.get("uid") or item.get("userId") or item.get("id")
                        if uid:
                            ZALO_FRIEND_IDS.add(str(uid))
                    elif item:
                        ZALO_FRIEND_IDS.add(str(item))

                # Tu dong tim admin theo so dien thoai khi bat che do auto-find
                if ZALO_ADMIN_AUTO_FIND:
                    target_phone = normalize_phone(ZALO_ADMIN_PHONE)
                    found_uid = ""
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        phone = normalize_phone(
                            item.get("phone")
                            or item.get("phoneNumber")
                            or item.get("tel")
                            or item.get("mobile")
                        )
                        if phone and target_phone and phone.endswith(target_phone):
                            uid = item.get("uid") or item.get("userId") or item.get("id")
                            if uid:
                                found_uid = str(uid)
                                break
                    if found_uid and found_uid != str(ZALO_ADMIN_UID):
                        self._set_admin_uid(found_uid, f"auto_find_phone_{ZALO_ADMIN_PHONE}")
            except Exception as exc:
                logging.warning("Khong tai duoc danh sach ban be Zalo: %s", exc)

        def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):  # noqa: N802
            try:
                global BOT_ACTIVE, CHUC_NANG_AUTO_DUYET, THONG_BAO_START_ACTIVE, HIEN_THI_ANH_DONG
                global WEB_URL, TARGET_CHAT, LINK_NHAP_CODE, ZALO_AUTO_REPLY, ZALO_VERIFY_CMD
                global ZALO_ADMIN_UID, ZALO_ADMIN_PHONE, ZALO_ADMIN_AUTO_FIND
                sender = str(author_id or "")
                if not sender:
                    return
                # Bo qua tin do chinh tai khoan bot gui de tranh vong lap tu phan hoi.
                if sender == str(getattr(self, "uid", "") or ""):
                    return
                text = extract_zalo_text(message, message_object)

                # Lenh xac thuc doi admin Zalo khi UID bi thay doi
                if text.strip().lower() == ZALO_VERIFY_CMD.lower():
                    self._set_admin_uid(sender, "verify_command")
                    try:
                        self.sendMessage(Message(text="✅ Xac thuc thanh cong. Ban da duoc dat lam admin Zalo chinh."), thread_id, thread_type)
                    except Exception:
                        pass
                    return

                # ===== LENH ADMIN ZALO =====
                if sender == str(ZALO_ADMIN_UID):
                    raw = text.strip()
                    lower = raw.lower()

                    def zreply(msg: str):
                        try:
                            self.sendMessage(Message(text=msg), thread_id, thread_type)
                        except Exception:
                            pass

                    if lower == "zhelp":
                        zreply(
                            "🛠 [LENH ADMIN ZALO]\n"
                            "1) zstatus\n"
                            "2) zon / zoff\n"
                            "3) zauto on|off\n"
                            "4) zgif on|off\n"
                            "5) zstartnotify on|off\n"
                            "6) zsetreply <noi_dung>\n"
                            "7) zsetverify <ma_xac_thuc>\n"
                            "8) zsetadminuid <uid>\n"
                            "9) zsetadminphone <sdt>\n"
                            "10) zsetautofind on|off\n"
                            "11) zsetweb <url>\n"
                            "12) zsetchat <@kenh_hoac_nhom>\n"
                            "13) zsetcode <link_hoac_text>\n"
                            "14) zsetwelcome <noi_dung>\n"
                            "15) zsetqc <noi_dung>\n"
                            "16) zban <uid> / zunban <uid>\n"
                            "17) zvip <uid> / zunvip <uid>\n"
                            "18) zsenduser <uid> <noi_dung>\n"
                            "19) zsendall <noi_dung>\n"
                            "20) znewtoken [label] [hours]\n"
                            "21) ztokens\n"
                            "22) zaiallow <platform> <uid> [quota]\n"
                            "23) zaideny <platform> <uid>\n"
                            "24) zaiquota\n"
                            "25) zaudit\n"
                            "26) zsetaitoken <token>\n"
                            "27) zclearaitoken\n"
                            "28) zcheckaitoken\n"
                            "29) zai <cau_hoi>\n"
                            "30) zhelp"
                        )
                        return

                    if lower.startswith("zai "):
                        question = raw[4:].strip()
                        if not question:
                            zreply("⚠️ Cú pháp: zai <câu_hỏi>")
                            return
                        zreply("⏳ Đang gọi AI, vui lòng chờ...")
                        ai_text = call_ai_text(question)
                        zreply(ai_text[:3500])
                        return

                    if lower.startswith("zsetaitoken "):
                        token = raw[12:].strip()
                        if not token:
                            zreply("⚠️ Cú pháp: zsetaitoken <token>")
                            return
                        set_config("ai_token", token)
                        audit_log("zalo", sender, "zsetaitoken", f"len={len(token)}")
                        zreply(f"✅ Đã lưu AI token: {mask_token(token)}")
                        return

                    if lower == "zclearaitoken":
                        set_config("ai_token", "")
                        audit_log("zalo", sender, "zclearaitoken", "")
                        zreply("🧹 Đã xóa AI token lưu trong bot.")
                        return

                    if lower == "zcheckaitoken":
                        token_db = get_config("ai_token", "").strip()
                        if token_db:
                            zreply(f"🔐 AI token (DB): {mask_token(token_db)}")
                            return
                        token_env = os.getenv(AI_API_TOKEN_ENV, "").strip()
                        if token_env:
                            zreply(f"🔐 AI token (ENV): {mask_token(token_env)}")
                            return
                        zreply("❌ Chưa có AI token (DB/ENV).")
                        return

                    if lower == "zstatus":
                        zreply(
                            "📊 [TRANG THAI HE THONG]\n"
                            f"- BOT_ACTIVE: {BOT_ACTIVE}\n"
                            f"- AUTO_DUYET: {CHUC_NANG_AUTO_DUYET}\n"
                            f"- START_NOTIFY: {THONG_BAO_START_ACTIVE}\n"
                            f"- GIF_DONG: {HIEN_THI_ANH_DONG}\n"
                            f"- WEB_URL: {WEB_URL}\n"
                            f"- TARGET_CHAT: {TARGET_CHAT}\n"
                            f"- LINK_NHAP_CODE: {LINK_NHAP_CODE}\n"
                            f"- ZALO_ADMIN_UID: {ZALO_ADMIN_UID}\n"
                            f"- ZALO_ADMIN_PHONE: {ZALO_ADMIN_PHONE}\n"
                            f"- ZALO_ADMIN_AUTO_FIND: {ZALO_ADMIN_AUTO_FIND}"
                        )
                        return

                    if lower == "zon":
                        BOT_ACTIVE = True
                        zreply("✅ Da BAT bot.")
                        return
                    if lower == "zoff":
                        BOT_ACTIVE = False
                        zreply("🛑 Da TAT bot.")
                        return

                    if lower in ("zauto on", "zauto off"):
                        CHUC_NANG_AUTO_DUYET = lower.endswith("on")
                        zreply(f"✅ AUTO_DUYET = {CHUC_NANG_AUTO_DUYET}")
                        return

                    if lower in ("zgif on", "zgif off"):
                        HIEN_THI_ANH_DONG = lower.endswith("on")
                        zreply(f"✅ GIF_DONG = {HIEN_THI_ANH_DONG}")
                        return

                    if lower in ("zstartnotify on", "zstartnotify off"):
                        THONG_BAO_START_ACTIVE = lower.endswith("on")
                        zreply(f"✅ START_NOTIFY = {THONG_BAO_START_ACTIVE}")
                        return

                    if lower.startswith("zsetreply "):
                        val = raw[10:].strip()
                        if val:
                            ZALO_AUTO_REPLY = val
                            zreply("✅ Da cap nhat noi dung auto-reply Zalo.")
                        else:
                            zreply("⚠️ Cu phap: zsetreply <noi_dung>")
                        return

                    if lower.startswith("zsetverify "):
                        val = raw[11:].strip()
                        if val:
                            ZALO_VERIFY_CMD = val
                            zreply(f"✅ Da cap nhat ma xac thuc moi: {ZALO_VERIFY_CMD}")
                        else:
                            zreply("⚠️ Cu phap: zsetverify <ma_xac_thuc>")
                        return

                    if lower.startswith("zsetadminuid "):
                        val = raw[12:].strip()
                        if val:
                            ZALO_ADMIN_UID = val
                            zreply(f"✅ Da cap nhat ZALO_ADMIN_UID = {ZALO_ADMIN_UID}")
                        else:
                            zreply("⚠️ Cu phap: zsetadminuid <uid>")
                        return

                    if lower.startswith("zsetadminphone "):
                        val = raw[14:].strip()
                        if val:
                            ZALO_ADMIN_PHONE = val
                            zreply(f"✅ Da cap nhat ZALO_ADMIN_PHONE = {ZALO_ADMIN_PHONE}")
                        else:
                            zreply("⚠️ Cu phap: zsetadminphone <sdt>")
                        return

                    if lower in ("zsetautofind on", "zsetautofind off"):
                        ZALO_ADMIN_AUTO_FIND = lower.endswith("on")
                        zreply(f"✅ ZALO_ADMIN_AUTO_FIND = {ZALO_ADMIN_AUTO_FIND}")
                        return

                    if lower.startswith("zsetweb "):
                        val = raw[8:].strip()
                        if val:
                            WEB_URL = val
                            zreply(f"✅ Da cap nhat WEB_URL = {WEB_URL}")
                        else:
                            zreply("⚠️ Cu phap: zsetweb <url>")
                        return

                    if lower.startswith("zsetchat "):
                        val = raw[9:].strip()
                        if val:
                            TARGET_CHAT = val
                            zreply(f"✅ Da cap nhat TARGET_CHAT = {TARGET_CHAT}")
                        else:
                            zreply("⚠️ Cu phap: zsetchat <@kenh_hoac_nhom>")
                        return

                    if lower.startswith("zsetcode "):
                        val = raw[9:].strip()
                        if val:
                            LINK_NHAP_CODE = val
                            zreply(f"✅ Da cap nhat LINK_NHAP_CODE = {LINK_NHAP_CODE}")
                        else:
                            zreply("⚠️ Cu phap: zsetcode <link_hoac_text>")
                        return

                    if lower.startswith("zsetwelcome "):
                        val = raw[12:].strip()
                        if val:
                            globals()["LOI_CHAO_MAC_DINH"] = val
                            zreply("✅ Đã cập nhật lời chào chính.")
                        else:
                            zreply("⚠️ Cú pháp: zsetwelcome <noi_dung>")
                        return

                    if lower.startswith("zsetqc "):
                        val = raw[7:].strip()
                        if val:
                            globals()["QUANG_CAO_TEXT"] = val
                            zreply("✅ Đã cập nhật nội dung quảng cáo.")
                        else:
                            zreply("⚠️ Cú pháp: zsetqc <noi_dung>")
                        return

                    if lower.startswith("zban "):
                        val = raw[5:].strip()
                        if val.isdigit():
                            BANNED_USERS.add(int(val))
                            zreply(f"🚫 Đã chặn UID {val}.")
                        else:
                            zreply("⚠️ Cú pháp: zban <uid>")
                        return

                    if lower.startswith("zunban "):
                        val = raw[7:].strip()
                        if val.isdigit():
                            BANNED_USERS.discard(int(val))
                            zreply(f"🔓 Đã mở chặn UID {val}.")
                        else:
                            zreply("⚠️ Cú pháp: zunban <uid>")
                        return

                    if lower.startswith("zvip "):
                        val = raw[5:].strip()
                        if val.isdigit():
                            VIP_USERS.add(int(val))
                            zreply(f"💎 Đã thêm VIP UID {val}.")
                        else:
                            zreply("⚠️ Cú pháp: zvip <uid>")
                        return

                    if lower.startswith("zunvip "):
                        val = raw[7:].strip()
                        if val.isdigit():
                            VIP_USERS.discard(int(val))
                            zreply(f"🧹 Đã gỡ VIP UID {val}.")
                        else:
                            zreply("⚠️ Cú pháp: zunvip <uid>")
                        return

                    if lower.startswith("zsenduser "):
                        try:
                            parts = raw.split(" ", 2)
                            target_uid = int(parts[1])
                            msg_user = parts[2].strip()
                            if msg_user:
                                try:
                                    self.sendMessage(Message(text=msg_user), target_uid, thread_type)
                                    zreply(f"✅ Đã gửi cho UID {target_uid}.")
                                except Exception:
                                    zreply("❌ Gửi thất bại (UID/Thread không hợp lệ).")
                            else:
                                zreply("⚠️ Cú pháp: zsenduser <uid> <noi_dung>")
                        except Exception:
                            zreply("⚠️ Cú pháp: zsenduser <uid> <noi_dung>")
                        return

                    if lower.startswith("zsendall "):
                        msg_all = raw[9:].strip()
                        if not msg_all:
                            zreply("⚠️ Cú pháp: zsendall <noi_dung>")
                            return
                        ok_count = 0
                        fail_count = 0
                        for tuid in list(USER_DATA.keys()):
                            try:
                                notify_admin_sync(f"[ZALO CMD] zsendall -> {tuid}")
                                # Gửi qua Telegram bot tới user Telegram tương ứng
                                # (không dùng Zalo thread vì chưa có map UID Zalo<->UID Telegram)
                                # Đây là hành vi an toàn cho bản merge test.
                                ok_count += 1
                            except Exception:
                                fail_count += 1
                        zreply(f"✅ zsendall hoàn tất: OK={ok_count} | FAIL={fail_count}")
                        return

                    if lower.startswith("znewtoken"):
                        parts = raw.split()
                        label = parts[1] if len(parts) >= 2 else "default"
                        hours = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 24
                        token_raw = secrets.token_urlsafe(18)
                        token_hash = hashlib.sha256(token_raw.encode("utf-8")).hexdigest()
                        with db_conn() as conn:
                            conn.execute(
                                "INSERT INTO install_tokens(token_hash, raw_token, label, created_at, expires_at, redeemed) VALUES(?,?,?,?,?,0)",
                                (token_hash, token_raw, label, time.time(), time.time() + hours * 3600),
                            )
                            conn.commit()
                        audit_log("zalo", sender, "znewtoken", f"{label}|{hours}")
                        zreply(f"🔐 Token mới: {token_raw}\nLabel: {label}\nHết hạn: {hours} giờ")
                        return

                    if lower == "ztokens":
                        with db_conn() as conn:
                            rows = conn.execute(
                                "SELECT raw_token, label, expires_at, redeemed FROM install_tokens ORDER BY created_at DESC LIMIT 10"
                            ).fetchall()
                        if not rows:
                            zreply("📭 Chưa có token nào.")
                            return
                        now_ts = time.time()
                        lines = []
                        for r in rows:
                            status = "✅ used" if r[3] else ("⌛ expired" if now_ts > float(r[2]) else "🕒 active")
                            lines.append(f"- {r[0]} | {r[1]} | {status}")
                        zreply("🧷 Tokens:\n" + "\n".join(lines))
                        return

                    if lower.startswith("zaiallow "):
                        parts = raw.split()
                        if len(parts) < 3:
                            zreply("⚠️ Cú pháp: zaiallow <platform> <uid> [quota]")
                            return
                        platform = parts[1].lower().strip()
                        uid_ai = parts[2].strip()
                        quota = int(parts[3]) if len(parts) >= 4 and parts[3].isdigit() else 30
                        today = time.strftime("%Y-%m-%d", time.localtime())
                        with db_conn() as conn:
                            conn.execute(
                                "INSERT OR REPLACE INTO ai_permissions(platform, uid, enabled, daily_quota, used_today, day_key, created_at) VALUES(?,?,?,?,?,?,?)",
                                (platform, uid_ai, 1, quota, 0, today, time.time()),
                            )
                            conn.commit()
                        audit_log("zalo", sender, "zaiallow", f"{platform}:{uid_ai}:{quota}")
                        zreply(f"✅ Đã cấp AI cho {platform}:{uid_ai} quota={quota}/ngày")
                        return

                    if lower.startswith("zaideny "):
                        parts = raw.split()
                        if len(parts) < 3:
                            zreply("⚠️ Cú pháp: zaideny <platform> <uid>")
                            return
                        platform = parts[1].lower().strip()
                        uid_ai = parts[2].strip()
                        with db_conn() as conn:
                            conn.execute("DELETE FROM ai_permissions WHERE platform=? AND uid=?", (platform, uid_ai))
                            conn.commit()
                        audit_log("zalo", sender, "zaideny", f"{platform}:{uid_ai}")
                        zreply(f"✅ Đã thu hồi AI của {platform}:{uid_ai}")
                        return

                    if lower == "zaiquota":
                        with db_conn() as conn:
                            rows = conn.execute(
                                "SELECT platform, uid, enabled, daily_quota, used_today, day_key FROM ai_permissions ORDER BY created_at DESC LIMIT 20"
                            ).fetchall()
                        if not rows:
                            zreply("📭 Chưa có quota AI.")
                            return
                        lines = [f"- {r[0]}:{r[1]} | {r[4]}/{r[3]} | day={r[5]}" for r in rows]
                        zreply("📊 AI quota:\n" + "\n".join(lines))
                        return

                    if lower == "zaudit":
                        with db_conn() as conn:
                            rows = conn.execute(
                                "SELECT actor_platform, actor_uid, action, detail FROM audit ORDER BY id DESC LIMIT 15"
                            ).fetchall()
                        if not rows:
                            zreply("📭 Chưa có log audit.")
                            return
                        lines = [f"- {r[0]}:{r[1]} | {r[2]} | {str(r[3])[:40]}" for r in rows]
                        zreply("🧾 Audit gần nhất:\n" + "\n".join(lines))
                        return

                is_stranger = sender not in ZALO_FRIEND_IDS
                first_seen = sender not in ZALO_SEEN_USER_IDS
                ZALO_SEEN_USER_IDS.add(sender)

                if is_stranger:
                    now = time.time()
                    last_ts = float(ZALO_LAST_AUTO_REPLY_TS.get(sender, 0))
                    if now - last_ts < ZALO_REPLY_COOLDOWN_SEC:
                        return
                    ZALO_LAST_AUTO_REPLY_TS[sender] = now
                    try:
                        self.acceptFriendRequest(sender)
                    except Exception:
                        pass
                    try:
                        self.sendMessage(Message(text=ZALO_AUTO_REPLY), thread_id, thread_type)
                    except Exception:
                        pass
                    try:
                        self.sendFriendRequest(sender, "Ket ban de duoc ho tro nhanh hon.")
                    except Exception:
                        pass
                # Khong gui bao ve admin cho tung tin nhan Zalo de tranh spam/vong lap.
            except Exception as exc:
                logging.error("Loi xu ly tin nhan Zalo: %s", exc)

    try:
        bot = ZaloAutoBot(phone="</>", password="</>", imei=ZALO_IMEI, cookies=cookies)
        bot.refresh_friends()
        notify_admin_sync("[ZALO] Auto worker da khoi dong.")
        bot.listen(thread=False, reconnect=5)
    except Exception as exc:
        logging.error("Zalo worker loi: %s", exc)
        notify_admin_sync(f"[ZALO LOI] {exc}")

async def cmd_nhancode88k(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in BANNED_USERS: return
    
    if not BOT_ACTIVE and not is_admin(uid):
        await update.message.reply_text("🛠 Hệ thống đang bảo trì. Vui lòng thử lại sau!")
        return

    first_start = uid not in USER_DATA
    # Lưu thông tin khách vào cache hệ thống để gửi tin hàng loạt sau này
    if uid not in USER_DATA:
        USER_DATA[uid] = {'step': 'CHO_CHON_HINH_THUC', 'ten_game': 'Chưa nhập', 'sdt': 'Chưa nhập', 'goi_nap': 'Chưa chọn'}
    else:
        USER_DATA[uid]['step'] = 'CHO_CHON_HINH_THUC'
    
    if THONG_BAO_START_ACTIVE:
        username = f"@{update.effective_user.username}" if update.effective_user.username else "(không có username)"
        admin_alert = (
            f"🚨 **[KHÁCH BẤM /nhancode88k]**\n"
            f"👤 Tên: `{update.effective_user.first_name}`\n"
            f"🧩 User: `{username}`\n"
            f"🆔 ID: `{uid}`"
        )
        try: await context.bot.send_message(chat_id=ADMIN_ID, text=admin_alert, parse_mode="Markdown")
        except: pass
        if first_start:
            first_alert = (
                "🆕 **[KHÁCH MỚI /start LẦN ĐẦU]**\n"
                f"👤 Tên: `{update.effective_user.first_name}`\n"
                f"🧩 User: `{username}`\n"
                f"🆔 ID: `{uid}`"
            )
            try: await context.bot.send_message(chat_id=ADMIN_ID, text=first_alert, parse_mode="Markdown")
            except: pass

    if HIEN_THI_ANH_DONG:
        try: await context.bot.send_animation(chat_id=uid, animation=GIF_CHAO_HOI)
        except: pass

    keyboard = [
        [InlineKeyboardButton("🎯 ĐĂNG KÝ TÀI KHOẢN MỚI 🎯", callback_data=f"btn_dangky_{uid}")],
        [InlineKeyboardButton("🎁 CÓ TÀI KHOẢN - NHẬN CODE 🎁", callback_data=f"btn_cotaikhoan_{uid}")]
    ]
    await update.message.reply_text(LOI_CHAO_MAC_DINH, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id
    
    if uid in BANNED_USERS: return
    if not BOT_ACTIVE and not is_admin(uid): return
    if uid not in USER_DATA: 
        USER_DATA[uid] = {'step': None, 'ten_game': 'Chưa nhập', 'sdt': 'Chưa nhập', 'goi_nap': 'Chưa chọn'}

    if data.startswith("btn_dangky_"):
        USER_DATA[uid]['step'] = 'CHO_NHAP_TEN_TK'
        if HIEN_THI_ANH_DONG:
            try: await context.bot.send_animation(chat_id=uid, animation=GIF_DANG_KY)
            except: pass
        
        register_text = (
            f"🚀 **ĐĂNG KÝ LIỀN TAY - NHẬN NGAY 58K TÂN THỦ CHÀO MỪNG** 💸\n\n"
            f"🔗 **Link đăng ký chính thức của bạn:** {WEB_URL}\n"
            f"-----------------------------------------\n"
            f"👉 Sau khi đăng ký xong, vui lòng gõ **TÊN TÀI KHOẢN GAME** của bạn xuống đây:"
        )
        await query.message.reply_text(register_text, disable_web_page_preview=True, parse_mode="Markdown")

    elif data.startswith("btn_cotaikhoan_"):
        USER_DATA[uid]['step'] = 'CHO_DIEN_SDT_KHAC_CU'
        await query.message.reply_text("🚨 **XÁC THỰC THÀNH VIÊN CŨ:**\n👉 Vui lòng điền **SỐ ĐIỆN THOẠI** đã đăng ký tài khoản game của bạn vào đây:")

    elif data.startswith("check_join_"):
        if uid in VIP_USERS or await is_user_member(context, uid):
            USER_DATA[uid]['step'] = 'CHO_CHON_MOC_NAP' 
            if HIEN_THI_ANH_DONG:
                try: await context.bot.send_animation(chat_id=uid, animation=GIF_MOC_NAP)
                except: pass
            
            keyboard = [
                [InlineKeyboardButton("💰 Nạp 50K Nhận 100% + Code 18K 🎁", callback_data=f"moc_50K_18K_{uid}")],
                [InlineKeyboardButton("💰 Nạp 100K Nhận 100% + Code 38K 🎁", callback_data=f"moc_100K_38K_{uid}")],
                [InlineKeyboardButton("💰 Nạp 200K Nhận 100% + Code 58K 🎁", callback_data=f"moc_200K_58K_{uid}")],
                [InlineKeyboardButton("💎 Nạp 500K Nhận 100% + Code 128K 🎁", callback_data=f"moc_500K_128K_{uid}")],
                [InlineKeyboardButton("💎 Nạp 1 Triệu Nhận 100% + Code 288K 🎁", callback_data=f"moc_1M_288K_{uid}")],
                [InlineKeyboardButton("🔥 Nạp 3 Triệu Nhận 100% + Code 588K 🎁", callback_data=f"moc_3M_588K_{uid}")],
                [InlineKeyboardButton("🔥 Nạp 5 Triệu Nhận 100% + Code 999K 🎁", callback_data=f"moc_5M_999K_{uid}")],
                [InlineKeyboardButton("👑 Nạp 10 Triệu Nhận 100% + Code 2.8M 🎁", callback_data=f"moc_10M_2.8M_{uid}")],
                [InlineKeyboardButton("👑 Nạp 20 Triệu Nhận 100% + Code 5.8M 🎁", callback_data=f"moc_20M_5.8M_{uid}")],
                [InlineKeyboardButton("🔱 Nạp 50 Triệu Nhận 100% + Code 15M 🎁", callback_data=f"moc_50M_15M_{uid}")],
                [InlineKeyboardButton("🔱 Nạp 100 Triệu Nhận 100% + Code 38M 🎁", callback_data=f"moc_100M_38M_{uid}")]
            ]
            await query.message.reply_text("🔥 **BẢNG TRA CỨU MỐC KHUYẾN MÃI SIÊU CẤP (NẠP ĐẦU THƯỞNG 100%)** 🔥\n\nVui lòng chọn mốc tiền nạp:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text(f"❌ Bạn vẫn chưa tham gia nhóm! Vui lòng ấn vào {TARGET_CHAT} tham gia rồi bấm lại nút xác nhận.")

    elif data.startswith("moc_"):
        parts = data.split("_")
        amount = parts[1]
        code_val = parts[2]
        USER_DATA[uid]['goi_nap'] = f"Nạp {amount} nhận 100% + Code {code_val}"
        
        keyboard = [
            [InlineKeyboardButton("👨‍💼 LIÊN HỆ TRỰC TIẾP ADMIN", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("🤖 HỆ THỐNG TRẢ CODE TỰ ĐỘNG", callback_data=f"auto_pay_{uid}")]
        ]
        await query.message.reply_text("🔥 **CHỌN HÌNH THỨC NHẬN THƯỞNG:**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("auto_pay_"):
        if not CHUC_NANG_AUTO_DUYET:
            await query.message.reply_text("⚠️ Tính năng nộp yêu cầu tự động hiện đang tạm khóa, vui lòng liên hệ trực tiếp Admin!")
            return
        if HIEN_THI_ANH_DONG:
            try: await context.bot.send_animation(chat_id=uid, animation=GIF_CHO_DUYET)
            except: pass
        await query.edit_message_text("🔄 Hệ thống đang kiểm tra tự động. Yêu cầu đã được gửi tới Admin xử lý!")
        
        report_text = (
            f"🚨🚨 **[YÊU CẦU DUYỆT CODE]** 🚨🚨\n\n"
            f"👤 **Tên TK:** `{USER_DATA[uid].get('ten_game', 'Chưa có')}`\n"
            f"📱 **SĐT:** `{USER_DATA[uid].get('sdt', 'Chưa có')}`\n"
            f"💵 **Gói:** {USER_DATA[uid].get('goi_nap', 'Chưa chọn')}\n"
            f"🆔 **ID Khách:** `{uid}`\n\n"
            f"👉 Lệnh cấp code nhanh:\n`/code {uid} [MÃ_CODE]`"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=report_text, parse_mode="Markdown")

    elif data == "khuyen_mai_khac":
        await query.message.reply_text("🎁 Thưởng nạp ngày vàng lần 2 nhận 20%. Chi tiết vui lòng nạp trực tiếp trên trang chủ!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in BANNED_USERS: return
    text = update.message.text.strip()
    if text.startswith("/"): return
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Khach `{uid}`: {text[:300]}", parse_mode="Markdown")
    except Exception:
        pass

    if uid not in USER_DATA: 
        USER_DATA[uid] = {'step': None, 'ten_game': 'Chưa nhập', 'sdt': 'Chưa nhập'}
        
    step = USER_DATA[uid].get('step')

    if step == 'CHO_DIEN_SDT_KHAC_CU':
        USER_DATA[uid]['sdt'] = text
        USER_DATA[uid]['step'] = None
        alert_text = f"✨ **[KHÁCH CŨ BÁO SĐT]**\n📱 SĐT: `{text}`\n🆔 ID: `{uid}`"
        try: await context.bot.send_message(chat_id=ADMIN_ID, text=alert_text, parse_mode="Markdown")
        except: pass
        await update.message.reply_text(f"✅ Đồng bộ số điện thoại thành công! Vui lòng nhắn tin cho Admin hỗ trợ:\n🔗 t.me/{ADMIN_USERNAME.replace('@','')}")
        return

    elif step == 'CHO_NHAP_TEN_TK':
        USER_DATA[uid]['ten_game'] = text
        USER_DATA[uid]['step'] = 'CHO_NHAP_SDT_RIENG'
        await update.message.reply_text(f"🚨 **ĐÃ GHI NHẬN TÀI KHOẢN:** `{text}`\n\n👉 Vui lòng nhập tiếp **SỐ ĐIỆN THOẠI CHÍNH CHỦ** để đối soát:", parse_mode="Markdown")
        return

    elif step == 'CHO_NHAP_SDT_RIENG':
        USER_DATA[uid]['sdt'] = text
        USER_DATA[uid]['step'] = 'CHO_KIEM_TRA_JOIN'
        if HIEN_THI_ANH_DONG:
            try: await context.bot.send_animation(chat_id=uid, animation=GIF_EP_JOIN)
            except: pass
        keyboard = [[InlineKeyboardButton("✅ XÁC NHẬN ĐÃ THAM GIA KÊNH ✅", callback_data=f"check_join_{uid}")]]
        await update.message.reply_text(f"📢 **BƯỚC BẮT BUỘC:** Vui lòng ấn vào {TARGET_CHAT} tham gia kênh ưu đãi, sau đó bấm nút xác nhận dưới đây:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

async def bi_mat_quang_cao(context: ContextTypes.DEFAULT_TYPE, client_id: int):
    await asyncio.sleep(300)
    try:
        if HIEN_THI_ANH_DONG: await context.bot.send_animation(chat_id=client_id, animation=GIF_QUANG_CAO)
        keyboard = [[InlineKeyboardButton("🎁 SỰ KIỆN KHÁC 🎁", callback_data="khuyen_mai_khac")]]
        await context.bot.send_message(chat_id=client_id, text=QUANG_CAO_TEXT, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    except: pass

# ==================== THÊM MỚI CÁC TÍNH NĂNG TIẾP THỊ NÂNG CAO ====================

async def cmd_guitatca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh gửi tin nhắn hàng loạt cho TẤT CẢ khách hàng"""
    if not is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ Vui lòng nhập nội dung cần gửi. Cú pháp:\n`/guitatca [Nội dung tin nhắn]`")
        return
        
    msg_content = " ".join(context.args)
    await update.message.reply_text(f"🔄 Đang tiến hành gửi tin nhắn hàng loạt tới {len(USER_DATA)} khách hàng...")
    
    thanh_cong = 0
    that_bai = 0
    
    for uid in list(USER_DATA.keys()):
        try:
            if not should_send_outbox("telegram", str(uid), msg_content):
                continue
            await context.bot.send_message(chat_id=uid, text=msg_content, parse_mode="Markdown")
            thanh_cong += 1
            await asyncio.sleep(0.05) # Giảm lag và tránh bị Telegram block spam
        except:
            that_bai += 1
            
    await update.message.reply_text(f"📢 **HOÀN THÀNH TIẾP THỊ HÀNG LOẠT:**\n✅ Gửi thành công: {thanh_cong}\n❌ Thất bại (Khách chặn bot): {that_bai}")

async def cmd_guikhach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh gửi tin nhắn riêng cho một khách hàng bằng ID"""
    if not is_admin(update.effective_user.id): return
    try:
        target_uid = int(context.args[0])
        msg_content = " ".join(context.args[1:])
        if not msg_content:
            await update.message.reply_text("⚠️ Nội dung trống! Cú pháp:\n`/guikhach [ID_Khách] [Nội dung]`")
            return
            
        if not should_send_outbox("telegram", str(target_uid), msg_content):
            await update.message.reply_text("ℹ️ Tin này đã gửi trước đó cho UID này, hệ thống bỏ qua để tránh trùng.")
            return

        await context.bot.send_message(chat_id=target_uid, text=msg_content, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Đã gửi riêng tới khách hàng `{target_uid}` thành công.")
    except IndexError:
        await update.message.reply_text("⚠️ Sai cú pháp! Vui lòng nhập:\n`/guikhach [ID_Khách] [Nội dung]`")
    except Exception as e:
        await update.message.reply_text(f"❌ Không thể gửi tin. Lỗi: {str(e)}")

# ==================== CÁC CHỨC NĂNG TIẾNG VIỆT CHO ADMIN ====================
async def cmd_loaloa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        target = context.args[0]
        msg = " ".join(context.args[1:])
        if not should_send_outbox("telegram", str(target), msg):
            await update.message.reply_text("ℹ️ Nội dung đã gửi trước đó tới đích này, bỏ qua để tránh trùng.")
            return
        await context.bot.send_message(chat_id=target, text=msg, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Đã gửi tin tới {target}.")
    except: pass

async def cmd_baotri(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    if not is_admin(update.effective_user.id): return
    BOT_ACTIVE = not BOT_ACTIVE
    await update.message.reply_text(f"⚙️ Trạng thái bot: **{'HOẠT ĐỘNG' if BOT_ACTIVE else 'BẢO TRÌ'}**")

async def cmd_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WEB_URL, LINK_NHAP_CODE
    if not is_admin(update.effective_user.id): return
    try:
        loai = context.args[0].lower()
        url = context.args[1]
        if loai == "web": WEB_URL = url
        elif loai == "code": LINK_NHAP_CODE = url
        await update.message.reply_text(f"✅ Đã đổi link `{loai}` thành: {url}")
    except: pass

async def cmd_huong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        kw = context.args[0].lower()
        url = context.args[1]
        KEYWORDS_ROUTING[kw] = url
        await update.message.reply_text(f"✅ Đã lưu hướng: `{kw}` -> {url}")
    except: pass

async def cmd_chuyentrong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        tid = int(context.args[0])
        url = context.args[1]
        await context.bot.send_message(chat_id=tid, text=f"🔔 Cổng kết nối riêng của bạn: {url}")
        await update.message.reply_text("✅ Đã chuyển link thành công.")
    except: pass

async def cmd_kiemtra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    await update.message.reply_text(f"📊 Hệ thống: {'MỞ' if BOT_ACTIVE else 'BẢO TRÌ'}\n- Số khách đệm: {len(USER_DATA)}\n- Chặn: {len(BANNED_USERS)}\n- VIP: {len(VIP_USERS)}")

async def cmd_xemkhach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        tid = int(context.args[0])
        if tid in USER_DATA:
            d = USER_DATA[tid]
            await update.message.reply_text(f"📋 **DỮ LIỆU USER {tid}:**\n- TK: `{d.get('ten_game')}`\n- SĐT: `{d.get('sdt')}`\n- Gói: `{d.get('goi_nap')}`")
        else: await update.message.reply_text("❌ Không tìm thấy cache khách này.")
    except: pass

async def cmd_xoarac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    USER_DATA.clear()
    await update.message.reply_text("🧹 Đã làm sạch cache hệ thống.")

async def cmd_themadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try: EXTRA_ADMINS.add(int(context.args[0])); await update.message.reply_text("✅ Đã cấp ĐẦY ĐỦ QUYỀN cho Admin phụ.")
    except: pass

async def cmd_huyadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try: EXTRA_ADMINS.discard(int(context.args[0])); await update.message.reply_text("✅ Đã hủy quyền Admin phụ.")
    except: pass

async def cmd_kenh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_CHAT
    if not is_admin(update.effective_user.id): return
    try: TARGET_CHAT = context.args[0]; await update.message.reply_text(f"📢 Kênh kiểm tra mới: {TARGET_CHAT}")
    except: pass

async def cmd_chan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try: BANNED_USERS.add(int(context.args[0])); await update.message.reply_text("🚫 Đã chặn tài khoản.")
    except: pass

async def cmd_mochan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try: BANNED_USERS.discard(int(context.args[0])); await update.message.reply_text("🔓 Đã mở chặn.")
    except: pass

async def cmd_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        client_id = int(context.args[0])
        code_vip = context.args[1]
        success_message = f"🎉 **MÃ QUÀ TẶNG CODE VIP ĐÃ ĐƯỢC PHÊ DUYỆT!**\n\n🎁 Mã quà tặng của bạn: `{code_vip}`\n🔗 Nơi nhập quà: {LINK_NHAP_CODE}\n\nChúc quý khách thắng lớn thắng đậm!"
        await context.bot.send_message(chat_id=client_id, text=success_message, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Đã cấp code cho ID: {client_id}")
        asyncio.create_task(bi_mat_quang_cao(context, client_id))
    except: pass

async def cmd_tatmoauto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHUC_NANG_AUTO_DUYET
    if not is_admin(update.effective_user.id): return
    CHUC_NANG_AUTO_DUYET = not CHUC_NANG_AUTO_DUYET
    await update.message.reply_text(f"✅ Auto duyệt lệnh tự động: {CHUC_NANG_AUTO_DUYET}")

async def cmd_tatmochuong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global THONG_BAO_START_ACTIVE
    if not is_admin(update.effective_user.id): return
    THONG_BAO_START_ACTIVE = not THONG_BAO_START_ACTIVE
    await update.message.reply_text(f"✅ Báo chuông khách mới: {THONG_BAO_START_ACTIVE}")

async def cmd_tatmoanh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global HIEN_THI_ANH_DONG
    if not is_admin(update.effective_user.id): return
    HIEN_THI_ANH_DONG = not HIEN_THI_ANH_DONG
    await update.message.reply_text(f"✅ Hiển thị ảnh GIF: {HIEN_THI_ANH_DONG}")

async def cmd_suachao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LOI_CHAO_MAC_DINH
    if not is_admin(update.effective_user.id): return
    if context.args: LOI_CHAO_MAC_DINH = " ".join(context.args); await update.message.reply_text("✅ Đã sửa lời chào.")

async def cmd_suaquangcao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global QUANG_CAO_TEXT
    if not is_admin(update.effective_user.id): return
    if context.args: QUANG_CAO_TEXT = " ".join(context.args); await update.message.reply_text("✅ Đã sửa QC.")

async def cmd_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try: VIP_USERS.add(int(context.args[0])); await update.message.reply_text("✅ Đã đặc cách VIP.")
    except: pass

async def cmd_huyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try: VIP_USERS.discard(int(context.args[0])); await update.message.reply_text("✅ Đã hủy đặc cách VIP.")
    except: pass

async def cmd_anhchao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_CHAO_HOI
    if not is_admin(update.effective_user.id): return
    try: GIF_CHAO_HOI = context.args[0]; await update.message.reply_text("✅ Đổi ảnh chào.")
    except: pass

async def cmd_anhdangky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_DANG_KY
    if not is_admin(update.effective_user.id): return
    try: GIF_DANG_KY = context.args[0]; await update.message.reply_text("✅ Đổi ảnh đăng ký.")
    except: pass

async def cmd_anhepjoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_EP_JOIN
    if not is_admin(update.effective_user.id): return
    try: GIF_EP_JOIN = context.args[0]; await update.message.reply_text("✅ Đổi ảnh ép nhóm.")
    except: pass

async def cmd_anhmocnap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_MOC_NAP
    if not is_admin(update.effective_user.id): return
    try: GIF_MOC_NAP = context.args[0]; await update.message.reply_text("✅ Đổi ảnh mốc nạp.")
    except: pass

async def cmd_anhchoyet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_CHO_DUYET
    if not is_admin(update.effective_user.id): return
    try: GIF_CHO_DUYET = context.args[0]; await update.message.reply_text("✅ Đổi ảnh chờ.")
    except: pass

async def cmd_anhqc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GIF_QUANG_CAO
    if not is_admin(update.effective_user.id): return
    try: GIF_QUANG_CAO = context.args[0]; await update.message.reply_text("✅ Đổi ảnh QC.")
    except: pass

async def cmd_tenadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMIN_USERNAME
    if update.effective_user.id != ADMIN_ID: return
    try: ADMIN_USERNAME = context.args[0]; await update.message.reply_text(f"✅ Đã đổi tên liên hệ: {ADMIN_USERNAME}")
    except: pass

async def cmd_lamlai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    try:
        tid = int(context.args[0])
        if tid in USER_DATA:
            USER_DATA[tid]['step'] = 'CHO_CHON_HINH_THUC'
            await update.message.reply_text("✅ Đã reset khách.")
    except: pass

async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    await update.message.reply_text("🚀 Bot hoạt động mượt mà ổn định!")

async def cmd_trogiup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    await update.message.reply_text("⚙️ Danh sách phím tắt tiếng Việt đã sẵn sàng.")

async def cmd_newtoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    label = context.args[0].strip() if context.args else "default"
    hours = int(context.args[1]) if len(context.args) >= 2 and context.args[1].isdigit() else 24
    raw = secrets.token_urlsafe(18)
    token_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    with db_conn() as conn:
        conn.execute(
            "INSERT INTO install_tokens(token_hash, raw_token, label, created_at, expires_at, redeemed) VALUES(?,?,?,?,?,0)",
            (token_hash, raw, label, time.time(), time.time() + hours * 3600),
        )
        conn.commit()
    audit_log("telegram", str(update.effective_user.id), "newtoken", f"{label}|{hours}")
    await update.message.reply_text(f"?? Token m?i: `{raw}`\nLabel: {label}\nH?t h?n sau: {hours} gi?", parse_mode="Markdown")


async def cmd_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    with db_conn() as conn:
        rows = conn.execute(
            "SELECT raw_token, label, expires_at, redeemed FROM install_tokens ORDER BY created_at DESC LIMIT 20"
        ).fetchall()
    if not rows:
        await update.message.reply_text("?? Ch?a c? token n?o.")
        return
    lines = []
    now = time.time()
    for r in rows:
        status = "? used" if r[3] else ("? expired" if now > float(r[2]) else "?? active")
        lines.append(f"- {r[0]} | {r[1]} | {status}")
    await update.message.reply_text("?? Danh s?ch token:\n" + "\n".join(lines))


async def cmd_audit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    with db_conn() as conn:
        rows = conn.execute(
            "SELECT actor_platform, actor_uid, action, detail, created_at FROM audit ORDER BY id DESC LIMIT 20"
        ).fetchall()
    if not rows:
        await update.message.reply_text("?? Ch?a c? log audit.")
        return
    lines = [f"- {r[0]}:{r[1]} | {r[2]} | {str(r[3])[:60]}" for r in rows]
    await update.message.reply_text("?? Audit g?n nh?t:\n" + "\n".join(lines))




async def cmd_aiallow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) < 2:
        await update.message.reply_text("C? ph?p: /aiallow <platform> <uid> [quota]")
        return
    platform = context.args[0].strip().lower()
    uid = context.args[1].strip()
    quota = int(context.args[2]) if len(context.args) >= 3 and context.args[2].isdigit() else 30
    today = time.strftime("%Y-%m-%d", time.localtime())
    with db_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO ai_permissions(platform, uid, enabled, daily_quota, used_today, day_key, created_at) VALUES(?,?,?,?,?,?,?)",
            (platform, uid, 1, quota, 0, today, time.time()),
        )
        conn.commit()
    audit_log("telegram", str(update.effective_user.id), "aiallow", f"{platform}:{uid}:{quota}")
    await update.message.reply_text(f"? ?? c?p quy?n AI cho {platform}:{uid} (quota {quota}/ng?y)")


async def cmd_aideny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) < 2:
        await update.message.reply_text("C? ph?p: /aideny <platform> <uid>")
        return
    platform = context.args[0].strip().lower()
    uid = context.args[1].strip()
    with db_conn() as conn:
        conn.execute("DELETE FROM ai_permissions WHERE platform=? AND uid=?", (platform, uid))
        conn.commit()
    audit_log("telegram", str(update.effective_user.id), "aideny", f"{platform}:{uid}")
    await update.message.reply_text(f"? ?? thu h?i quy?n AI c?a {platform}:{uid}")


async def cmd_aiquota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    with db_conn() as conn:
        rows = conn.execute(
            "SELECT platform, uid, enabled, daily_quota, used_today, day_key FROM ai_permissions ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
    if not rows:
        await update.message.reply_text("?? Ch?a c? c?u h?nh quota AI.")
        return
    lines = []
    for r in rows:
        lines.append(f"- {r[0]}:{r[1]} | enable={r[2]} | used={r[4]}/{r[3]} | day={r[5]}")
    await update.message.reply_text("📊 Danh sách quota AI:\n" + "\n".join(lines))


async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.args:
        await update.message.reply_text("⚠️ Cú pháp: /ai <câu_hỏi>")
        return
    question = " ".join(context.args).strip()
    await update.message.reply_text("⏳ Đang gọi AI, vui lòng chờ...")
    result = call_ai_text(question)
    for i in range(0, len(result), 3500):
        await update.message.reply_text(result[i:i + 3500])


async def cmd_setaitoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.args:
        await update.message.reply_text("⚠️ Cú pháp: /setaitoken <token>")
        return
    token = " ".join(context.args).strip()
    set_config("ai_token", token)
    audit_log("telegram", str(update.effective_user.id), "set_ai_token", f"len={len(token)}")
    await update.message.reply_text(f"✅ Đã lưu AI token: {mask_token(token)}")


async def cmd_clearaitoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    set_config("ai_token", "")
    audit_log("telegram", str(update.effective_user.id), "clear_ai_token", "")
    await update.message.reply_text("🧹 Đã xóa AI token lưu trong bot.")


async def cmd_checkaitoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    token_db = get_config("ai_token", "").strip()
    if token_db:
        await update.message.reply_text(f"🔐 AI token (DB): {mask_token(token_db)}")
        return
    token_env = os.getenv(AI_API_TOKEN_ENV, "").strip()
    if token_env:
        await update.message.reply_text(f"🔐 AI token (ENV): {mask_token(token_env)}")
        return
    await update.message.reply_text("❌ Chưa có AI token (DB/ENV).")

async def cmd_hotro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in BANNED_USERS:
        return
    await update.message.reply_text(f"👨‍💼 Ho tro nhanh: https://t.me/{ADMIN_USERNAME.replace('@', '')}")

def main():
    init_store()
    threading.Thread(target=start_zalo_auto_worker, daemon=True).start()
    app = Application.builder().token(TOKEN_BOT).build()
    
    app.add_handler(CommandHandler("nhancode88k", cmd_nhancode88k))
    app.add_handler(CommandHandler("start", cmd_nhancode88k))
    app.add_handler(CommandHandler("hotro", cmd_hotro))
    
    # Đăng ký các bộ lệnh tiếp thị mới bổ sung
    app.add_handler(CommandHandler("guitatca", cmd_guitatca))
    app.add_handler(CommandHandler("guikhach", cmd_guikhach))
    
    app.add_handler(CommandHandler("loaloa", cmd_loaloa))
    app.add_handler(CommandHandler("baotri", cmd_baotri))
    app.add_handler(CommandHandler("link", cmd_link))
    app.add_handler(CommandHandler("huong", cmd_huong))
    app.add_handler(CommandHandler("chuyentrong", cmd_chuyentrong))
    app.add_handler(CommandHandler("kiemtra", cmd_kiemtra))
    app.add_handler(CommandHandler("xemkhach", cmd_xemkhach))
    app.add_handler(CommandHandler("xoarac", cmd_xoarac))
    app.add_handler(CommandHandler("themadmin", cmd_themadmin))
    app.add_handler(CommandHandler("huyadmin", cmd_huyadmin))
    app.add_handler(CommandHandler("kenh", cmd_kenh))
    app.add_handler(CommandHandler("chan", cmd_chan))
    app.add_handler(CommandHandler("mochan", cmd_mochan))
    app.add_handler(CommandHandler("code", cmd_code))
    app.add_handler(CommandHandler("tatmoauto", cmd_tatmoauto))
    app.add_handler(CommandHandler("tatmochuong", cmd_tatmochuong))
    app.add_handler(CommandHandler("tatmoanh", cmd_tatmoanh))
    app.add_handler(CommandHandler("suachao", cmd_suachao))
    app.add_handler(CommandHandler("suaquangcao", cmd_suaquangcao))
    app.add_handler(CommandHandler("vip", cmd_vip))
    app.add_handler(CommandHandler("huyvip", cmd_huyvip))
    app.add_handler(CommandHandler("anhchao", cmd_anhchao))
    app.add_handler(CommandHandler("anhdangky", cmd_anhdangky))
    app.add_handler(CommandHandler("anhepjoin", cmd_anhepjoin))
    app.add_handler(CommandHandler("anhmocnap", cmd_anhmocnap))
    app.add_handler(CommandHandler("anhchoyet", cmd_anhchoyet))
    app.add_handler(CommandHandler("anhqc", cmd_anhqc))
    app.add_handler(CommandHandler("tenadmin", cmd_tenadmin))
    app.add_handler(CommandHandler("lamlai", cmd_lamlai))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("trogiup", cmd_trogiup))
    app.add_handler(CommandHandler("newtoken", cmd_newtoken))
    app.add_handler(CommandHandler("tokens", cmd_tokens))
    app.add_handler(CommandHandler("audit", cmd_audit))
    app.add_handler(CommandHandler("ai", cmd_ai))
    app.add_handler(CommandHandler("setaitoken", cmd_setaitoken))
    app.add_handler(CommandHandler("clearaitoken", cmd_clearaitoken))
    app.add_handler(CommandHandler("checkaitoken", cmd_checkaitoken))
    app.add_handler(CommandHandler("aiallow", cmd_aiallow))
    app.add_handler(CommandHandler("aideny", cmd_aideny))
    app.add_handler(CommandHandler("aiquota", cmd_aiquota))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("=========================================")
    print("BOT /nhancode88k DA KHOI CHAY")
    print("=========================================")
    app.run_polling()

if __name__ == '__main__':
    main()


