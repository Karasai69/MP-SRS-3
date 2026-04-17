from PyPDF2 import PdfReader

# 📄 Извлечение текста из PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# 📊 Кастомный скоринг (сравнение)
def score_resume(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    common = resume_words.intersection(job_words)
    score = len(common) / (len(job_words) + 1)

    return score, list(common)
