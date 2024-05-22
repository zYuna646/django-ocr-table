from django.urls import path
from .views import OCRProcessView

urlpatterns = [
    path('process/', OCRProcessView.as_view(), name='ocr-process'),
]

