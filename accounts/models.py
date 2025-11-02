from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom User Model to add flexibility (required for many Django projects)
class User(AbstractUser):
    """
    A custom User model based on AbstractUser.
    We use this to ensure future flexibility in adding user-specific fields
    without needing to migrate existing Django auth tables later.
    """
    is_freelancer = models.BooleanField(
        default=False,
        verbose_name=_('Freelancer Status'),
        help_text=_('Designates whether the user is a freelancer who manages projects.')
    )
    is_client = models.BooleanField(
        default=False,
        verbose_name=_('Client Status'),
        help_text=_('Designates whether the user is a client (customer) of the freelancer.')
    )
    email = models.EmailField(_('email address'), unique=True)
    
    # We set the email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_freelancer', 'is_client']

    def __str__(self):
        return self.email


class FreelancerProfile(models.Model):
    """
    Extends the User model for specific freelancer settings (e.g., subscription).
    """
    # One-to-One Link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    # Subscription Tier for the SaaS business model
    SUBSCRIPTION_CHOICES = [
        ('FREE', 'Free Tier (Limited Projects)'),
        ('PRO', 'Pro Tier (Unlimited Projects)'),
        ('PREMIUM', 'Premium Tier (Invoicing & Integrations)'),
    ]
    subscription_tier = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_CHOICES,
        default='FREE',
        help_text="The current paid subscription level of the freelancer."
    )
    
    # Hourly Rate used for quote generation
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=50.00,
        help_text="The freelancer's standard hourly rate for quoting."
    )

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.subscription_tier})"
        
    class Meta:
        verbose_name = "Freelancer Profile"
        verbose_name_plural = "Freelancer Profiles"
        
        
class Client(models.Model):
    """
    Represents a company or individual who commissions a project from the Freelancer.
    """
    # The freelancer who owns this client record
    freelancer = models.ForeignKey(
        FreelancerProfile, 
        on_delete=models.CASCADE, 
        related_name='clients',
        help_text="The freelancer managing this client."
    )
    
    name = models.CharField(max_length=255, help_text="The full name of the client or company.")
    contact_email = models.EmailField(help_text="The primary contact email for the client.")
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        # Ensures a freelancer can't accidentally add the same client name twice for their account
        unique_together = ('freelancer', 'name')
