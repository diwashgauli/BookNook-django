from django import forms
from .models import Post,Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author_name',
            'price',
            'image',
            'category',
            'description',
            'book_condition',
            'trade_condition',
            'exchange_with'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter the book's author"
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a brief description',
                'rows': 4
            }),
            'book_condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'trade_condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'exchange_with': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What do you want in exchange? (Optional)'
            }),
        }





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }




