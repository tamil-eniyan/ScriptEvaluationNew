from fastapi import APIRouter,File,UploadFile
import random
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import fitz
import google.generativeai as genai
import tempfile
import os
import shutil
from pathlib import Path
import json


one_api_router = APIRouter()

GEMINI_API = "AIzaSyD-HzbQwUFUN9libpS9NtXvYWVq8ibXCTA"

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 400,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]




def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            file_name = buffer.name
            print(type(file_name))
    finally:
        upload_file.file.close()
    return file_name


def delete_file(filename):
    os.remove(filename)





def pdf2img(pdf_path):
        pdf_document = fitz.open(pdf_path)
        image_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_list.append(page.get_pixmap())

        pdf_document.close()

        images = [
            Image.frombytes("RGB", (image.width, image.height), image.samples)
            for image in image_list
        ]

        # Combine all images vertically
        combined_image = Image.new(
            "RGB", (images[0].width, sum(image.height for image in images))
        )
        offset = 0

        for image in images:
            combined_image.paste(image, (0, offset))
            offset += image.height

        # Save the combined image
        combined_image.save("temp.jpeg", "JPEG")
        

@one_api_router.post("/evaluate_answer")
def evaluate_answer(expectedAnswerpath, studentAnswerpath, question, max_marks):
    extracted_text = ""
    additional_points = ""
    image_string = ""
    try:
        print('[+]evaluating....')
        pdf2img(expectedAnswerpath)
        expectedAnswer = Image.open("temp.jpeg")

        image_string = pdf2img(studentAnswerpath)
        studentAnswer = Image.open("temp.jpeg")
        
        
        genai.configure(api_key=GEMINI_API)
        model_vision = genai.GenerativeModel(
            "gemini-pro-vision", safety_settings=safety_settings
        )

        response = model_vision.generate_content(
            [
                f"The images below are the Expected answer and the student given answer for the question : {question} and the expected answer is {expectedAnswer}, please Evaluate them and give me json file with  the marksout of {max_marks} and the explination why the mark was given(just two key:value pairs marks,explanation),just give me the mark no explanation or sorry message required {additional_points}",
                studentAnswer,
            ]
        )

        text = response.text

      
       
        text = text.split("```")[1]
        text = text.replace("\\n","")
        text = text.replace("json","")
        text = text.replace("\\","")
        text = text.lower()

        print(f"{text}")
        
        return text
    except Exception as e:
        print(f"[-]Error during evaluation : {str(e)}")
        print(expectedAnswerpath)
        print(studentAnswerpath)
        print(question)
        print(max_marks)
        return -1










@one_api_router.post('/evaluate/one')
async def One_Question(question:str , mark: str,ES: UploadFile = File(),AS: UploadFile=File()):
    max_marks = str(mark)
    
    file_one_path = save_upload_file(ES, Path(f"expectedanswer.pdf"))
    file_two_path = save_upload_file(AS, Path(f"studentanswer.pdf"))

    result = evaluate_answer(file_one_path, file_two_path,question,max_marks)
    
    
    #print(f"{file_one_path},,{file_two_path}")
    delete_file(file_one_path)
    delete_file(file_two_path)
    delete_file('temp.jpeg') 
    print('[+] Evaluation complited')
    #return result
    

    json_data=json.dumps(result)


    return {json_data}



























