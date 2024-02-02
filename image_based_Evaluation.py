import spacy
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import google.generativeai as genai
import docx2txt
from PIL import Image
import PIL

import fitz
 
GEMINI_API = "AIzaSyCtQ914aymvoEhR07yzd9wB0EnkGBCK8JY"

pdf_paths = [
    r'test_data/biology_1_teacher_answer.pdf',
    r'test_data/Answer1.pdf',
# Add more paths as needed
]

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



def pdf2img(pdf_path):
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
        combined_image.save("temp.jpeg","JPEG")

    except Exception as e:
            print(f"Error during image conversion detection: {str(e)}")


def evaluation_script(expectedAnswerpaths,studentAnswerpath,question,max_marks):
    extracted_text = ""
    try:
                
                pdf2img(expectedAnswerpaths)
                expectedAnswer = PIL.Image.open("temp.jpeg")

                pdf2img(studentAnswerpath)
                studentAnswer = PIL.Image.open("temp.jpeg")    

                genai.configure(api_key=GEMINI_API)
                model_vision = genai.GenerativeModel('gemini-pro-vision')

                response =  model_vision.generate_content([f"The images below are the Expected answer and the student given answer for the question : {question} and the expected answer is {expectedAnswer}, please Evaluate them and give the marksout of {max_marks}, just give me the mark no explanition or sorry mssage required",studentAnswer])
         
                awarded_marks = response.text

                
                print("The marks awarded is : "+awarded_marks)

    except Exception as e:
            print(f"Error during evaluation : {str(e)}")
  


# Replace 'your_image_paths' with a list of paths to your image files

# Replace 'path/to/your/keyfile.json' with the actual path to your Google Cloud service account key JSON file
#credentials_path = '/home/tamil/keys/unused/script-evaluation-a41aac110e2b.json'

#main call for detecting the handwriting via the Google.vesion
#batch_detect_handwriting(image_paths, credentials_path)
    
    #Theory normal paper
#evaluate_the_AnswerScript_gemini(image_paths)
max_marks = "10"
question = "Draw and explain the functioning of the human neuron "

evaluation_script(pdf_paths[0],pdf_paths[1],question,max_marks)



