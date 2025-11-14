from django.core.exceptions import ValidationError
import os

def validate_image_size(value):
    if value.size > 2*(1024**2):
        raise ValidationError("File size should not be above 2 MB")

def validate_image_format(value):
    ext = os.path.splitext(value.name)[1]
    valid_formats = ['.jpg', '.jpeg', '.png', '.bmp']
    
    if ext not in valid_formats:
        raise ValidationError("Wrong file format")