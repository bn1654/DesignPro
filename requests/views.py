from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Request
from .forms import SignUpForm, LoginForm, RequestCreateForm
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def index(request):
    
    request_list = Request.objects.filter(status='c').order_by('-creation_date')
    print(request_list)
    newest_completed_request = []
    request_count = 0
    for i in request_list:
        newest_completed_request.append(i)
        request_count += 1
        if request_count >= 4:
            break

    requests_is_accepted = Request.objects.filter(status='a').count()
    
    return render(
    request,
    'requests/index.html',
    context={'request_list': newest_completed_request, 'requests_is_accepted':requests_is_accepted,},
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
    form_class = LoginForm
    template_name = 'requests/login_form.html'

@login_required
def profile_view(request):
    profile_requests = Request.objects.filter(author=request.user)
    
    
    return render(request, 'requests/profile.html', context={"requests": profile_requests})

class ProfileView(ListView):
    model = Request
    template_name = 'requests/profile.html'
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        author = self.request.user
        
        queryset = queryset.filter(author=author)
        
        status = self.request.GET.get('status')
        print(status)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        print(context)
        return context
    
    

class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestCreateForm
    template_name = 'requests/request_creation.html'
    success_url = reverse_lazy('profile')
    
    def dispatch(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.current_user
        form.instance.creation_date = datetime.now()
        return super().form_valid(form)


class RequestDelete(DeleteView):
    model = Request
    success_url = reverse_lazy('profile')