import requests
import numpy as np
from paddleocr import PaddleOCR
from openpyxl import Workbook
from PIL import Image
import os
from io import BytesIO
from django.http import FileResponse
from django.http import HttpResponseServerError
import traceback


def load_image(image):
    if hasattr(image, 'url') and image.url.startswith('http'):
        response = requests.get(image.url)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(image)
    return img

def extract_text_from_image(image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR
    img = np.array(image)
    result = ocr.ocr(img, cls=True)
    return result

def group_text_by_rows(results):
    rows = {}
    for line in results:
        for word in line:
            text = word[-1][0]
            box = word[0]  # Bounding box coordinates
            top_left_y = box[0][1]

            # Determine the row based on the y-coordinate of the top-left corner
            row_key = int(top_left_y // 20)  # Adjust this threshold according to your image
            if row_key not in rows:
                rows[row_key] = []
            rows[row_key].append((box[0][0], text))  # Store x-coordinate and text

    # Sort rows by y-coordinate and then sort each row by x-coordinate
    sorted_rows = sorted(rows.items())
    table_data = []
    for _, row in sorted_rows:
        row.sort(key=lambda x: x[0])
        table_data.append([text for _, text in row])
    
    return table_data

def results_to_excel(table_data, output_excel):
    wb = Workbook()
    ws = wb.active

    for row in table_data:
        ws.append(row)

    wb.save(output_excel)
    return output_excel


def process_image(image_path, output_excel):
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    image = load_image(image_path)
    results = extract_text_from_image(image)
    table_data = group_text_by_rows(results)
    excel_file = results_to_excel(table_data, output_excel)
    return excel_file  # Mengembalikan nama file string


