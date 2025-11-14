from django.shortcuts import render
from .models import Request



def index(request):
    
    request_list = Request.objects.filter(status='c')
    requests_is_accepted = Request.objects.filter(status='a').count()
    print(requests_is_accepted)
    
    return render(
    request,
    'requests/index.html',
    context={'request_list': request_list, 'requests_is_accepted':requests_is_accepted,},
)

