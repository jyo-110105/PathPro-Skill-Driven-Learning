# PathPro-Skill-Driven-Learning
The application uses the Hugging Face transformers library to load the dbmdz/bert-large-cased-finetuned-conll03-english model. It will automatically download when the app runs.
app.py: Flask app with the provided Python code.
templates/index.html: Home page for subject selection and job viewing.
templates/job_details.html: Displays job role details (description and required skills).
**Usage**
Home Page:

Select a subject (e.g., Computer Science, Mechanical Engineering).
View job roles associated with the selected subject.
Job Role Details:

Click a job role (e.g., Software Developer) to view its description and required skills.
AI Chat:

Send a message with job-related queries or skills.
The AI will extract skills or job-related entities and provide role suggestions or identified skills.
Subject-Role Mapping:

Users can select a subject and view job roles related to it.
Job Role Details:

Provides detailed job descriptions and required skills for each role.
Skill Extraction:

The chat feature extracts skills or job-related entities from the user’s input using a transformer-based model.
Error Handling:

If skill extraction fails, the system provides meaningful feedback to the user.

**Future Enhancements**

Skill-to-Job Mapping:

Suggest job roles based on specific skills mentioned by the user.
Improved UI/UX:

Enhance user interaction and presentation for job roles and chat responses.
