# Telegram Weather Bot

A simple Telegram bot that provides current weather information for any city using the OpenWeather API.

## Features

- Get real-time weather for any city via Telegram
- Uses OpenWeather API
- Simple command: `/weather <city>`

## Setup

1. Clone this repository.
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. **Set your OpenWeather API key as an environment variable:**
   - Register for a free API key at [https://openweathermap.org/appid](https://openweathermap.org/appid)
   - Set the environment variable:

     ```
     export OPENWEATHER_API_KEY=your_openweather_api_key
     ```

   - Or create a `.env` file with:

     ```
     OPENWEATHER_API_KEY=your_openweather_api_key
     ```

4. **Set your Telegram bot token as an environment variable or in a .env file:**
   - Create a new bot and get your token from [BotFather](https://t.me/botfather)
   - Set the environment variable:

     ```
     export TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     ```

   - Or add to your `.env` file:

     ```
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     ```

   - Make sure `bot.py` loads the token from the environment.

5. Run the bot:

   ```
   python bot.py
   ```

## Usage

- Start the bot in Telegram.
- Send `/weather <city>` (e.g., `/weather London`) to get the current weather.

## Docker

A Dockerfile is provided for easy deployment.

## License

MIT License
