import os
from PIL import Image
from django.core.exceptions import ValidationError

def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(f"Maximum size of image is 70px, but size of image that you've uploaded - {img.size}")
            

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.jpeg', '.png', '.jpg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupperted file extension")
