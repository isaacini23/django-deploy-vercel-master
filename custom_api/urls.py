from django.urls import path
from .views import transcribe_audio, ocr_image, get_transcriptions

urlpatterns = [
    path('transcribe_audio/', transcribe_audio, name='transcribe_audio'),
    path('ocr_image/', ocr_image, name='ocr_image'),
    path('transcriptions/', get_transcriptions, name='get_transcriptions'),
    
]
