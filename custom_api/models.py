from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at}"

class Transcription1(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at}"