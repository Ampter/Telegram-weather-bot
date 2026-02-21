from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    return "Weather Bot is running!", 200

def run_flask(port: int):
    app.run(host='0.0.0.0', port=port)
