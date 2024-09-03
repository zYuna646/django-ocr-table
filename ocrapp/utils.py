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
    print(result)
    return result

def group_text_by_rows(results):
    rows = {}
    for line in results:
        for word in line:
            text = word[-1][0]
            box = word[0]
            top_left_y = box[0][1]
            row_key = int(top_left_y // 30)
            if row_key not in rows:
                rows[row_key] = []
            rows[row_key].append((box[0][0], text))

    sorted_rows = sorted(rows.items())
    table_data = []
    for _, row in sorted_rows:
        row.sort(key=lambda x: x[0])
        table_data.append([text for _, text in row])

    return table_data

def map_table_data_to_json(table_data):
    json_output = []
    for row in table_data:
        if len(row) >= 12:  # Adjust based on expected number of columns
            json_output.append({
                "No. URUT": row[0],
                "No.": '',
                "Tanggal": row[1],
                "Bentuk Perbuatan Hukum": row[2],
                "Pihak Yang Mengalihkan/Memberikan": row[3],
                "Pihak Yang Menerima": row[4],
                "Jenis dan Nomor Hak": row[5],
                "Letak Tanah dan Bangunan": row[6],
                "Tanah": row[7],
                "Bgn": row[8],
                "Harga Transaksi Perolehan/Pengalihan": row[9],
                "NOP TAHUN": row[10],
                "NJOP (Rp.000)": row[11] if len(row) > 11 else "",
                "SSP TGL": row[12] if len(row) > 12 else "",
                "SSP (Rp.000)": row[13] if len(row) > 13 else "",
                "SSB TGL": row[14] if len(row) > 14 else "",
                "SSB (Rp.000)": row[15] if len(row) > 15 else "",
                "Ket": row[16] if len(row) > 16 else ""
            })
    return json_output

def process_image(image_path):  
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    image = load_image(image_path)
    results = extract_text_from_image(image)
    
    table_data = group_text_by_rows(results)
    json_data = map_table_data_to_json(table_data)
    return json_data


