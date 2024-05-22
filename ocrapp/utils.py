# ocrapp/utils.py
import cv2
import numpy as np
from paddleocr import PaddleOCR
from openpyxl import Workbook
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

def load_image(image_path):
    if image_path.startswith('http'):
        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(image_path)
    return img

def display_image(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def extract_text_from_image(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR
    img = load_image(image_path)
    img = np.array(img)
    result = ocr.ocr(img, cls=True)
    return result

def print_ocr_results(results):
    for line in results:
        for word in line:
            print(word[-1][0])  # Print the detected text

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
