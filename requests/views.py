from datetime import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Request, Category
from .forms import SignUpForm, LoginForm, RequestCreateForm, RequestStatusAForm, RequestStatusСForm, CategoryCreateForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def index(request):
    
    request_list = Request.objects.filter(status='c').order_by('-creation_date')
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


class ProfileView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'requests/profile.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        author = self.request.user
        
        queryset = queryset.filter(author=author)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-creation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
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
    

class AdminView(ListView):
    model = Request
    template_name = 'requests/admin_panel.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("Доступ запрещен")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-creation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        return context

class RequestStatusUpdate(UpdateView):
    model = Request
    fields = ['status']
    success_url = reverse_lazy('admin')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("Доступ запрещен")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['selected_status'] = self.request.GET.get('status', '')
        context['accept_form'] = RequestStatusAForm()
        context['complete_form'] = RequestStatusСForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if 'accept' in request.POST:
            form = RequestStatusAForm(request.POST)
            if form.is_valid():
                self.object.status = 'a'
                self.object.save()
                return redirect(self.success_url)
            else:
                context = self.get_context_data()
                context['accept_form'] = form
                return self.render_to_response(context)        
        elif 'complete' in request.POST:
            form = RequestStatusСForm(request.POST, request.FILES)
            if form.is_valid():
                self.object.status = 'c'
                self.object.save()
                return redirect(self.success_url)
            else:
                context = self.get_context_data()
                context['complete_form'] = form
                return self.render_to_response(context)
        
        return redirect(self.success_url)

class CategoryListView(ListView):
    model = Category
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["category_create"] = CategoryCreateForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        else:
            context = self.get_context_data()
            context['category_create'] = form
            return self.render_to_response(context)

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    
    