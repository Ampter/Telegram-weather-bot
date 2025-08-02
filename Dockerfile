# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variable for Telegram bot token
ENV TELEGRAM_BOT_TOKEN=""

# Run the bot
CMD ["python", "bot.py"]
