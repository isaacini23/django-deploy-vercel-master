from django.contrib import admin
from custom_api.models import *

# Register your models here.

@admin.register(Transcription)  # ✅ This is the correct way to register
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')  # Customize the list view
    search_fields = ('text',)  # Allow searching by text
    ordering = ('-created_at',)  # Show newest transcriptions first
admin.register(Transcription1)