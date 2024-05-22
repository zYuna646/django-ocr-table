from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageUploadSerializer
from .utils import process_image
from django.http import FileResponse


class OCRProcessView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            image = file_serializer.validated_data['image']
            # Memproses gambar dan mendapatkan lokasi file output
            output_excel = process_image(image, 'output.xlsx')
            # Membuka file output dan mengirimkannya sebagai respons

            return FileResponse(open(output_excel, 'rb'), as_attachment=True, filename='output.xlsx')

        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
