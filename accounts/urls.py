from django.urls import path
from django.contrib.auth import views as auth_views # Django built-in auth views
from . import views

# Set the app_name for cleaner URL referencing in templates
app_name = 'accounts'

urlpatterns = [
    # Custom Signup
    path('signup/freelancer/', views.FreelancerSignUpView.as_view(), name='signup_freelancer'),
    
    # Built-in Login/Logout views
    # Django Auth views use specific template names by default
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
