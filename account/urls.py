from django.urls import path
from .views import UserRegistrationView,LoginView,LogoutView,Profile,UserUpdateView

urlpatterns = [
    path('register',UserRegistrationView.as_view(),name='register'),
    path('update',UserUpdateView.as_view(),name='update'),
    path('profile',Profile,name='profile'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView,name='logout'),
]
