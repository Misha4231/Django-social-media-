from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', file_create, name='file_create'),
    path('media/', media_list, name='media_list'),
    path('like/', image_like, name='like'),
]