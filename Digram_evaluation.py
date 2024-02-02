import spacy
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import google.generativeai as genai
import docx2txt
import PIL.Image


GEMINI_API = "AIzaSyCtQ914aymvoEhR07yzd9wB0EnkGBCK8JY"

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






def gemini_analysis_digram(expectedAnswer_imagepaths,studentAnswer_imagepath,question,max_marks):
    extracted_text = ""
    try:
                
                expectedAnswer = PIL.Image.open(expectedAnswer_imagepaths)
                studentAnswer = PIL.Image.open(studentAnswer_imagepath)
                genai.configure(api_key=GEMINI_API)
                model_vision = genai.GenerativeModel('gemini-pro-vision', safety_settings=safety_settings)

                response =  model_vision.generate_content([f"The images below are the Expected answer and the student given answer for the question below {question} , please Evaluste them and give the marksout of {max_marks}, Give me only the mark that too only a number, no other explanation or suggestion or sorry message or any alternatives",expectedAnswer,studentAnswer])
         
                Awarded_marks = response.text

                
                print("The marks awarded is : "+Awarded_marks)

    except Exception as e:
            print(f"Error during batch document text detection: {str(e)}")
  


# Replace 'your_image_paths' with a list of paths to your image files
image_paths = [
    r'/home/tamil/ScriptEvaluationNew/test_data/Neuron_Expected_answer.jpg',
    r'/home/tamil/ScriptEvaluationNew/test_data/Neuron_Given_Answer.jpeg',
# Add more paths as needed
]

# Replace 'path/to/your/keyfile.json' with the actual path to your Google Cloud service account key JSON file
#credentials_path = '/home/tamil/keys/unused/script-evaluation-a41aac110e2b.json'

#main call for detecting the handwriting via the Google.vesion
#batch_detect_handwriting(image_paths, credentials_path)
    
    #Theory normal paper
#evaluate_the_AnswerScript_gemini(image_paths)
max_marks = "10"
question = "Draw a neat digram of human neuron and mark the following parts Axon hillock,dentrits,axon,presyhaptic terminal"

gemini_analysis_digram(image_paths[0],image_paths[1],question,max_marks)



