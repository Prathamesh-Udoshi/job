from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import traceback
import base64
import requests

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

try:
    # Configure Gemini API
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    logger.error(f"Error during Gemini API initialization: {str(e)}")
    raise

def generate_diagram(mermaid_code, output_file):
    """Generate a diagram from Mermaid code and save it as an image."""
    try:
        encoded_code = base64.b64encode(mermaid_code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded_code}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            logger.info(f"Diagram saved as {output_file}")
            return True
        else:
            logger.error(f"Error generating diagram: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error in diagram generation: {str(e)}")
        return False

def parse_ai_response(text):
    """Parse the AI response to extract sections and content."""
    sections = {}
    current_section = None
    for line in text.split('\\n'):
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit() and '.' in line or line.endswith(':'):
            current_section = line.split('.', 1)[-1].split(':', 1)[0].strip()
            sections[current_section] = []
        elif current_section and line.startswith('-'):
            sections[current_section].append(line[1:].strip())
    return sections

def create_dynamic_diagram(title, content_sections):
    """Create a Mermaid flowchart diagram based on AI response content."""
    nodes = []
    connections = []
    styles = []

    nodes.append(f'Root["{title}"]')

    # Create a linear flow from section to section
    previous_id = 'Root'
    for i, (section, items) in enumerate(content_sections.items(), 1):
        section_id = f'Section{i}'
        nodes.append(f'{section_id}["{section}"]')
        connections.append(f'{previous_id} --> {section_id}')
        styles.append(f'class {section_id} section')
        previous_id = section_id

        # Add items as subnodes connected to the section
        for j, item in enumerate(items, 1):
            item_id = f'Item{i}_{j}'
            nodes.append(f'{item_id}["{item}"]')
            connections.append(f'{section_id} --> {item_id}')
            styles.append(f'class {item_id} topic')

    mermaid_code = f"""
    flowchart TD
        %% Nodes
        {'\\n        '.join(nodes)}

        %% Connections
        {'\\n        '.join(connections)}

        %% Styling
        classDef root fill:#f9f,stroke:#333,stroke-width:2px
        classDef section fill:#bbf,stroke:#333,stroke-width:2px
        classDef topic fill:#bfb,stroke:#333,stroke-width:2px

        class Root root
        {'\\n        '.join(styles)}
    """
    return mermaid_code

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_job_roadmap', methods=['POST'])
def generate_job_roadmap():
    try:
        jobs = request.form.get('jobs')
        timeline = request.form.get('timeline')
        if not jobs or not timeline:
            return jsonify({'error': 'Please provide both jobs and timeline'}), 400

        prompt = f"""
        Create a detailed career roadmap for the job(s): {jobs} that can be achieved in {timeline}.
        Include clear sections with descriptions and steps to follow:
        1. Required Skills
        2. Practical Projects
        3. Career Progression Steps
        4. Additional Tips
        Format the response with numbered sections and bullet points.
        """

        response = model.generate_content(prompt)
        cleaned_text = response.text.replace('*', '').replace('#', '')
        sections = parse_ai_response(cleaned_text)
        title = f"Career Roadmap for {jobs}"
        mermaid_code = create_dynamic_diagram(title, sections)

        os.makedirs('static/diagrams', exist_ok=True)
        diagram_path = 'static/diagrams/job_roadmap.png'
        success = generate_diagram(mermaid_code, diagram_path)
        if not success:
            logger.error("Failed to generate the Mermaid diagram image.")

        return jsonify({
            'roadmap': cleaned_text,
            'diagram': diagram_path if success else None,
            'diagram_generation_success': success
        })

    except Exception as e:
        logger.error(f"Error in generate_job_roadmap: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)