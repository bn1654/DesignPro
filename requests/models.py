from django.db import models
from datetime import datetime
from .utilities import rename_image
from django.contrib.auth.models import AbstractUser

class AbsUser(AbstractUser):
    FIO = models.CharField(verbose_name="ФИО")
    email=models.EmailField(verbose_name="email", unique=True)
    
    def __str__(self):
        return self.username
    
    
    class Meta(AbstractUser.Meta):
        pass

class Category(models.Model):
    name  = models.CharField(verbose_name="Название", help_text="Название категории")
    
    def __str__(self):
        return self.name

class Request(models.Model):
    name = models.CharField(verbose_name="Название", help_text="Название заявки")
    summary = models.TextField(verbose_name="Описание", help_text="Описание заявки")
    image = models.ImageField(verbose_name="Изображение",blank=True,help_text="Изображение дизайна",upload_to=rename_image)
    creation_date = models.DateTimeField(verbose_name="Дата создания", default=datetime.now(), help_text="Дата и время создания заявки")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(AbsUser, on_delete=models.CASCADE, null=True)
    
    
    REQUEST_STATUS = [
        ('n', 'Новая'),
        ('a', 'Принята в работу'),
        ('c', 'Выполнено'),
    ]
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='n', help_text='request status')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['creation_date']


    