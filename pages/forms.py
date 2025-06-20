# pages/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Book, Category

User = get_user_model()

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.cleaned_data['username'] = user.username  # Switch to username for auth
                return super().clean()
            except User.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'email'
    }))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': 'username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'id': 'confirmPassword'
        })


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'id': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password'  
        })
    )


class BookForm(forms.ModelForm):
    custom_category = forms.CharField(
        required=False,
        label='Custom Category',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom category name'
        })
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book title'
        }),
        min_length=2,
        max_length=200,
        help_text="Title must be between 2 and 200 characters"
    )
    author = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author name'
        }),
        min_length=2,
        max_length=100,
        help_text="Author name must be between 2 and 100 characters"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book description',
            'rows': 4
        }),
        min_length=10,
        help_text="Description must be at least 10 characters"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select a category or choose 'Other' to create a new one"
    )
    status = forms.ChoiceField(
        choices=Book.status_book,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select the availability status of the book"
    )
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text="Upload a cover image (max 5MB, supported formats: JPG, PNG)"
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'image', 'status']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long")
        
        # Check for duplicate titles, excluding the current instance if editing
        existing_books = Book.objects.filter(title__iexact=title)
        if self.instance and self.instance.pk:
            existing_books = existing_books.exclude(pk=self.instance.pk)
            
        if existing_books.exists():
            raise forms.ValidationError("A book with this title already exists")
        return title.strip()

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 2:
            raise forms.ValidationError("Author name must be at least 2 characters long")
        return author.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long")
        return description.strip()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Unsupported file format. Please use JPG or PNG")
        return image

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'address', 'birth_date', 'gender']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Upload a profile image (max 5MB)',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'birth_date': 'Date of Birth',
            'gender': 'Gender',
        }
