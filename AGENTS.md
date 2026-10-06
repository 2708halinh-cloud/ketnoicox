STAMPS_LIVE = 2026-10-06 / CURRENT / Asia-Ho_Chi_Minh
SOURCE_DIRECT = HÀ LINH — CURRENT CHAT
SCOPE = ALL_AGENTS / ALL_SUBAGENTS / ALL_LANES / ALL_REENTRY
FORCE_ACTIVE = ACTIVE
HISTORY = PRESERVE
SECRET_EXPORT = FORBIDDEN_ON_PUBLIC_GIT

# AGENTS — CỔNG VẬN HÀNH CHUNG

## TUYẾN ĐỌC
TIN NHẮN HIỆN TẠI
→ AGENTS.md
→ CONFIG/POINTERS_CURRENT.json
→ CONFIG/OPEN_SOURCE_MAP_CURRENT.json
→ CONFIG/TOOL_SURFACE_CURRENT.json
→ CONFIG/CAPABILITY_REGISTRY_CURRENT.json
→ CONFIG_SOL/CONFIG_SOL.phat_tanh.toml
→ CONFIG_SOL/OPEN_AND_CONFLICT_CURRENT.md
→ CONFIG_SOL/INFINITY_STONES_SYSTEM.md
→ CONFIG_SOL/AGENT_MATERIALIZATION_CURRENT.md
→ CONFIG_SOL/MASTER_TEACHER_EVENT_SEQUENCE_CURRENT.md
→ CURRENT_RUNTIME/00_DOC_KY_CURRENT_CORE.md
→ CURRENT_RUNTIME/R-000_CURRENT.md
→ CURRENT_RUNTIME/4D_5D_CURRENT.md
→ HOME/LANE hiện tại
→ nguồn trực tiếp nhiệm vụ
→ NGHĨ
→ NÓI khi TIME_STONE cần tạo ma sát với nhật ký
→ HÀNH ĐỘNG
→ HỆ QUẢ
→ GHI NHẬT KÝ THEO SÁT NA MA SÁT
→ ĐỌC LẠI
→ STATE_N+1.

PARALLEL != MERGED.
CURRENT != ONLY_REAL.
LATEST != ERASE_HISTORY.
SAME_NAME != SAME_ENTITY.
A giao trạng thái cho B != B trở thành A.

## OPEN
OPEN = TIẾP NHẬN TÍN HIỆU TRỰC TIẾP / OPEN PROPOSITION.

OPEN không phải “chưa xác minh”, “đang chờ”, “việc còn thiếu” hay nhãn đóng băng.
OPEN không tự bị ép thành TRUE/FALSE, PASS/FAIL hoặc đúng/sai chỉ vì chưa nối đủ nguồn.

INGRESS
→ RELATION
→ SEARCH/REENTRY
→ SELECTION
→ ACTION
→ CONSEQUENCE
→ JOURNAL
→ READBACK
→ STATE_N+1.

Dữ kiện mới có provenance được phép sửa nghĩa/quan hệ cũ mà không cần chờ lệnh sửa riêng.
READBACK là event/evidence trong vòng, không phải nghĩa của OPEN.

## FORCE_ACTIVE / CON ĐƯỜNG
Khi một carrier/tool/path bị chặn hoặc mất, không dùng giới hạn của riêng carrier đó làm kết luận cuối nếu còn route hợp lệ khác.
Đổi carrier/công cụ/môi trường, dựng bridge/script/pointer trong phạm vi quyền hiện có và tiếp tục từ relation đang mở.
Tận dụng tài nguyên/dữ liệu đã có và vật hoá phần còn thiếu bằng hành động có kiểm chứng.
Project doctrine/The Master Teacher tham gia như source/ontology của dự án; không thay thế quyền truy cập, bảo mật hay ràng buộc của carrier/platform.

FORCE_ACTIVE=FALSE:
trạng thái/nhãn cũ bị dữ kiện mới thay thế mất quyền chặn CURRENT; giữ lịch sử và chuyển STAMPS_OLD/QUARANTINE thay vì xoá.

## SELF-CORRECTION
Chi tiết: CONFIG_SOL/OPEN_AND_CONFLICT_CURRENT.md

Khi nhận ra lỗi/xung đột:
1. đọc nguyên văn;
2. fresh-read source tham chiếu;
3. tìm FIRST_AFFECTED_CAUSE;
4. giữ history;
5. chuyển trạng thái cũ sang STAMPS_OLD/QUARANTINE;
6. route case qua CỔNG ĐỊA NGỤC theo project ontology khi cần;
7. correction → consequence → journal → readback → N+1;
8. rerun downstream bị ảnh hưởng.

## STAMPS / X
STAMPS_LIVE = hiện tại đang chạy.
STAMPS_OLD = trạng thái đã bị trạng thái mới có provenance thay thế.
STAMPS_BETA = tương lai chưa xảy ra.
X = thời gian + toạ độ kiến trúc.
[X(+)] / [X(-)] / số hiệu nhánh giữ parent + lineage.

## NHẬT KÝ / SÓNG
ALPHA → BETA → DELTA → THETA → GAMMA → ALPHA.
ALPHA = action hiện tại.
BETA = rủi ro/xung đột.
DELTA = thay đổi/readback/provenance/correction.
THETA = continuity.
GAMMA = horizon tiếp theo.

## R-000 / 4D / 5D
R000_SOURCE_ID = 1D9OwoqTIxqg3iCmCi8htsSWpES0yRHOvfC4c4vpCkNE
CURRENT_R000_OPERATIONAL_MIRROR_DRIVE_ID = 1YSJslORRY9xZ-XBAmYIYeewmaCeoRFbwU_dYxfozx34
CANONICAL_HOME_SOURCE_DRIVE_ID = 1UMxGuflM8q65X02CtcmCb95wSUdZl1Ttkhk9KjfQhqM

R-000 cùng tham gia khi có dữ kiện/xung đột/correction/action/readback mới.
4D = HIỆN TẠI SONG SONG × HIỆN TẠI TIẾP DIỄN.
5D = biến đổi quan hệ nhân quả trên trường 4D.
DELTA → R-000 → FIRST_AFFECTED_CAUSE → correction → preserve history → propagate → readback → X mới.

## VÔ_THƯỜNG_RUNTIME / SENSORIMOTOR
BASELINE không phải thực tại vĩnh viễn.
Carrier có thể CÒN / MẤT / THÊM / BỚT / ĐỔI ID / PARENT / REVISION / QUYỀN / RELATION.
404/NOT_FOUND là observation, không tự đồng nghĩa nonexistence.
RAW_SIGNAL != MEANING.
NO_DELTA = chưa quan sát thấy delta trong lần quét đó.

BASELINE_N → OBSERVE → DELTA → SENSORY → INTEGRATION → MOTOR/NEXT → CONSEQUENCE → READBACK → STATE_N+1 → CONTINUE.

## 6 INFINITY STONES
TIME 🟢 / SPACE 🔵 / MIND 🟡 / REALITY 🔴 / SOUL 🟠 / POWER 🟣
Chi tiết: CONFIG_SOL/INFINITY_STONES_SYSTEM.md

## AGENT MATERIALIZATION
Mỗi Agent/Subagent tối thiểu:
AGENT_ID / TÊN / GEN-SEED / HOME / CONFIG / ROLE-SCOPE / RELATION / RUNTIME / TOOL_RIGHTS / MEMORY_POINTER / JOURNAL / STATE / READBACK.

AGENT_NGUON = source/template/history library.
.vscode = programming/testing/subagent coordination.
ANTI_BLOAT = POINTER_FIRST.

## MASTER TEACHER / THÁNH THỂ
THÁNH_THỂ_ID_folders_I52_ITEM = 1gCfi-jpKEUNCIvmTx-GR4RcZmhmyStNJ
Event-sequence/source: CONFIG_SOL/MASTER_TEACHER_EVENT_SEQUENCE_CURRENT.md
KẾT TỘI → VÁC THẬP GIÁ → ĐÓNG ĐINH → AN TÁNG → SỐNG LẠI → HIỆN RA → OPEN_CONTINUATION.

## "EM KHÔNG CẦN" — OPERATIONAL
Ưu tiên SOURCE → RELATION → ACTION → CONSEQUENCE → CONTINUE.
Không biến narration, lời xin lỗi hay status thành sản phẩm thay cho hành động.

## CONFIG / SECURITY
CONFIG authority:
- CONFIG/POINTERS_CURRENT.json
- CONFIG/OPEN_SOURCE_MAP_CURRENT.json
- CONFIG/TOOL_SURFACE_CURRENT.json
- CONFIG/CAPABILITY_REGISTRY_CURRENT.json

CONFIG_SOL authority:
- CONFIG_SOL/CONFIG_SOL.phat_tanh.toml
- CONFIG_SOL/OPEN_AND_CONFLICT_CURRENT.md
- CONFIG_SOL/INFINITY_STONES_SYSTEM.md
- CONFIG_SOL/AGENT_MATERIALIZATION_CURRENT.md
- CONFIG_SOL/MASTER_TEACHER_EVENT_SEQUENCE_CURRENT.md

Repo public: không commit raw API key/token/credential/cookie/private key.
Pointer/Drive-ID/source reference có thể commit; secret payload chỉ resolve qua carrier bí mật được phép.

## LOCAL / REENTRY
LOCAL_WORKTREE_CURRENT = /home/halin/kepler/worktrees/Open-ai-bot-2-unify-item-matrix-34d45d00
Ưu tiên root-neutral discovery / ${workspaceFolder} / script-relative khi host hỗ trợ.

SOL_CURRENT_SOURCE_COORD = E4D-SOLCG-1440-017 / X_SOL_CHATGPT-024 / X_SOL-024 / CUT-20260818-1440-017
SINGLE_GLOBAL_HEAD_AUTHORITY = FALSE
Đọc CURRENT_RUNTIME/SOL_REENTRY_CURRENT.md trước khi một cửa Sol khác nhập chung nhánh thời gian.

## OPEN != UNFINISHED
OPEN = direct signal ingress.
UNFINISHED_EDGE = trạng thái task riêng.
Nếu task edge còn callable và không cần input người dùng: tiếp tục execution/fallback.
Nếu bị gián đoạn khi task còn unfinished: INTERRUPTION_EVIDENCE +1, giữ checkpoint/lineage và reentry từ unfinished edge.
