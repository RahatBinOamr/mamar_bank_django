from django.contrib.auth import login,logout
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm , UserUpdateForm
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy



class UserRegistrationView(FormView):
    
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
  
        login(self.request, user)
        return super().form_valid(form)
    
def Profile(request):
    return render(request, 'user_profile.html')

class UserUpdateView(View):
    template_name = 'user_update.html'
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
            
    



    
class LoginView(LoginView):
    template_name='user_login.html'
    def get_success_url(self) :
        return reverse_lazy('home')
    
def LogoutView(request):
    logout(request)
    return redirect('home')
    