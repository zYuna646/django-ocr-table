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
            data =  process_image(image)
            return Response(data, status=status.HTTP_200_OK)
        else:
            print('here');
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
