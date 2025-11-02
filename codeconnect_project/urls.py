from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Temporary view for the dashboard/home page until the 'projects' app is built
# This will eventually be replaced by a proper dashboard view
def dashboard_view(request):
    if request.user.is_authenticated:
        return redirect('projects:dashboard') # Assumes we will have a 'projects' app dashboard
    return redirect('accounts:login') # Redirect unauthenticated users to login


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home Page / Dashboard - Check if user is logged in
    path('', dashboard_view, name='dashboard'), 
    
    # Includes all URLs from the accounts app (login, signup, logout)
    path('accounts/', include('accounts.urls')),
    
    # Placeholder for future projects app
    # path('projects/', include('projects.urls')),
]
