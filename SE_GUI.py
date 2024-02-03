import spacy
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import google.generativeai as genai
import docx2txt
from PIL import Image
import PIL
import base64
from io import BytesIO
import pandas as pd
import PySimpleGUI as sg
from pathlib import Path

import fitz
 
GEMINI_API = "AIzaSyCtQ914aymvoEhR07yzd9wB0EnkGBCK8JY"

total_marks=0

layout = [[sg.Text("Evaluation Scheme"), sg.Input(key="-ES-"), sg.FileBrowse(file_types=(("Evaluation Scheme", "*.csv"),))],
         [sg.Text("Student Answer"), sg.Input(key="-AS-"), sg.FileBrowse(file_types=(("Student Answer script", "*.csv"),))],
         [sg.Exit(), sg.Button("Evaluate")],]


generation_config = {
        "temperature":0,
        "top_p":1,
        "top_k":1,
        "max_output_tokens":1,
    }

safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]



def pdf2img2string(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        image_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_list.append(page.get_pixmap())

        pdf_document.close()

        images = [Image.frombytes("RGB", (image.width, image.height), image.samples) for image in image_list]

    # Combine all images vertically
        combined_image = Image.new("RGB", (images[0].width, sum(image.height for image in images)))
        offset = 0

        for image in images:
            combined_image.paste(image, (0, offset))
            offset += image.height

    # Save the combined image
        combined_image.save("combinedimage_temp.jpeg","JPEG")
        return(image_to_string("combinedimage_temp.jpeg"))


    except Exception as e:
            print(f"Error during image conversion detection: {str(e)}")


def evaluate_answer(expectedAnswerpath,studentAnswerpath,question,max_marks,qid):
    extracted_text = ""
    additional_points = ""
    image_string = ""
    try:
                
                image_string = pdf2img2string(expectedAnswerpath)
                string_to_image(image_string)
                expectedAnswer = PIL.Image.open("temp.jpeg")

                image_string = pdf2img2string(studentAnswerpath)
                string_to_image(image_string)
                studentAnswer = PIL.Image.open("temp.jpeg")

               


                genai.configure(api_key=GEMINI_API)
                model_vision = genai.GenerativeModel('gemini-pro-vision',safety_settings=safety_settings)

                response =  model_vision.generate_content([f"The images below are the Expected answer and the student given answer for the question : {question} and the expected answer is {expectedAnswer}, please Evaluate them and give the marksout of {max_marks},just give me the mark no explanation or sorry message required {additional_points}",studentAnswer])
         
                awarded_marks = response.text

                
                print(f"The marks awarded for question {qid} is : {awarded_marks}")
                return awarded_marks
    except Exception as e:
        print(f"Error during evaluation : {str(e)}")
        print(expectedAnswerpath)
        print(studentAnswerpath)
        print(question)
        print(max_marks)
        print(qid)
        return -1
  



def image_to_string(image_path):
    with open(image_path, "rb") as image_file:
        # Read binary data
        binary_data = image_file.read()
        # Encode binary data to base64
        encoded_data = base64.b64encode(binary_data)
        # Convert bytes to string
        image_string = encoded_data.decode("utf-8")
    return image_string


def string_to_image(image_string):
    # Decode base64 string to binary data
    binary_data = base64.b64decode(image_string)

    # Convert binary data to PIL Image
    image = Image.open(BytesIO(binary_data))

    # Save the image to the specified output path
    image.save("temp.jpeg")










def input_fun(es_path,student_answerscripts_path):
    #student_answerscripts_path = input("Enter the path of the StudentAnswer scripts : ")
    
    print("[+]Evaluating the Questions.....")
    evaluationscheme_dataframe = pd.read_csv (es_path)
    total_marks = 0
    
    studentanswerscripts_dataframe = pd.read_csv (student_answerscripts_path)
    #print(studentanswerscripts_dataframe)
    
    for index ,  rows in studentanswerscripts_dataframe.iterrows():

        #print(rows)                       
        temp = evaluationscheme_dataframe[evaluationscheme_dataframe["Qid"] == rows.Qid]
        
        

        temp_ES_path = temp.Expected_answer_pdf_path.to_numpy()[0]
        temp_AS_path = rows.path
        temp_question = temp.Question.to_numpy()[0]
        temp_max_marks = str(temp.Max_Marks.to_numpy()[0])
        temp_Qid = str(temp.Qid.to_numpy()[0])
            
        total_marks += int(evaluate_answer(temp_ES_path,temp_AS_path,temp_question,temp_max_marks,temp_Qid))
        
    print("[+]Evaluation Completed sucessfully :) ")

    print(f"The total marks is {total_marks}")
    sg.popup_no_titlebar(f"The Total Marks is {total_marks}")

#***************************************************Driver Function********************************************************************


window = sg.Window("Answer Script Evaluation", layout)

while True:
    event,  values = window.read()
    
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Evaluate":

        input_fun(
                es_path=values["-ES-"],
                student_answerscripts_path=values["-AS-"],)            


window.close()









