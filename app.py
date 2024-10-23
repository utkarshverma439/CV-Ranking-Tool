import os
import re
from flask import Flask, request, render_template
from groq import Groq
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Functions from your original code
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text).strip()

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r') as file:
        return file.read().strip()

def load_data(cv_files):
    cvs = {}
    for file in cv_files:
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        else:
            return None, f"Unsupported file format: {file.filename}"
        cvs[file.filename] = text
    return cvs, None

def rank_cv_sections(cv_text, job_description):
    prompt = f"Rank the sections of this CV based on their relevance to the following job description:\n\nCV:\n{cv_text}\n\nJob Description:\n{job_description}\n\nProvide a ranked list of CV sections and relevancy scores (0-1)."
    
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    response = completion.choices[0].message.content
    ranked_sections = []
    pattern = r'(\d+)\.\s*\*\*(.*?)\*\*\s*\((\d\.\d)\)'
    
    for match in re.finditer(pattern, response):
        section_name = match.group(2).strip()
        score = float(match.group(3))
        ranked_sections.append({'section': section_name, 'score': score})
    
    return ranked_sections

def rank_multiple_cvs(cvs, job_description):
    overall_scores = {}
    
    for cv_id, cv in cvs.items():
        ranked_sections = rank_cv_sections(cv, job_description)
        
        if ranked_sections:
            overall_score = sum(section['score'] for section in ranked_sections) / len(ranked_sections)
            overall_scores[cv_id] = overall_score * 100
        else:
            overall_scores[cv_id] = 0
            
    ranked_cvs = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_cvs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form['job_description']
        cv_files = request.files.getlist('cvs')

        if not cv_files or not job_description:
            return render_template('index.html', error='Please provide both CVs and a job description.')

        # Save uploaded files
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        for file in cv_files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        cvs, error = load_data(cv_files)
        if error:
            return render_template('index.html', error=error)

        # Rank the CVs
        overall_cv_rankings = rank_multiple_cvs(cvs, job_description)

        return render_template('results.html', rankings=overall_cv_rankings)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
