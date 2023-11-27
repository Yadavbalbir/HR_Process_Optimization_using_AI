from django.shortcuts import redirect, render
from PyPDF2 import PdfReader
import os
from hpo import settings
import ast
from openai import OpenAI
client = OpenAI(
    api_key=""
)

def index(request):
    return render(request, "index.html")

def get_prompt(jd, job_title, resume):
    print("################################################################")
    print("Generating prompt...")
    print("################################################################")
    prompt = '''
    Job Title: {}
    Job Description: {}
    candidates Resume: {}

    Scoring Criteria:
    Evaluate each resume based on the following criteria and assign a score on a scale of 1 to 10, where 1 is the lowest and 10 is the highest.

    Relevance to Job Title:

    To what extent does the resume align with the specified job title?
    Score: [ ]
    Professional Experience:

    Evaluate the candidate's professional experience in relation to the job requirements.
    Score: [ ]
    Educational Background:

    Consider the candidate's education and how well it matches the job requirements.
    Score: [ ]
    Key Skills:

    Assess the presence of key skills relevant to the job description.
    Score: [ ]
    Achievements and Accomplishments:

    Review the candidate's achievements and accomplishments.
    Score: [ ]
    Clarity and Organization:

    Evaluate the overall clarity and organization of the resume.
    Score: [ ]
    Relevant Certifications:

    Check for any relevant certifications that add value to the candidate's profile.
    Score: [ ]
    Additional Information:

    Consider any additional information provided in the resume.
    Score: [ ]
    Overall Score: [ ]

    return json which contains candiate name and overall score
    '''.format(job_title, jd, resume)

    return prompt

def demo(request):
    if request.method == 'POST':
    # Process each uploaded file
        job_title = request.POST.get('job_title')
        jd = request.POST.get('jd')
        resume_content = []
        shortlisted = []
        for uploaded_file in request.FILES.getlist('resumes'):
            resume_content.append(handle_uploaded_file(uploaded_file))
        # Add your logic for resume processing here
        # ...
        i = 0
        for resume in resume_content:
            prompt = get_prompt(jd, job_title, resume)
            print("################################################################")
            print("Prompt Generated successfully for candidate "+ str(1))
            i += 1
            print("################################################################")

            print("Now Using LLM for score calculation...")
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Evaluate resume for a given job position based on the given job description. Use a scale of 1 to 10 for each criterion, where 1 is the lowest and 10 is the highest. Give candidate_name, department, cpi and his overall_score as your response, use only these variables strictly. don't include anything else in your response"},
                {"role": "user", "content": prompt }
            ]
            )

            message = completion.choices[0].message
            candidate = ast.literal_eval(message.content)
            shortlisted.append(candidate)
            print(candidate, type(candidate))
        print(shortlisted)
        context = {
            "shortlisted": shortlisted,
            "job_title": job_title,
            "jd": jd
        }
        return render(request, "results.html", context)  # Redirect to a success page
    return render(request, "demo.html")


def handle_uploaded_file(file):
    with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # Example: Save the file to a specific location
    # Read the PDF content
    pdf_reader = PdfReader(file)
    pdf_text = ''
    for page_number in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_number].extract_text()
    return pdf_text