import requests
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import os
from io import BytesIO
import json

def load_image(image_path):
    img = Image.open(image_path)
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
    
    # Map table data to the desired JSON structure
    json_data = {}
    for i, row in enumerate(table_data):
        if len(row) >= 18:  # Ensure there are enough columns
            data = {
                "Akta": {
                    "No.": row[0],
                    "Tanggal": row[1],
                },
                "Bentuk_Perbuatan_Hukum": row[2],
                "NPWP": {
                    "Pihak_Yang_Mengalihkan/Memberikan": row[3],
                    "Pihak Yang Menerima": row[4],
                },
                "Jenis_Dan_Nomor_Hak": row[5],
                "Letak_Tanah_Dan_Bangunan": row[6],
                "Luas": {
                    "Tanah": row[7],
                    "Bgn": row[8],
                },
                "Harga_Transaksi_Perolehan_Pengalihan": row[9],
                "SPPT_PPB": {
                    "NOP_Tahun": row[10],
                    "NJOP": row[11],
                },
                "SSP": {
                    "Tgl": row[12],
                    "Rp": row[13],
                },
                "SSB": {
                    "Tgl": row[14],
                    "Rp": row[15],
                },
                "Ket": row[16]
            }
            json_data[i] = data
    
    return json_data

def process_image(image_path):
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    image = load_image(image_path)
    results = extract_text_from_image(image)
    
    json_data = group_text_by_rows(results)
    return json_data