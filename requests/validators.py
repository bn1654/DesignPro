import re
from django.core.exceptions import ValidationError
import os

def validate_image_size(value):
    if value.size > 2*(1024**2):
        raise ValidationError("Файл не должен превышать 2 МБ")

def validate_image_format(value):
    ext = os.path.splitext(value.name)[1]
    valid_formats = ['.jpg', '.jpeg', '.png', '.bmp']
    
    if ext not in valid_formats:
        raise ValidationError("Неверное расширение файла")

def validate_FIO(value):
    alphabet=r'^[а-я/-/ ]+$'
    if not re.findall(alphabet, value):
        raise ValidationError("ФИО указано неверно")

    
    
