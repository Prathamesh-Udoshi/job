import PyPDF2
import re

def parse_resume(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        # Normalize text to lowercase and remove special characters
        text = re.sub(r'[^\w\s]', '', text.lower())

        # Define a more extensive set of skills across domains
        keywords = [
    'python', 'java', 'c++', 'html', 'css', 'javascript', 'sql', 'excel',
    'powerpoint', 'flask', 'django', 'react', 'nodejs', 'aws', 'azure',
    'ml', 'machine learning', 'data science', 'nlp', 'deep learning',
    'flutter', 'android', 'git', 'figma', 'photoshop', 'illustrator',
    'public speaking', 'leadership', 'communication', 'marketing',
    'sales', 'content writing', 'business analysis', 'graphic design', 
    'content creation', 'community outreach', 'project management', 
    'digital marketing', 'data visualization', 'cloud computing', 
    'video editing', 'salesforce', 'business process automation', 
    'enterprise resource planning', 'chatbot development', 'cybersecurity', 
    'finance', 'nursing', 'teaching', 'retail', 'e-commerce', 'photography', 
    'transportation', 'hospitality', 'agriculture', 'data entry', 
    'customer service', 'telecommunication', 'public relations', 'law', 
    'event management', 'architecture', 'fashion design', 'electrician', 
    'plumbing', 'carpentry', 'psychology'
]



        found_skills = [skill for skill in keywords if skill in text]

        return ', '.join(sorted(set(found_skills))) if found_skills else "No key skills found"

    except Exception as e:
        print("[Resume Parsing Error]:", e)
        return "Resume could not be parsed"
