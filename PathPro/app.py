from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the skill extraction model or fall back to a basic NER model
try:
    # Load a model capable of extracting skills or job-related entities
    skill_extractor = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
except Exception as e:
    print(f"Error loading the specified model: {e}")
    print("Using a fallback model for demonstration purposes.")
    # Fall back to a basic NER model if the desired one fails
    skill_extractor = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)

# Define data for subjects and job roles
subjects = {
    'Computer Science': ['Software Developer', 'Data Scientist', 'AI Engineer'],
    'Mechanical Engineering': ['Mechanical Engineer', 'Design Engineer', 'Project Manager'],
    'Business': ['Business Analyst', 'Marketing Specialist', 'Operations Manager'],
}

job_roles = {
    'Software Developer': {
        'skills': ['Python', 'JavaScript', 'SQL', 'Algorithms'],
        'description': 'A software developer writes and tests code that allows programs to function.'
    },
    'Data Scientist': {
        'skills': ['Python', 'Machine Learning', 'Statistics', 'Data Visualization'],
        'description': 'Data scientists analyze large sets of data and extract actionable insights.'
    },
    'AI Engineer': {
        'skills': ['Python', 'Deep Learning', 'Neural Networks', 'TensorFlow'],
        'description': 'AI engineers build and deploy AI models for various applications.'
    },
    'Mechanical Engineer': {
        'skills': ['CAD', 'Mechanics', 'Thermodynamics', 'Manufacturing'],
        'description': 'Mechanical engineers design, analyze, and manufacture mechanical systems.'
    },
    'Design Engineer': {
        'skills': ['AutoCAD', 'SolidWorks', 'Problem-Solving', 'Creativity'],
        'description': 'Design engineers create and develop plans for mechanical products.'
    },
    'Project Manager': {
        'skills': ['Leadership', 'Project Planning', 'Risk Management', 'Communication'],
        'description': 'Project managers oversee projects and ensure they are completed on time and within budget.'
    },
    'Business Analyst': {
        'skills': ['Data Analysis', 'Communication', 'Business Modeling', 'Problem Solving'],
        'description': 'Business analysts help businesses improve by analyzing data and processes.'
    },
    'Marketing Specialist': {
        'skills': ['SEO', 'Content Marketing', 'Market Research', 'Digital Advertising'],
        'description': 'Marketing specialists develop strategies to promote products and services.'
    },
    'Operations Manager': {
        'skills': ['Process Optimization', 'Team Management', 'Logistics', 'Supply Chain Management'],
        'description': 'Operations managers oversee day-to-day activities to ensure efficiency in business operations.'
    }
}

@app.route('/')
def index():
    return render_template('index.html', subjects=subjects)

@app.route('/view_jobs', methods=['POST'])
def view_jobs():
    selected_subject = request.form.get('subject')
    roles = subjects.get(selected_subject, [])
    return render_template('index.html', subjects=subjects, roles=roles, selected_subject=selected_subject)

@app.route('/job_details/<role>')
def job_details(role):
    job_info = job_roles.get(role)
    return render_template('job_details.html', job_info=job_info, role=role)

# Updated route for AI chat using skill extraction with enhanced error handling
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    try:
        # Extract skills or job-related entities from the user input
        extracted_data = skill_extractor(user_input)

        # Ensure extracted_data is not empty or malformed
        if not extracted_data or 'entity_group' not in extracted_data[0]:
            response = "I couldn't extract relevant information from your input. Could you please rephrase?"
        else:
            # Handle case where model returns named entities
            extracted_skills = [item['word'] for item in extracted_data if item['entity_group'] in ['MISC', 'ORG']]

            # Process the extracted skills or job roles
            if extracted_skills:
                # Check if extracted skill matches a job role in our predefined list
                matching_roles = []
                for skill in extracted_skills:
                    for role, details in job_roles.items():
                        if skill in details['skills']:
                            matching_roles.append(role)

                if matching_roles:
                    # If a match is found, return job role details
                    role_info = {role: job_roles[role] for role in matching_roles}
                    response = f"Here are some roles matching your input: {', '.join(matching_roles)}"
                else:
                    response = f"Extracted skills: {', '.join(extracted_skills)}"
            else:
                response = "No skills or roles were identified in the input."
    except Exception as e:
        response = f"Error processing the input: {e}"

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
