from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Request
from .forms import SignUpForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    
    request_list = Request.objects.filter(status='c')
    requests_is_accepted = Request.objects.filter(status='a').count()
    
    return render(
    request,
    'requests/index.html',
    context={'request_list': request_list, 'requests_is_accepted':requests_is_accepted,},
)

class SingUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'requests/singup_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('index')

class RequestLogin(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile')
    template_name = 'requests/login_form.html'

@login_required
def profile_view(request):
    return render(request, 'requests/profile.html')