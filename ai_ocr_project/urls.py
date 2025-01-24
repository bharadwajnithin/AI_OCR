from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_upload(request):
    return redirect('upload')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ocr/', include('ocr.urls')),
    path('', redirect_to_upload),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
