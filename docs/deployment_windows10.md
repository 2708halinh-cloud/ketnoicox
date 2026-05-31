# Tai lieu trien khai Windows 10

## Muc tieu
Trien khai `userbot_scanner.py` tren may Windows 10 de quet so dien thoai Viet Nam tu text, file va contact media cua ADMIN.

## Buoc 1: Chuan bi moi truong
1. Cai Python 3.10+.
2. Mo PowerShell tai thu muc du an.
3. Chay:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Buoc 2: Cau hinh
1. Tao `.env` tu `.env.example`.
2. Cap nhat:
   - `API_ID`
   - `API_HASH`
   - `ADMIN_ID`
3. Neu can doi duong dan runtime:
   - `BASE_DIR=D:\ZALO_MOVE\userbot_scanner`

## Buoc 3: Chay service
- Cach 1: click `run_userbot_scanner.bat`
- Cach 2:
```powershell
python userbot_scanner.py
```

Lan dau dang nhap Telethon co the yeu cau ma OTP/2FA. Sau khi thanh cong, session se duoc luu o:
- `D:\ZALO_MOVE\userbot_scanner\sessions\userbot_session.session`

## Buoc 4: Van hanh
- Text thuong tu admin: bot quet ngay.
- File `.txt/.csv/.vcf`: gui file kem `/scan` hoac reply `/scan` vao message co file.
- Contact Telegram: bot trich SDT tu `MessageMediaContact`.

## Buoc 5: Giam sat
- Log: `D:\ZALO_MOVE\userbot_scanner\logs\userbot_scanner.log`
- Temp: `D:\ZALO_MOVE\userbot_scanner\temp\`
- Ket qua dai: `D:\ZALO_MOVE\userbot_scanner\results\`

## Xu ly su co
- Khong nhan lenh: kiem tra `ADMIN_ID`.
- Bao loi cau hinh: kiem tra `.env`.
- FloodWait: he thong tu cho theo so giay Telegram yeu cau.
