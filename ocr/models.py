from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    processed_text = models.TextField(null=True, blank=True)
