from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import FreelancerSignUpForm
from .models import User

# Use the Django built-in LoginView for simplicity, configured via settings.py

class FreelancerSignUpView(CreateView):
    """
    View to handle the Freelancer registration process.
    """
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'accounts/signup_freelancer.html'
    success_url = reverse_lazy('dashboard') # Redirect after successful registration

    def get_context_data(self, **kwargs):
        """Add context for the template (e.g., page title)."""
        kwargs['user_type'] = 'freelancer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """
        Called when valid form data has been POSTed.
        1. Saves the user and profile (handled by form.save()).
        2. Logs the user in immediately.
        """
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
