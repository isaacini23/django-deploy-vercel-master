import os
import subprocess
import cv2
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import speech_recognition as sr
import pytesseract
from PIL import Image
from django.core.files.storage import default_storage
from paddleocr import PaddleOCR
from .models import Transcription
from .serializers import TranscriptionSerializer

# Define storage paths
AUDIO_UPLOAD_FOLDER = "media/uploads/audio/"
IMAGE_UPLOAD_FOLDER = "media/uploads/images/"

# Ensure storage folders exist
os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)

# Initialize PaddleOCR
ocr = PaddleOCR(lang='en')

# ✅ VOICE TRANSCRIPTION (SPEECH-TO-TEXT)
@api_view(['GET', 'POST'])  # Require login
def transcribe_audio(request):
    """Convert uploaded audio file to text and save it."""
    print("✅ Received speech-to-text request")


    if request.method == "GET":
        return Response({"message": "Send a POST request with an audio file to transcribe."})


    if 'audio' not in request.FILES:
        print("❌ No audio file uploaded")
        return Response({'error': 'No audio file uploaded'}, status=400)

    # Save the uploaded audio file
    audio_file = request.FILES['audio']
    file_name = audio_file.name
    file_path = os.path.join(AUDIO_UPLOAD_FOLDER, file_name)

    with open(file_path, 'wb') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)

    print(f"🔍 Saved audio file: {file_path}")

    # Convert to WAV if needed
    wav_path = file_path.rsplit(".", 1)[0] + ".wav"
    
    try:
        print("🎵 Converting audio to WAV...")
        subprocess.run(
            ["ffmpeg", "-i", file_path, "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", wav_path],
            check=True,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )

        if not os.path.exists(wav_path):
            print("❌ WAV conversion failed")
            return Response({'error': 'Failed to convert audio to WAV'}, status=500)

        print("✅ Audio converted successfully")

        # Process audio with speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            print("🎤 Listening to audio...")
            audio = recognizer.record(source)

        try:
            print("🧠 Performing speech recognition...")
            text = recognizer.recognize_google(audio)
            print(f"📜 Transcription: {text}")

            # ✅ Save transcription to DB
            transcription = Transcription.objects.create(audio_file=wav_path, text=text)
            serializer = TranscriptionSerializer(transcription)

            return Response({"transcription": text, "file_path": wav_path, "data": serializer.data})

        except sr.UnknownValueError:
            return Response({"error": "Could not understand audio"}, status=400)
        except sr.RequestError:
            return Response({"error": "Speech recognition service unavailable"}, status=503)

    except subprocess.CalledProcessError:
        return Response({'error': 'ffmpeg failed to convert audio'}, status=500)

# ✅ OCR IMAGE PROCESSING (TEXT FROM IMAGE)
@api_view(['GET', 'POST'])
  # Require login
def ocr_image(request):
    """Extract text from an uploaded image using PaddleOCR."""
    print("✅ Received OCR request")


    if request.method == "GET":
        return Response({"message": "Send a POST request with an audio file to transcribe."})


    if 'image' not in request.FILES:
        return Response({'error': 'No image file uploaded'}, status=400)

    # Save the uploaded file
    image_file = request.FILES['image']
    file_name = image_file.name
    file_path = os.path.join(IMAGE_UPLOAD_FOLDER, file_name)

    with open(file_path, 'wb') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    print(f"🔍 Saved image file: {file_path}")

    # Perform OCR with PaddleOCR
    try:
        result = ocr.ocr(file_path, cls=True)

        # Extract text from result
        extracted_text = "\n".join([word[1][0] for line in result for word in line])

        print(f"📜 Extracted Text:\n{extracted_text}")

        # ✅ Save transcription to DB
        transcription = Transcription.objects.create(image_file=file_path, text=extracted_text)
        serializer = TranscriptionSerializer(transcription)

        return Response({"text": extracted_text, "file_path": file_path, "data": serializer.data})

    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return Response({"error": "OCR failed", "details": str(e)}, status=500)

# ✅ GET TRANSCRIPTIONS FROM DATABASE
@api_view(['GET', 'POST'])
 # Require login
 
def get_transcriptions(request):
    """Retrieve all transcriptions from the database."""

    if request.method == "GET":
        return Response({"message": "Send a POST request with an audio file to transcribe."})

    transcriptions = Transcription.objects.all().order_by('-created_at')
    serializer = TranscriptionSerializer(transcriptions, many=True)
    return Response(serializer.data)
