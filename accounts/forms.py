from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, FreelancerProfile

class FreelancerSignUpForm(UserCreationForm):
    """
    Custom form for a new Freelancer to sign up.
    Includes fields from the User model (username, email, password)
    and the FreelancerProfile model (hourly_rate).
    """
    
    # Fields for FreelancerProfile
    hourly_rate = forms.DecimalField(
        label='Your Standard Hourly Rate (USD)',
        max_digits=6,
        decimal_places=2,
        initial=50.00,
        min_value=0.01,
        help_text="This rate will be used as the default for quote generation."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Include email in the signup form
        fields = ('username', 'email',) + UserCreationForm.Meta.fields

    @transaction.atomic
    def save(self):
        """
        Saves the User and creates the associated FreelancerProfile.
        """
        # 1. Save the base User object
        user = super().save(commit=False)
        user.is_freelancer = True  # Mark the user as a freelancer
        user.is_client = False # Ensure client status is false
        user.save()
        
        # 2. Create the linked FreelancerProfile
        freelancer_profile = FreelancerProfile.objects.create(
            user=user,
            hourly_rate=self.cleaned_data.get('hourly_rate')
        )
        # Note: subscription_tier defaults to 'FREE' as defined in the model
        
        return user
