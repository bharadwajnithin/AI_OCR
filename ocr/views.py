from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import ImageUpload
from .utils import (convert_to_grayscale, reduce_noise, binarize_image, correct_skew,
                    enhance_contrast, extract_text, create_pdf)
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            image_path = image_upload.image.path
            preprocessed_image_path = f"{image_path}_preprocessed.jpg"

            grayscale_image = convert_to_grayscale(image_path, preprocessed_image_path)
            cleaned_image = reduce_noise(grayscale_image, preprocessed_image_path)
            bw_image = binarize_image(cleaned_image, preprocessed_image_path)
            corrected_image = correct_skew(bw_image, preprocessed_image_path)
            enhanced_image = enhance_contrast(corrected_image, preprocessed_image_path)

            processed_text = extract_text(preprocessed_image_path)
            image_upload.processed_text = processed_text
            image_upload.save()
            return redirect('result', pk=image_upload.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'ocr/upload.html', {'form': form})

def view_result(request, pk):
    image_upload = ImageUpload.objects.get(pk=pk)
    return render(request, 'ocr/result.html', {'image_upload': image_upload})

def download_pdf(request, pk):
    image_upload = ImageUpload.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="processed_text_{pk}.pdf"'
    create_pdf(image_upload.processed_text, response)
    return response

def download_preprocessed_image(request, pk):
    image_upload = ImageUpload.objects.get(pk=pk)
    preprocessed_image_path = f"{image_upload.image.path}_preprocessed.jpg"
    with open(preprocessed_image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="preprocessed_image_{pk}.jpg"'
    return response
