# ocrapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageUploadSerializer
from .utils import extract_text_from_image, group_text_by_rows, results_to_excel
import os

class OCRProcessView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            image = file_serializer.validated_data['image']
            image_path = image.temporary_file_path()

            results = extract_text_from_image(image_path)
            table_data = group_text_by_rows(results)
            output_excel = 'output.xlsx'
            results_to_excel(table_data, output_excel)

            with open(output_excel, 'rb') as f:
                response = Response(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=output.xlsx'
                return response

        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
