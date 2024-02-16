from typing_extensions import Unpack
from fastapi import Form, UploadFile
from pydantic import BaseModel, ConfigDict

class EvalForm(BaseModel):
    exam_type: str
    subject_id: str
    evaluation_scheme: UploadFile

class AnswerScriptForm(BaseModel):
    exam_type: str
    subject_id: str
    student_id: str
    answer_script_file: UploadFile

