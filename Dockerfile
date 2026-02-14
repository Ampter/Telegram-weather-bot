FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Required runtime variables:
# - TELEGRAM_TOKEN (or TELEGRAM_BOT_TOKEN)
# - OPENWEATHER_API_KEY
CMD ["python", "bot.py"]
