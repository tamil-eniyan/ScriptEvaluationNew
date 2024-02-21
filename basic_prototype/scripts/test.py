import spacy
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account

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

# Replace 'your_image_paths' with a list of paths to your image files
image_paths = [
    'C:/Ganglia/ScriptEvaluationNew/app/uploads/Answer1.png',
    'C:/Ganglia/ScriptEvaluationNew/app/uploads/Answer2.png',
    # Add more paths as needed
]

# Replace 'path/to/your/keyfile.json' with the actual path to your Google Cloud service account key JSON file
credentials_path = 'C:/Ganglia/scriptEvalToken/script-evaluation-a41aac110e2b.json'

batch_detect_handwriting(image_paths, credentials_path)
