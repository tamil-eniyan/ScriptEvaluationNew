import spacy
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import google.generativeai as genai
import docx2txt

GEMINI_API = "AIzaSyCtQ914aymvoEhR07yzd9wB0EnkGBCK8JY"
GOOGLE_VISION_CREDENTIALS_PATH = r"KEYS\google_vision_cred.json"
FIREBASE_CREDENTIALS_PATH = r"KEYS\firebase_cred.json"
RIGHT_ANSWER_PATH = r"test_data\right_answer.docx"
STUDENT_ANSWER_PATH = r"test_data\student_answer.jpeg"

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



def gemini_grading(student_ans,right_ans,max_marks):
    genai.configure(api_key=GEMINI_API)
    model = genai.GenerativeModel(model_name = 'gemini-pro',safety_settings=safety_settings)

    template = f"""The student answer is '{student_ans}' ; and the expected answer by the teacher is '{right_ans}'; now evaluate the answer of the student by using the expected answer of the teacher as the template and give back  the mark out of {max_marks} , Give me only the mark, no other explanation or suggestion or sorry message or any alternatives"""

    marks = model.generate_content(template).text
    return marks





def process_text_into_paragraphs(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    paragraphs = []
    current_paragraph = []

    for sentence in doc.sents:
        current_paragraph.append(sentence.text)

    # Check if the current paragraph is not empty before appending
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    return paragraphs

def batch_detect_handwriting(image_paths, credentials_path):
    """Batch detects handwriting features in images using Google Cloud Vision API."""
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    batch_requests = []

    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        feature = types.Feature(type_=types.Feature.Type.DOCUMENT_TEXT_DETECTION)
        
        request = {"image": image, "features": [feature]}
        batch_requests.append(request)

    try:
        # Perform batch document text detection
        batch_response = client.batch_annotate_images(requests=batch_requests)

        for i, response in enumerate(batch_response.responses, 1):
            # Extract and print the text for each image
            extracted_text = response.full_text_annotation.text
            # print(f"\nImage {i} - Extracted Text:")
            # print(extracted_text)

            # Process the text into paragraphs
            paragraphs = process_text_into_paragraphs(extracted_text)

            # Print the processed paragraphs
            print("\nProcessed Paragraphs:")
            for j, paragraph in enumerate(paragraphs, 1):
                print(f"Paragraph {j}: {paragraph}")

    except Exception as e:
        print(f"Error during batch document text detection: {str(e)}")
    
    

    answer_scheme = docx2txt.process(RIGHT_ANSWER_PATH)
    print(answer_scheme)

    max_marks='10'

    awaded_marks = gemini_grading(extracted_text,answer_scheme,max_marks).split("/")[0]
    print("")
    print("The marks awarded to the student is : "+awaded_marks)


# Replace 'your_image_paths' with a list of paths to your image files
image_paths = [
    STUDENT_ANSWER_PATH,
    # Add more paths as needed
]

# Replace 'path/to/your/keyfile.json' with the actual path to your Google Cloud service account key JSON file
credentials_path = GOOGLE_VISION_CREDENTIALS_PATH

batch_detect_handwriting(image_paths, credentials_path)
