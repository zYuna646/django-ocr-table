import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import os

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
            row_key = int(top_left_y // 30)  # Adjust this threshold according to your image
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

def map_table_data_to_json(table_data):
    json_data = []

    for i, row in enumerate(table_data):
        # Ensure there are enough columns to avoid IndexError
        if len(row) >= 17:
            data = {
                "Akta": {
                    "No.": row[0],
                    "Tanggal": row[1],
                },
                "Bentuk Perbuatan Hukum": row[2],
                "NPWP": {
                    "Pihak Yang Mengalihkan/Memberikan": row[3],
                    "Pihak Yang Menerima": row[4],
                },
                "Jenis Dan Nomor Hak": row[5],
                "Letak Tanah Dan Bangunan": row[6],
                "Luas": {
                    "Tanah": row[7],
                    "Bgn": row[8],
                },
                "Harga Transaksi Perolehan Pengalihan": row[9],
                "SPPT PBB": {
                    "NOP Tahun": row[10],
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
            json_data.append(data)
        else:
            # Handle rows with fewer columns, log or handle as needed
            print(f"Row {i} has insufficient data: {row}")

    return json_data

def process_image(image_path):  
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    image = load_image(image_path)
    results = extract_text_from_image(image)
    
    table_data = group_text_by_rows(results)
    json_data = map_table_data_to_json(table_data)
    return json_data


