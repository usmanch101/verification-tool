# Professional AI Project Verification System

## Overview
This is a professional verification tool built for AI project phases. It meets all requirements for automated testing, evidence generation, and Telegram integration.

## Features
- ✅ **Automated Verification Checks**: File structure, database schema, and API endpoints
- ✅ **Evidence Generation**: Timestamped JSON files with detailed results
- ✅ **Telegram Bot Integration**: Natural language commands via Telegram
- ✅ **Professional Reporting**: Clean, detailed reports with PASS/FAIL status
- ✅ **CLI Interface**: Single command execution
- ✅ **Comprehensive Logging**: Detailed logs for debugging and auditing
- ✅ **Environment Variable Support**: Secure token storage via .env file

## Quick Setup Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the project root:
```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional: Override default settings
API_BASE_URL=http://localhost:8000
DATABASE_PATH=phase2.db
```

### 3. Configure Telegram Bot
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Add the token to your `.env` file
4. Get your chat ID (send a message to your bot, then visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`)

### 4. Run Verification (CLI Mode)
```bash
python verification_tool.py --mode cli
```

### 5. Run with Telegram Bot
```bash
python verification_tool.py --mode telegram
```

## Usage Examples

### CLI Usage
```bash
# Basic verification
python verification_tool.py --mode cli

# Specify phase
python verification_tool.py --mode cli --phase phase2

# Use custom config
python verification_tool.py --mode cli --config custom_config.json
```

### Telegram Usage
Once the bot is running, send these commands:
- `Run Phase 2 test` - Execute verification
- `Run verification` - Execute verification
- `Status` - Check system status

## Configuration

### Environment Variables (.env file)
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
API_BASE_URL=http://localhost:8000
DATABASE_PATH=phase2.db
LOG_LEVEL=INFO
```

### Configuration File (verification_config.json)
```json
{
  "telegram_token": "YOUR_BOT_TOKEN_HERE",
  "project_name": "AI Project Phase 2 - Professional Verification System",
  "phase2_outputs": {
    "file_structure": {
      "required_files": [
        "main.py",
        "requirements.txt",
        "config.json",
        "verification_tool.py"
      ],
      "required_dirs": [
        "src/",
        "tests/",
        "data/",
        "verification_evidence/"
      ]
    },
    "database_schema": {
      "connection_string": "sqlite:///phase2.db",
      "required_tables": [
        "users",
        "conversations",
        "models"
      ]
    },
    "api_endpoints": {
      "base_url": "http://localhost:8000",
      "endpoints": [
        "/health",
        "/api/v1/chat",
        "/api/v1/models"
      ]
    }
  }
}
```

## Verification Components

### 1. File Structure Check
- Verifies required files exist
- Checks for required directories
- Generates evidence with file listings
- **Evidence**: `file_structure_YYYYMMDD_HHMMSS.json`

### 2. Database Schema Check
- Connects to SQLite database
- Verifies required tables exist
- Checks table schemas
- Generates evidence with database structure
- **Evidence**: `database_schema_YYYYMMDD_HHMMSS.json`

### 3. API Endpoints Check
- Tests API endpoint accessibility
- Measures response times
- Checks HTTP status codes
- Generates evidence with response details
- **Evidence**: `api_endpoints_YYYYMMDD_HHMMSS.json`

## Evidence Files
All verification results are stored in `verification_evidence/` directory:
- `file_structure_YYYYMMDD_HHMMSS.json` - File structure evidence
- `database_schema_YYYYMMDD_HHMMSS.json` - Database schema evidence
- `api_endpoints_YYYYMMDD_HHMMSS.json` - API endpoints evidence
- `verification_report_YYYYMMDD_HHMMSS.txt` - Human-readable report
- `verification.log` - Detailed chronological logs

## Project Structure
```
├── main.py                    # Main entry point
├── verification_tool.py       # Core verification system
├── verification_config.json   # Configuration file
├── requirements.txt           # Python dependencies
├── config.json               # Project configuration
├── .env                      # Environment variables (create this)
├── README.md                 # This documentation
├── demo.py                   # Demo script
├── phase2.db                 # SQLite database
├── src/                      # Source code directory
├── tests/                    # Test files directory
├── data/                     # Data files directory
└── verification_evidence/    # Evidence and logs
```

## Testing the System

### Run Demo
```bash
python demo.py
```

### Test PASS Scenario
```bash
python verification_tool.py --mode cli
```

### Test FAIL Scenario
1. Rename `phase2.db` to `phase2_backup.db`
2. Run verification: `python verification_tool.py --mode cli`
3. Restore: `mv phase2_backup.db phase2.db`

## Troubleshooting

### Common Issues
1. **Telegram Bot Not Responding**
   - Check bot token in `.env` file
   - Verify chat ID is correct
   - Ensure bot is started with `--mode telegram`

2. **Database Connection Failed**
   - Check if `phase2.db` exists
   - Verify database path in config
   - Check file permissions

3. **API Endpoints Not Accessible**
   - Verify API server is running
   - Check base URL in config
   - Test endpoints manually

### Logs
Check `verification_evidence/verification.log` for detailed error information.

---
**Built for Professional AI Project Success** 🚀
