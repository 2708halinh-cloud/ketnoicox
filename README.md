# ketnoicox recovery bundle

This folder is the recovered copy of the bot repo from GitHub.

Core files:
- `tncodevip.py`: fuller merged bot version; recommended entry point.
- `codevip.py`: earlier bot version.
- `helpimgs/`: optional help images kept from the repo.
- `Api/proxi`: proxy config file from a separate repo; not required by the bot code.

Run on Windows:
1. Open PowerShell in this folder.
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Start the bot:
   ```powershell
   python main.py
   ```

Notes:
- `GH_MODELS_TOKEN` is only needed if you want the AI commands to work.
- `CODEX_DB` and `CODEX_DB_BACKUP` can be used to move the SQLite database path.
- The Telegram/Zalo credentials are currently hardcoded in the source. If these are real secrets, rotate them before sharing the code.
