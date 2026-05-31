# userbot_scanner (Windows 10)

Userbot Telethon de quet so dien thoai Viet Nam tu:
- Van ban admin gui truc tiep.
- File `.txt`, `.csv`, `.vcf` voi lenh `/scan`.
- Contact duoc chia se/forward (`MessageMediaContact`).

## 1) Yeu cau
- Windows 10
- Python 3.10+ (da test voi Python 3.14)
- Ket noi Internet
- API Telegram tu [https://my.telegram.org](https://my.telegram.org)

## 2) Cau truc thu muc
Mac dinh he thong su dung `BASE_DIR=D:\ZALO_MOVE\userbot_scanner` va tao:
- `logs/` log runtime
- `temp/` file tam tai ve de quet
- `results/` file ket qua khi danh sach dai
- `sessions/` session Telethon (`userbot_session.session`)

## 3) Cai dat nhanh
1. Copy `.env.example` thanh `.env`.
2. Dien gia tri that:
   - `API_ID`
   - `API_HASH`
   - `ADMIN_ID`
3. Chay:
   - `run_userbot_scanner.bat`

Hoac chay tay:
```powershell
python -m pip install -r requirements.txt
python userbot_scanner.py
```

## 4) Luong hoat dong
- Chi xu ly tin nhan neu `sender_id == ADMIN_ID`.
- Text thuong (khong bat dau bang `/`) => quet ngay.
- `/scan` + file `.txt/.csv/.vcf` (gui cung message, hoac reply `/scan` vao message co file) => tai file tam, quet, xoa file tam.
- Contact media => doc `phone_number`, chuan hoa, phan hoi.

## 5) Dinh dang ket qua
- Tom tat:
  - Tong chuoi phat hien
  - So hop le
  - So trung da loai
  - So duy nhat tra ve
- Neu so luong ket qua `> RESULT_THRESHOLD` (mac dinh 50), bot gui file ket qua trong `results/`.

## 6) Regex va chuan hoa
- Ho tro dau so: `+84`, `84`, `0`.
- Co loai bo khoang trang/dau `.` `-`.
- Chuan hoa dau ra ve dinh dang so bat dau bang `0`.
- Loai bo trung lap.

## 7) Bao mat va do on dinh
- Random delay (`RANDOM_DELAY_MIN`, `RANDOM_DELAY_MAX`) de giam burst.
- Bat `FloodWaitError` va cho theo `e.seconds`.
- Tu dong luu session, khong can OTP moi lan chay.

## 8) Kiem thu de xuat
- `python --version`
- `pip install -r requirements.txt`
- `python userbot_scanner.py`
- Gui text test tu admin va non-admin.
- Gui `.txt/.csv/.vcf` voi `/scan`.
- Chia se contact Telegram cho bot.
- Test list > 50 so de xac nhan gui file ket qua.

## 9) Loi thuong gap
- `Thieu cau hinh bat buoc`: kiem tra `.env`.
- `FloodWaitError`: bot se tu cho, khong can tat.
- Khong phan hoi: kiem tra `ADMIN_ID` dung hay khong.
