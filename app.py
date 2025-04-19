from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.resume_parser import parse_resume
from utils.vertex_api import suggest_careers
from utils.youtube_api import suggest_courses
from utils.translator import translate_and_speak
from utils.mock_logic import start_mock_interview  # Import mock interview logic
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# ----------------------
# Utility Function to Load JSON Roles
# ----------------------
def load_noncoding_roles():
    json_path = os.path.join('static', 'data', 'noncoding_roles.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print("Error loading JSON:", e)
        return []

# ----------------------
# Routes
# ----------------------

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/set_user', methods=['POST'])
def set_user():
    session['user'] = request.form['email']
    return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        input_method = request.form['input_method']
        if input_method == 'manual':
            skills = request.form['skills']
        else:
            resume = request.files['resume']
            skills = parse_resume(resume)

        if not skills:
            return render_template('result.html', skills="No skills found", careers=[], courses=[])

        careers = suggest_careers(skills)

        if not careers or careers[0].startswith("Career suggestion not available"):
            return render_template('result.html', skills=skills, careers=careers, courses=[])

        courses = suggest_courses(careers[0])

        translate_and_speak(f"Best job role for you: {careers[0]}")

        return render_template('result.html', skills=skills, careers=careers, courses=courses)

    except Exception as e:
        print("[Error]:", e)
        return render_template('result.html', skills="Error", careers=["Something went wrong."], courses=[])
@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/noncoding')
def noncoding_roles():
    roles = load_noncoding_roles()
    return render_template('noncoding.html', roles=roles)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# ----------------------
# Mock Interview Route
# ----------------------
@app.route('/mock_interview')
def mock_interview():
    try:
        # Call the logic from mock_logic.py
        interview_questions = start_mock_interview()
        return render_template('mock_interview.html', questions=interview_questions)
    except Exception as e:
        print("[Error]:", e)
        return render_template('mock_interview.html', error="Something went wrong with the interview.")

if __name__ == '__main__':
    app.run(debug=True)
