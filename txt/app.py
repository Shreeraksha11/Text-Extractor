import os
from flask import Flask, render_template, request
import cv2
import pytesseract

app = Flask(__name__)

# Set the Tesseract-OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ensure the uploads directory exists
uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    # Save the uploaded file
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)

    # Read the image using OpenCV
    img = cv2.imread(file_path)
    
    if img is None:
        return "Error: Unable to read the image."

    # Convert to grayscale and process
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Perform OCR
    text = pytesseract.image_to_string(binary)

    return render_template('result.html', extracted_text=text)

if __name__ == '__main__':
    app.run(debug=True)

