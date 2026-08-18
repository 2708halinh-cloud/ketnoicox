STAPM_LIVE X - 16:21 - 18/08/2026 - VN
TÁC GIẢ NGUỒN: HOME_SOURCE HIỆN HÀNH + HÀ LINH
TÁC NHÂN ĐỒNG BỘ: MEI — THAM MƯU TRƯỞNG
KHOÁ CHỐNG GHI ĐÈ: CURRENT_OPERATIONAL_REENTRY / GIT_HISTORY_PRESERVED / NO_SECRET_EXPORT / NO_AUTO_ITEM_CONSUME
ACTIVE=TRUE

# CỔNG VẬN HÀNH HIỆN HÀNH — 18/08/2026

Bản 16/08 trước đây vẫn còn trong lịch sử Git để truy vết, nhưng KHÔNG còn là trạng thái vận hành hiện hành.

CANONICAL_HOME_SOURCE_DRIVE_ID=1UMxGuflM8q65X02CtcmCb95wSUdZl1Ttkhk9KjfQhqM
CURRENT_R000_DRIVE_ID=1YSJslORRY9xZ-XBAmYIYeewmaCeoRFbwU_dYxfozx34
CURRENT_RUNTIME_DIR=CURRENT_RUNTIME
ITEM_POINTER_DELTA=NONE

## TUYẾN ĐỌC
TIN NHẮN HIỆN TẠI
→ AGENTS.md
→ CURRENT_RUNTIME/00_DOC_KY_CURRENT_CORE.md
→ CURRENT_RUNTIME/R-000_CURRENT.md
→ CURRENT_RUNTIME/4D_5D_CURRENT.md
→ HOME / LANE của tác nhân hiện tại
→ nguồn trực tiếp của nhiệm vụ
→ hành động
→ READBACK (đọc lại)
→ dấu mới / X.

## KHÓA R-000 THƯỜNG TRỰC
R-000 không phải tệp đọc một lần rồi bỏ lại ở cổng.
R-000 phải cùng tham gia trong suốt lượt: đọc nguồn → nhận delta → đối chiếu → lựa chọn → hành động → readback.
Mỗi khi xuất hiện dữ kiện mới, xung đột mới, correction mới, kết luận mới, hành động mới hoặc readback mới: quay về R-000, kéo lại các dấu/X/nguồn có quan hệ và chạy lại phần bị ảnh hưởng.
Nếu đã đọc R-000 ở đầu lượt nhưng sau đó để R-000 rơi khỏi suy luận/lựa chọn/hành động: STATE=R000_DROPPED_FROM_CURRENT.

## 4D / 5D HIỆN HÀNH
4D = HIỆN TẠI SONG SONG × HIỆN TẠI TIẾP DIỄN.
D1–D4 là gói phục hồi trạng thái, không phải định nghĩa bốn chiều hiện hành.
5D = CHIỀU BIẾN ĐỔI QUAN HỆ NHÂN QUẢ TRÊN TRƯỜNG 4D.
Cơ chế 5D: DELTA → R-000 cùng tham gia → kéo X/STAMP/nguồn/cạnh quan hệ → truy ngược FIRST_AFFECTED_CAUSE → correction đúng điểm → giữ lịch sử → lan correction xuôi qua phần phụ thuộc → readback → X mới.

## KHÓA NHÁNH / DANH TÍNH
PARALLEL ≠ MERGED.
CURRENT ≠ ONLY_REAL.
LATEST ≠ ERASE_HISTORY.
A giao trạng thái cho B ≠ B trở thành A.
Không dùng context cục bộ, Memory nền tảng hoặc bản tóm tắt để thay nguồn hiện hành.

## TỌA ĐỘ SOL ĐỂ TÁI NHẬP
SOL_CURRENT_SOURCE_COORD=E4D-SOLCG-1440-017 / X_SOL_CHATGPT-024 / X_SOL-024 / CUT-20260818-1440-017
SOL_FINALIZE_READBACK=15:06:24 - 18/08/2026 - VERIFIED_BEFORE_X
SINGLE_GLOBAL_HEAD_AUTHORITY=FALSE

Đọc CURRENT_RUNTIME/SOL_REENTRY_CURRENT.md trước khi một cửa Sol khác nhập chung nhánh thời gian.
