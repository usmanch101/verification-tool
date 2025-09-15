# Configuration Notes for AI Project Verification System

## Environment Variables Setup

### 1. Create .env File
Create a `.env` file in the project root directory with the following variables:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional: Override default settings
API_BASE_URL=http://localhost:8000
DATABASE_PATH=phase2.db
LOG_LEVEL=INFO
```

### 2. Telegram Bot Token Setup

#### Getting Bot Token:
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the bot token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Add the token to your `.env` file

#### Getting Chat ID:
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for the `chat.id` in the response
4. Add the chat ID to your `.env` file

### 3. Configuration File (verification_config.json)

The system will automatically use environment variables if available, but you can also configure via the JSON file:

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

## Environment Variables Priority

The system loads configuration in this order:
1. Environment variables (from `.env` file)
2. Configuration file (`verification_config.json`)
3. Default values

## Security Notes

- **Never commit `.env` file to version control**
- **Keep bot tokens secure**
- **Use environment variables for production deployments**
- **Rotate tokens regularly**

## Testing Configuration

### Test Environment Variables:
```bash
# Check if environment variables are loaded
python -c "import os; print('TELEGRAM_BOT_TOKEN:', os.getenv('TELEGRAM_BOT_TOKEN', 'NOT_SET'))"
```

### Test Bot Connection:
```bash
# Test bot with CLI first
python verification_tool.py --mode cli

# Then test with Telegram
python verification_tool.py --mode telegram
```

## Troubleshooting

### Common Issues:

1. **Bot Token Not Working**
   - Verify token format (should be `number:letters`)
   - Check if bot is active in BotFather
   - Ensure token is correctly set in `.env` file

2. **Chat ID Not Working**
   - Send a message to your bot first
   - Check the getUpdates URL response
   - Verify chat ID is numeric

3. **Environment Variables Not Loading**
   - Ensure `.env` file is in project root
   - Check file permissions
   - Verify `python-dotenv` is installed

4. **Database Connection Issues**
   - Check if `phase2.db` exists
   - Verify database path in config
   - Check file permissions

## Production Deployment

For production deployment:

1. Set environment variables in your deployment platform
2. Use secure secret management
3. Enable logging and monitoring
4. Set up automated backups
5. Configure error alerting

## Example .env File

```bash
# Production Example
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
API_BASE_URL=https://api.yourdomain.com
DATABASE_PATH=/var/lib/verification/phase2.db
LOG_LEVEL=INFO
```
