from flask import Flask, render_template, request, jsonify
from ai_logic import analyze_answers

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    feedback = analyze_answers(data)
    return jsonify({'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True)