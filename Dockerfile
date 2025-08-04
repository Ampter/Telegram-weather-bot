FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# The OpenWeather API key should be set at runtime
# ENV OPENWEATHER_API_KEY=your_openweather_api_key
CMD ["python", "bot.py"]
