
from werkzeug.utils import secure_filename
from app import app, db, storage_client
from app.forms import EvalForm, AnswerScriptForm
import os

from fastapi import FastAPI, Request, Depends, File, UploadFile, Form, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse

templates = Jinja2Templates(directory= r"app\templates")

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_nested_collections(main_collection, sub_collection):
    main_collection_ref = db.collection(main_collection)
    sub_collection_ref = main_collection_ref.document(sub_collection).collection('files')
    return sub_collection_ref

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        'add_eval.html',
        {'request': request}
    )

@app.post('/add_eval')
async def add_eval(exam_type : str = Form(...), subject_id: str = Form(...), evaluation_scheme: UploadFile = File(...)):
    # Process the form data here
    # return {"exam_type" : exam_type, "subject_id": subject_id, "evaluation_scheme": evaluation_scheme.filename}
    
    # Create a collection hierarchy
    ganglia_grade_ref = db.collection('GangliaGrade')
    exam_type_ref = ganglia_grade_ref.document(exam_type)
    subjects_ref = exam_type_ref.collection('subjects')
    subject_ref = subjects_ref.document(subject_id)

    # Upload the evaluation scheme tp Firebase Storage
    evaluation_scheme_file = evaluation_scheme.file
    evaluation_scheme_filename = secure_filename(evaluation_scheme.filename)
    evaluation_scheme_blob = storage_client.bucket().blob(f'{exam_type}/{subject_id}/{evaluation_scheme_filename}')
    evaluation_scheme_blob.upload_from_string(evaluation_scheme_file.read(), content_type=evaluation_scheme.content_type)

    # Get the URL of the uploaded file from Firebase Storage
    evaluation_scheme_url = evaluation_scheme_blob.public_url

    # Store the evaluation scheme URL directly inside the id document
    subject_ref.set({
        'subject_id' : subject_id,
        'evaluation_scheme' : evaluation_scheme_url
    })
    response = JSONResponse(content={"message": "Evaluation scheme added successfully!"})
    response.set_cookie(key="message", value="Evaluation scheme added successfully!")

    return RedirectResponse(url="/add_answer_script", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/add_answer_script', response_class=HTMLResponse)
def add_answer_script(request: Request):
    form_data = {
            'exam_type': 'your_exam_type',
            'subject_id': 'your_subject_id',
            'student_id': 'your_student_id',
            'answer_script_file': UploadFile(None),  
        }

    form_answer_script = AnswerScriptForm(**form_data)
    return templates.TemplateResponse(
        'add_answer_script.html',
        {'request': request,
        'form_answer_script': form_answer_script}
    )

@app.post('/add_answer_script')
def add_answer_script(exam_type: str = Form(...), subject_id: str = Form(...), student_id: str = Form(...), answer_script_file: UploadFile = File(...)):

    # return {"exam_type": exam_type, "subject_id": subject_id, "student_id": student_id, "answer_script_file": answer_script_file.filename}

    # Create a collection hierarchy
    ganglia_grade_ref = db.collection('GangliaGrade1')
    exam_type_ref = ganglia_grade_ref.document(exam_type)
    subjects_ref = exam_type_ref.collection('subjects')
    subject_ref = subjects_ref.document(subject_id)
    students_ref = subject_ref.collection('students')
    student_ref = students_ref.document(student_id)

    ganglia_grade_ref = db.collection('GangliaGrade1')
    exam_type_ref = ganglia_grade_ref.document(exam_type)
    subject_ref = exam_type_ref.collection(subject_id)
    student_ref = subject_ref.document(student_id)

    # Upload the answer script to Firebase Storage

    answer_script_file_n = answer_script_file.file
    if answer_script_file_n and allowed_file(answer_script_file.filename):
        answer_script_filename = secure_filename(answer_script_file.filename)
        answer_script_blob = storage_client.bucket().blob(f'{exam_type}/{subject_id}/{student_id}/{answer_script_filename}')
        answer_script_blob.upload_from_string(answer_script_file_n.read(), content_type= answer_script_file.content_type)

        # Get the URL of the uploaded file from Firebase Storage
        answer_script_url = answer_script_blob.public_url

        # Store the Answer Script URL directly inside the student_id document
        student_ref.set({
            'student_id': student_id,
            'answer_script_url': answer_script_url
        })

        response = JSONResponse(content={"message": "Evaluation scheme added successfully!"})
        response.set_cookie(key="message", value="Evaluation scheme added successfully!")

        return RedirectResponse(url = '/', status_code=status.HTTP_303_SEE_OTHER)
