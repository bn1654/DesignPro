from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('requests/', include('requests.urls')),
    path('', RedirectView.as_view(url='/requests/')),
    path('catalog/', RedirectView.as_view(url='/requests/')), #Почему то он пытается зайти на url прошлого задания (кеш браузера чистил раза 4)
    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)