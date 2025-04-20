from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.resume_parser import parse_resume
from utils.vertex_api import suggest_careers
from utils.youtube_api import suggest_courses
from utils.translator import translate_and_speak
import google.generativeai as genai
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# Configure the Gemini API
GOOGLE_API_KEY = "AIzaSyDHC5gKZCf30cM7kFDXEoC8xpy6fVAqZbw"
genai.configure(api_key=GOOGLE_API_KEY)

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

import re

def get_job_suggestions(skills):
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Create the prompt
    prompt = f"""Based on the following skills: {skills}
    Please suggest 5 suitable job roles and provide a brief description for each.
    Format the response as:
    1. Job Title: Description
    2. Job Title: Description
    etc."""
    
    # Generate the response
    response = model.generate_content(prompt)
    
    # Format the response to ensure each suggestion starts on a new line
    text = response.text.strip()
    # Insert a newline before each numbered item if not already present
    formatted_text = re.sub(r'(?<!\n)(\d+\.)', r'\n\1', text)
    
    # Parse the formatted text into a list of suggestion objects
    suggestions = []
    pattern = re.compile(r'(\d+)\.\s*([^:]+):\s*(.+)')
    for line in formatted_text.split('\n'):
        match = pattern.match(line.strip())
        if match:
            title = match.group(2).strip()
            description = match.group(3).strip()
            suggestions.append({'title': title, 'description': description})
    return suggestions

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

@app.route('/job_match')
def job_match():
    return render_template('job_match.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    skills = request.form.get('skills')
    if not skills:
        return jsonify({'error': 'Please enter at least one skill.'})
    try:
        suggestions = get_job_suggestions(skills)
        # Return the list of suggestion objects
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        return jsonify({'error': str(e)})

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

# New route to serve mock interview page
@app.route('/mock_interview')
def mock_interview():
    return render_template('mock_interview.html')

# New route to handle mock interview form submission

from utils.ai_logic import analyze_answers

@app.route('/mock_interview/submit', methods=['POST'])
def mock_interview_submit():
    data = request.get_json()
    feedback = analyze_answers(data)
    return jsonify({'feedback': feedback})

@app.route('/job_roadmap')
def job_roadmap():
    return render_template('job_roadmap.html')

@app.route('/generate_job_roadmap', methods=['POST'])
def generate_job_roadmap():
    jobs = request.form.get('jobs')
    timeline = request.form.get('timeline')

    if not jobs or not timeline:
        return jsonify({'error': 'Please provide both job(s) and timeline.'}), 400

    prompt = f"""Create a detailed roadmap for becoming a {jobs} within {timeline}. 
    Include key skills, milestones, and suggested learning resources."""

    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        roadmap_text = response.text.strip()
        # Remove markdown bold and heading syntax
        cleaned_text = roadmap_text.replace('**', '').replace('##', '')
        return jsonify({'roadmap': cleaned_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)