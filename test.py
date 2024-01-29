import spacy
from google.cloud import vision
from google.oauth2 import service_account

def process_text_into_paragraphs(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    paragraphs = []
    current_paragraph = []

    for sentence in doc.sents:
        current_paragraph.append(sentence.text)

        # Check for the end of a sentence to start a new paragraph
        if sentence.end == len(doc):
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []

    # Add the last paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    return paragraphs

def detect_handwriting(image_path, credentials_path):
    """Detects handwriting features in an image using Google Cloud Vision API."""
    # Set up credentials explicitly
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Read the image file
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    # Create a Vision API image object
    image = vision.Image(content=content)

    try:
        # Perform document text detection
        response = client.document_text_detection(image=image)

        # Extract and print the text
        extracted_text = response.full_text_annotation.text
        # print("Extracted Text:")
        # print(extracted_text)

        # Process the text into paragraphs
        paragraphs = process_text_into_paragraphs(extracted_text)

        # Print the processed paragraphs
        print("\nProcessed Paragraphs:")
        for i, paragraph in enumerate(paragraphs, 1):
            print(f"Paragraph {i}: {paragraph}")

    except Exception as e:
        print(f"Error during document text detection: {str(e)}")

# Replace 'your_image_path.jpg' with the path to your image file
image_path = 'C:/Ganglia/scriptEval/app/uploads/101_answer_script.png'

# Replace 'path/to/your/keyfile.json' with the actual path to your Google Cloud service account key JSON file
credentials_path = 'C:/Ganglia/scriptEvalToken/script-evaluation-a41aac110e2b.json'

detect_handwriting(image_path, credentials_path)
