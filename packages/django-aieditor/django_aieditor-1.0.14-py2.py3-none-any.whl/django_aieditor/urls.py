from django.urls import path
from . import views

app_name = 'django_aieditor'

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
] 