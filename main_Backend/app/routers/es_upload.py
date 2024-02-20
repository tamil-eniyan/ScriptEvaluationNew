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
import pyrebase


es_upload_router = APIRouter()

try:

    cred =  {
        "apiKey": "AIzaSyAcNkl3QXy0L_OWmMlxGNSEHar0YZddP_Q",
        "authDomain": "scriptevaluation.firebaseapp.com",
        "projectId": "scriptevaluation",
        "storageBucket": "scriptevaluation.appspot.com",
        "messagingSenderId": "955685431488",
        "appId": "1:955685431488:web:41c163453fa74cfad1a525",
        "measurementId": "G-1M4P9LFB0V",
        "databaseURL":"https://.firebaseio.com"
        }
    
    
    


    firebase = pyrebase.initialize_app(cred)


except Exception as e:
        print(f"[-]Error during importing of pyrebase at es_upload.py : {str(e)}")
        




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
        filename  = pdf_path.replace('.pdf','')
        # Save the combined image
        combined_image.save(f"{filename}.jpeg", "JPEG")
        return filename








def uploadfile_main(exam_id,subject_id,es_PDFpath, qid, question, max_marks):
    extracted_text = ""
    additional_points = ""
    image_string = ""
    try:
        print('[+]uploading...')

        filename = pdf2img(es_PDFpath)
        es_JPEGpath = Image.open(f"expectedanswer.jpeg")
        
        
        storage = firebase.storage()

        
        path_on_cloud_PDF = f"main_ES/{exam_id}/{subject_id}/{qid}/expectedanswer.pdf"
        path_local_PDF = "expectedanswer.pdf"

        path_on_cloud_JPEG = f"main_ES/{exam_id}/{subject_id}/{qid}/expectedanswer.jpeg"
        path_local_JPEG = "expectedanswer.jpeg"

        #storing in the cloud
        storage.child(path_on_cloud_PDF).put(path_local_PDF)
        storage.child(path_on_cloud_JPEG).put(path_local_JPEG)
        
        
        print("[+]finished uploading") 
        
        
        return 1
    except Exception as e:
        print(f"[-]Error during evaluation : {str(e)}")
        return -1










@es_upload_router.put('/evaluate/esupload')
async def ES_upload(exam_id:str,subject_id:str,question:str , mark: int,q_id:str,ES: UploadFile = File()):
    max_marks = str(mark)
    
    file_one_path = save_upload_file(ES, Path(f"expectedanswer.pdf"))
    

    result_jpeg_path = uploadfile_main(exam_id,subject_id,file_one_path,q_id,question,max_marks)
    
    
    #print(f"{file_one_path},,{file_two_path}")
    delete_file(file_one_path)
    delete_file("expectedanswer.jpeg")
    
    
    
    #return result
    

    #json_data=json.dumps(result)

    
    return {"data":"[+]uploaded"}








