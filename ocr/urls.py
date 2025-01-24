from django.urls import path
from .views import upload_image, view_result, download_pdf, download_preprocessed_image

urlpatterns = [
    path('', upload_image, name='upload'),
    path('result/<int:pk>/', view_result, name='result'),
    path('download_pdf/<int:pk>/', download_pdf, name='download_pdf'),
    path('download_preprocessed_image/<int:pk>/', download_preprocessed_image, name='download_preprocessed_image'),
]
