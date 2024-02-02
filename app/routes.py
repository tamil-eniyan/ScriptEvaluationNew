# app/routes.py

from flask import render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from app import app, db, storage_client
from app.forms import EvalForm
import os

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_nested_collections(main_collection, sub_collection):
    main_collection_ref = db.collection(main_collection)
    sub_collection_ref = main_collection_ref.document(sub_collection).collection('files')
    return sub_collection_ref

@app.route('/')
def index():
    return render_template('add_eval.html', form=EvalForm())

@app.route('/add_eval', methods=['POST'])
def add_eval():
    form_eval = EvalForm()

    if form_eval.validate_on_submit():
        exam_type = form_eval.exam_type.data
        subject_id = form_eval.subject_id.data
    
        # Create a collection hierarchy
        ganglia_grade_ref = db.collection('GangliaGrade')
        exam_type_ref = ganglia_grade_ref.document(exam_type)
        subjects_ref = exam_type_ref.collection('subjects')
        subject_ref = subjects_ref.document(subject_id)
    
        # Upload the evaluation scheme to Firebase Storage
        evaluation_scheme_file = form_eval.evaluation_scheme_csv.data
        evaluation_scheme_filename = secure_filename(evaluation_scheme_file.filename)
        evaluation_scheme_blob = storage_client.bucket().blob(f'{exam_type}/{subject_id}/{evaluation_scheme_filename}')
        evaluation_scheme_blob.upload_from_string(evaluation_scheme_file.read(), content_type=evaluation_scheme_file.content_type)
    
        # Get the URL of the uploaded file from Firebase Storage
        evaluation_scheme_url = evaluation_scheme_blob.public_url
    
        # Store the evaluation scheme URL directly inside the subject_id document
        subject_ref.set({
            'subject_id': subject_id,
            'evaluation_scheme_url': evaluation_scheme_url
        })
    
        flash('Evaluation scheme added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_eval.html', form_eval=form_eval)





# import spacy
# from google.cloud import vision
# from google.oauth2 import service_account
# from flask import render_template, redirect, url_for, flash, request
# from werkzeug.utils import secure_filename
# from app import app, db, storage_client
# import os
# import io
# from docx import Document
# import fitz
# from app.forms import SubjectForm, StudentForm, EvalForm

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}
# GOOGLE_VISION_CREDENTIALS_PATH = "F:\Ganglia\ScriptEvaluationNeWW\ScriptEvaluationNew\google_vision_cred.json"
# FIREBASE_CREDENTIALS_PATH = "F:\Ganglia\ScriptEvaluationNeWW\ScriptEvaluationNew\firebase_cred.json"

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def convert_pdf_to_text(pdf_data):
#     text = ""
#     with fitz.open("pdf", pdf_data) as pdf_document:
#         for page_number in range(pdf_document.page_count):
#             page = pdf_document[page_number]
#             text += page.get_text()
#     return text

# def convert_docx_to_text(docx_data):
#     doc = Document(io.BytesIO(docx_data))
#     text_content = ""
#     for paragraph in doc.paragraphs:
#         text_content += paragraph.text + '\n'
#     return text_content

# def process_text_into_paragraphs(text):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)

#     paragraphs = []
#     current_paragraph = []

#     for sentence in doc.sents:
#         current_paragraph.append(sentence.text)

#     # Check if the current paragraph is not empty before appending
#     if current_paragraph:
#         paragraphs.append(' '.join(current_paragraph))

#     return paragraphs

# def detect_handwriting(image_content):
#     """Detects handwriting features in an image using Google Cloud Vision API."""
#     # Set up credentials explicitly
#     credentials_path = GOOGLE_VISION_CREDENTIALS_PATH
#     credentials = service_account.Credentials.from_service_account_file(credentials_path)
#     client = vision.ImageAnnotatorClient(credentials=credentials)

#     # Create a Vision API image object
#     image = vision.Image(content=image_content)

#     try:
#         # Perform document text detection
#         response = client.document_text_detection(image=image)

#         # Extract and return the text
#         return response.full_text_annotation.text

#     except Exception as e:
#         print(f"Error during document text detection: {str(e)}")
#         return None

# @app.route('/')
# def index():
#     subjects = db.collection('subjects').stream()
#     return render_template('add_subject.html', subjects=subjects, form_subject=SubjectForm(), form_student=StudentForm())

# @app.route('/add_subject', methods=['POST'])
# def add_subject():
#     form_subject = SubjectForm()

#     if form_subject.validate_on_submit():
#         subject_data = {
#             'subject_id': form_subject.subject_id.data,
#             'name': form_subject.subject_name.data
#         }

#         # Upload the evaluation scheme to Firebase Storage under 'EvalScheme' folder
#         evaluation_scheme_file = form_subject.evaluation_scheme.data
#         evaluation_scheme_filename = secure_filename(evaluation_scheme_file.filename)
#         evaluation_scheme_blob = storage_client.bucket().blob(f'EvalScheme/{evaluation_scheme_filename}')
#         evaluation_scheme_blob.upload_from_string(evaluation_scheme_file.read(), content_type=evaluation_scheme_file.content_type)

#         # Get the URL of the uploaded file from Firebase Storage
#         evaluation_scheme_url = evaluation_scheme_blob.public_url

#          # Convert the file to text based on the file extension
#         if evaluation_scheme_filename.lower().endswith('.pdf'):
#             # Download the PDF file as binary data
#             pdf_data = evaluation_scheme_blob.download_as_bytes()
#             # Convert the PDF file to text
#             text_content = convert_pdf_to_text(pdf_data)
#         elif evaluation_scheme_filename.lower().endswith('.docx'):
#             # Download the DOCX file as binary data
#             docx_data = evaluation_scheme_blob.download_as_bytes()
#             # Convert the DOCX file to text
#             text_content = convert_docx_to_text(docx_data)
#         else:
#             text_content = "Unsupported file format"

#         # Store the evaluation scheme URL in Firestore
#         # subject_data['evaluation_scheme_url'] = evaluation_scheme_url

#         # Store subject data in Firestore
#         subject_data['evaluation_scheme_text'] = text_content
#         db.collection('subjects').document(form_subject.subject_id.data).set(subject_data)

#         flash('Subject added successfully!', 'success')
#         return render_template('add_student.html', form_student=StudentForm(),  success_message='Subject added successfully!')  # Render add_student.html template

#     return redirect(url_for('index'))

# @app.route('/add_student', methods=['POST'])
# def add_student():
#     form_student = StudentForm()

#     if form_student.validate_on_submit():
#         student_data = {
#             'roll_number': form_student.roll_number.data,
#             'name': form_student.name.data,
#             'sub_name': form_student.sub_name.data
#         }

#         # Upload the answer script to Firebase Storage under 'AnswerScript' folder
#         answer_script_file = form_student.answer_script.data
#         answer_script_filename = secure_filename(answer_script_file.filename)
#         answer_script_blob = storage_client.bucket().blob(f'AnswerScript/{answer_script_filename}')
#         answer_script_blob.upload_from_string(answer_script_file.read(), content_type=answer_script_file.content_type)

#         # Get the URL of the uploaded file from Firebase Storage
#         answer_script_url = answer_script_blob.public_url

#         # Store the answer script filename and URL in Firestore
#         student_data['answer_script_filename'] = answer_script_filename
#         student_data['answer_script_url'] = answer_script_url

#         # Download the image content from Firebase Storage
#         answer_script_content = answer_script_blob.download_as_bytes()

#         # Use Google Cloud Vision API to detect handwriting in the answer script
#         extracted_text = detect_handwriting(answer_script_content)

#         if extracted_text:
#             # Store the extracted text in Firestore
#             student_data['answer_script_text'] = extracted_text
#             db.collection('students').document(form_student.roll_number.data).set(student_data)

#             flash('Student added successfully!', 'success')
#         else:
#             flash('Error processing handwriting. Please try again.', 'danger')
        

#     return redirect(url_for('index'))


