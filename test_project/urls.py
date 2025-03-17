
from django.contrib import admin
from django.urls import path

from accounts.views import home, signup_view, login_view, logout_view
from custom_api.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('transcribe_audio/', transcribe_audio, name='transcribe_audio'),
    path('ocr_image/', ocr_image, name='ocr_image'),
    path('transcriptions/', get_transcriptions, name='get_transcriptions'),
    

]
