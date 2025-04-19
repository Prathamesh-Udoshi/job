#from google.cloud import aiplatform

# Enhanced skill-to-career role mapping
skill_to_roles = {
    "python": ["Backend Developer", "Data Analyst", "Automation Engineer", "Quality Analyst"],
    "java": ["Java Developer", "Android Developer", "Backend Developer", "Software Engineer"],
    "javascript": ["Frontend Developer", "Web Developer", "React Developer", "Node.js Developer"],
    "html": ["Frontend Developer", "Web Designer", "UI Designer", "Web Developer"],
    "css": ["Frontend Developer", "UI Designer", "Web Designer", "UX/UI Developer"],
    "sql": ["Data Analyst", "Database Administrator", "Business Intelligence Analyst", "ETL Developer"],
    "c++": ["Embedded Systems Engineer", "Game Developer", "Software Engineer", "C++ Developer"],
    "android": ["Android Developer", "Mobile App Developer", "Java Developer", "Mobile UI Designer"],
    "flutter": ["Mobile App Developer", "Cross-Platform App Developer", "UI Developer", "App Developer"],
    "react": ["Frontend Developer", "UI Developer", "React Developer", "Web Developer"],
    "nodejs": ["Full Stack Developer", "Backend Developer", "API Developer", "JavaScript Developer"],
    "aws": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect", "AWS Consultant"],
    "cybersecurity": ["Security Analyst", "Ethical Hacker", "Cybersecurity Consultant", "Penetration Tester"],
    "excel": ["Data Analyst", "Business Analyst", "Operations Analyst", "Financial Analyst"],
    "marketing": ["Digital Marketing Specialist", "Content Marketing Specialist", "SEO Specialist", "PPC Specialist"],
    "business analysis": ["Business Analyst", "Product Manager", "Systems Analyst", "Operations Manager"],
    "graphic design": ["Graphic Designer", "UI/UX Designer", "Web Designer", "Visual Designer"],
    "content writing": ["Content Writer", "SEO Content Writer", "Technical Writer", "Creative Writer"],
    "sales": ["Sales Manager", "Sales Executive", "Business Development Executive", "Account Manager"],
    "hr": ["HR Manager", "Recruitment Specialist", "Employee Relations Manager", "Training and Development Specialist"],
    "finance": ["Financial Analyst", "Accountant", "Investment Consultant", "Financial Planner"],
    "psychology": ["Clinical Psychologist", "Counseling Psychologist", "School Counselor", "Industrial Psychologist"],
    "architecture": ["Architect", "Urban Planner", "Interior Designer", "Landscape Architect"],
    "fashion design": ["Fashion Designer", "Textile Designer", "Costume Designer", "Fashion Merchandiser"],
    "electrician": ["Electrician", "Electrical Technician", "Installation Specialist", "Maintenance Engineer"],
    "plumbing": ["Plumber", "Plumbing Technician", "Water Systems Specialist", "Maintenance Worker"],
    "carpentry": ["Carpenter", "Woodworking Specialist", "Furniture Designer", "Construction Worker"],
    "nursing": ["Registered Nurse", "Healthcare Assistant", "Clinical Nurse", "Health Educator"],
    "teaching": ["School Teacher", "Private Tutor", "Teaching Assistant", "Subject Matter Expert"],
    "retail": ["Retail Manager", "Store Supervisor", "Sales Representative", "Customer Support Specialist"],
    "e-commerce": ["E-commerce Specialist", "Customer Service Representative", "Product Manager", "Logistics Manager"],
    "photography": ["Photographer", "Videographer", "Photo Editor", "Freelance Photographer"],
    "transportation": ["Truck Driver", "Delivery Driver", "Logistics Coordinator", "Supply Chain Manager"],
    "hospitality": ["Hotel Manager", "Restaurant Manager", "Event Planner", "Travel Coordinator"],
    "agriculture": ["Agricultural Technician", "Farm Manager", "Horticulturist", "Agricultural Advisor"],
    "data entry": ["Data Entry Operator", "Data Analyst", "Clerk", "Office Assistant"],
    "customer service": ["Customer Service Representative", "Customer Support Executive", "Help Desk Technician"],
    "telecommunication": ["Telecom Engineer", "Field Technician", "Network Engineer", "Telecom Consultant"],
    "public relations": ["PR Specialist", "Media Manager", "Communications Officer", "Event Coordinator"],
    "law": ["Lawyer", "Legal Assistant", "Paralegal", "Compliance Officer"],
    "event management": ["Event Coordinator", "Event Planner", "Logistics Manager", "Venue Manager"],
    "content creation": ["YouTuber", "Social Media Influencer", "Content Creator", "Video Editor"],
    "community outreach": ["Community Coordinator", "Outreach Specialist", "NGO Worker", "Social Worker"],
    "project management": ["Project Manager", "Program Manager", "Scrum Master", "Project Coordinator"],
    "digital marketing": ["SEO Specialist", "Content Marketing Manager", "Social Media Manager", "E-commerce Marketing Specialist"],
    "data visualization": ["Data Analyst", "Business Intelligence Developer", "Data Visualization Specialist", "BI Analyst"],
    "cloud computing": ["Cloud Engineer", "Cloud Solutions Architect", "Cloud Consultant", "Cloud Developer"],
    "video editing": ["Video Editor", "Content Creator", "Social Media Manager", "YouTuber"],
    "salesforce": ["Salesforce Developer", "Salesforce Administrator", "CRM Specialist", "Salesforce Consultant"],
    "business process automation": ["BPA Specialist", "Automation Engineer", "Robotics Process Automation Developer", "Software Engineer"],
    "enterprise resource planning": ["ERP Consultant", "ERP Analyst", "ERP Developer", "Business Systems Analyst"],
    "chatbot development": ["Chatbot Developer", "AI Developer", "Conversational Designer", "UX Designer for Chatbots"],
}



def suggest_careers(skills):
    # Normalize input
    skills_list = [skill.strip().lower() for skill in skills.split(',')]
    suggested_roles = set()

    for skill in skills_list:
        roles = skill_to_roles.get(skill)
        if roles:
            # Add roles for each skill, limit to first 5
            suggested_roles.update(roles[:4])

    # Fallback (if no role matched)
    if not suggested_roles:
        suggested_roles.add("Sorry could not find suitable career roles based on the provided skills. Please try with different skills. Example: Python, SQL, Java")

    return list(suggested_roles)

# Example usage
skills_input = "Python, SQL, Java"
career_suggestions = suggest_careers(skills_input)

# Print career suggestions for the given skills
print(career_suggestions)
