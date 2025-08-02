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
   - Register for a free API key at https://openweathermap.org/appid
   - Set the environment variable:
     ```
     export OPENWEATHER_API_KEY=your_openweather_api_key
     ```
   - Or create a `.env` file with:
     ```
     OPENWEATHER_API_KEY=your_openweather_api_key
     ```
4. Run the bot:
   ```
   python bot.py
   ```

The Telegram bot token is already set in the code. You can change it in `bot.py` if you want to use your own bot.

## Usage
- Start the bot in Telegram.
- Send `/weather <city>` (e.g., `/weather London`) to get the current weather.

## Docker
A Dockerfile is provided for easy deployment.

## License
MIT License
