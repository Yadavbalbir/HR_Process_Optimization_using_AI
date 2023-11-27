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
    job_title: {}
    job_description: {}
    Extract the relevant information from the resume given below like name, department like civil engineering etc, cpi etc.
    candidates_Resume_text: {}

    Please provide scores for the following criteria:
    1. Relevance to Job Title (range 1-10)
    2. Professional Experience (range 1-10)
    3. Educational Background  (range 1-10)
    4. Key Skills (range 1-10)
    5. Achievements and Accomplishments (range 1-10)
    6. Clarity and Organization (range 1-10)
    7. Relevant Certifications (range 1-10)

    Overall Score: (average of above 7 scores)
    return candidate_name, department_name, cpi, overall_score in json format

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
        i = 1
        for resume in resume_content:
            prompt = get_prompt(jd, job_title, resume)
            print("################################################################")
            print("Prompt Generated successfully for candidate "+ str(i))
            i += 1
            print("################################################################")

            print("Now Using LLM for score calculation...")
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Evaluate resume for a given job position based on the given job description. Use a scale of 1 to 10 for each criterion, where 1 is the lowest and 10 is the highest. Give candidate_name, department, cpi and his overall_score as your response, use only these variables strictly. don't include anything else in your response. Don't be too strictly in scoring."},
                {"role": "user", "content": prompt }
            ]
            )
            print("################################################################")
            print("LLM response received successfully")
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