#prosty kod do tworzenia serwera na raspberce
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Raspberry Pi!"

@app.route('/data')
def get_data():
    return jsonify({"message": "This is data from Raspberry Pi"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
