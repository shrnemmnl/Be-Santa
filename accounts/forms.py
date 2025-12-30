from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=True, max_length=255)
    age = forms.IntegerField(required=True, min_value=1, max_value=120, widget=forms.NumberInput(attrs={'class': 'no-spin'}))
    city = forms.CharField(required=True, max_length=100)
    phone = forms.CharField(
        required=True, max_length=15, 
        help_text="Enter a unique phone number"
    )
    full_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone', 'age', 'city', 'full_address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Auto-fill username with email
        if commit:
            user.save()
        return user
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Regex Validation
        if not phone.isdigit():
             raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
             raise forms.ValidationError("Phone number must be exactly 10 digits.")
        if not phone.startswith(('7', '8', '9')):
             raise forms.ValidationError("Phone number must start with 7, 8, or 9.")
             
        # Uniqueness Check
        if User.objects.filter(phone=phone).exists():
           raise forms.ValidationError("This user is already signed up, you have to login.")
        return phone

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
