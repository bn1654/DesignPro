from django.db import models
from . import validators
from datetime import datetime, timedelta
from .utilities import rename_image
from django.contrib.auth.models import AbstractUser

class AbsUser(AbstractUser):
    FIO = models.CharField(verbose_name="FIO", max_length=255, validators=[validators.validate_FIO])
    email=models.EmailField(verbose_name="login", max_length=255, unique=True)
    
    class Meta(AbstractUser.Meta):
        pass

class Category(models.Model):
    name  = models.CharField(verbose_name="name", max_length=200, help_text="name of category")
    
    def __str__(self):
        return self.name

class Request(models.Model):
    name = models.CharField(verbose_name="name", max_length=200, help_text="name of design")
    summary = models.TextField(verbose_name="summary", max_length=500, help_text="design's summary")
    image = models.ImageField(
        verbose_name="image",
        null=True,
        blank=True,
        help_text="design's image",
        validators=[validators.validate_image_size, validators.validate_image_format],
        upload_to=rename_image
        )
    creation_date = models.DateField(verbose_name="creation date", default=datetime.now(), help_text="date and time of design's creation")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    REQUEST_STATUS = [
        ('n', 'New'),
        ('a', 'Accepted'),
        ('c', 'Complete'),
    ]
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='n', help_text='request status')

    def __str__(self):
        return self.name
    
    def is_new_request(self):
        return datetime.now().date() < self.creation_date + timedelta(days=2)