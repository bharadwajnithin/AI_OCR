import cv2
import numpy as np
import easyocr
from reportlab.pdfgen import canvas

def convert_to_grayscale(image_path, output_path):
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, grayscale_image)
    return grayscale_image

def reduce_noise(image, output_path):
    cleaned_image = cv2.fastNlMeansDenoising(image, None, 30, 7, 21)
    cv2.imwrite(output_path, cleaned_image)
    return cleaned_image

def binarize_image(image, output_path):
    _, bw_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(output_path, bw_image)
    return bw_image

def correct_skew(image, output_path):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    corrected_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite(output_path, corrected_image)
    return corrected_image

def enhance_contrast(image, output_path):
    enhanced_image = cv2.equalizeHist(image)
    cv2.imwrite(output_path, enhanced_image)
    return enhanced_image

def extract_text(image_path):
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    result = reader.readtext(image)
    extracted_text = " ".join([text[1] for text in result])
    return extracted_text


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(text, response):
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 40, "Processed Text")

    # Draw the text
    text_object = c.beginText(100, height - 60)
    text_object.setFont("Helvetica", 12)
    
    lines = text.splitlines()
    for line in lines:
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()
