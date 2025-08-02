# Telegram Weather Bot

A simple Telegram bot that provides weather information for any city. Built with Python and python-telegram-bot.

## Features
- Responds to /start and /weather commands
- Fetches weather information for a given city (API integration coming soon)
- Easy to deploy and extend

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Ampter/Telegram-weather-bot.git
   cd Telegram-weather-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Telegram bot token:
   - Replace `'YOUR_TELEGRAM_BOT_TOKEN'` in `bot.py` with your actual bot token from BotFather.

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage
- `/start` - Get a welcome message and instructions.
- `/weather <city>` - Get weather information for the specified city.

### Example
```
/user: /weather London
/bot: Weather for London: [data not available yet]
```

## Contribution
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[Specify your license here]
