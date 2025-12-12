from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Citizen, Complaint

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a unique username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

class CitizenProfileForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ['phone', 'address', 'city', 'state']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'location', 'image', 'category', 'severity', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description of the issue'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Detailed description of the problem'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address or landmark'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be under 5MB.')
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = image.name.lower()
            if not any(ext.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError('Please upload a valid image file (JPG, PNG, GIF).')
        
        return image

class ComplaintStatusUpdateForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        help_text='Add notes about this status update',
        required=False
    )
    
    # Add severity and priority fields for admin use
    severity = forms.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Set the severity level of this issue'
    )
    
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Set the priority level for resolution'
    )
    
    class Meta:
        model = Complaint
        fields = ['status', 'category', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'style': 'resize: none; height: 120px;',
                'placeholder': 'Add admin notes about this complaint...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for severity and priority if provided
        if 'initial' in kwargs:
            if 'severity' in kwargs['initial']:
                self.fields['severity'].initial = kwargs['initial']['severity']
            if 'priority' in kwargs['initial']:
                self.fields['priority'].initial = kwargs['initial']['priority']
