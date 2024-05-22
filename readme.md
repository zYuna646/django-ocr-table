# Django OCR API

This Django project provides an API endpoint that accepts an image, processes it using PaddleOCR to extract text, and returns an Excel file with the extracted text.

## Features

- Accepts image uploads via API.
- Processes images using PaddleOCR to extract text.
- Organizes the extracted text into rows and columns.
- Returns an Excel file with the extracted text.

## Requirements

- Python 3.x
- Django
- PaddleOCR
- Pillow
- openpyxl
- djangorestframework

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/zYuna646/django-ocr-table.git
    cd django-ocr-table
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install django pillow paddlepaddle paddleocr openpyxl djangorestframework
    ```

4. Run the migrations:

    ```sh
    python manage.py migrate
    ```

5. Start the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

### API Endpoint

- **URL**: `/ocr/process/`
- **Method**: POST
- **Content Type**: `multipart/form-data`
- **Body**: 

  - `image`: The image file to be processed.

### Example with Postman

1. Open Postman and create a new POST request.
2. Set the URL to `http://127.0.0.1:8000/ocr/process/`.
3. Set the method to POST.
4. In the Body tab, select `form-data`.
5. Add a key named `image` and set its type to `File`.
6. Upload the image you want to process.
7. Send the request.

### Example with cURL

```sh
curl -X POST http://127.0.0.1:8000/ocr/process/ -F "image=@/path/to/your/image.jpg" 
```

### Example with Python
```sh
    import requests

    url = 'http://127.0.0.1:8000/ocr/process/'
    files = {'image': open('/path/to/your/image.jpg', 'rb')}

    response = requests.post(url, files=files)

    with open('output.xlsx', 'wb') as f:
        f.write(response.content)

    print("Excel file received and saved as output.xlsx")
```

<!-- myproject/
├── manage.py
├── ocr_table/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── ocrapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py -->


<!-- ### Penjelasan
- **Features**: Menjelaskan fitur utama dari proyek.
- **Requirements**: Menyediakan daftar pustaka yang diperlukan.
- **Installation**: Langkah-langkah untuk mengkloning repositori, membuat dan mengaktifkan virtual environment, menginstal dependensi, menjalankan migrasi, dan memulai server pengembangan.
- **Usage**: Instruksi tentang bagaimana menggunakan API, termasuk contoh penggunaan dengan Postman, cURL, dan Python.
- **Project Structure**: Menyediakan struktur direktori dari proyek untuk memberikan pemahaman tentang organisasi kode.
- **Contributing**: Panduan tentang bagaimana berkontribusi ke proyek.
- **License**: Informasi tentang lisensi proyek. -->
