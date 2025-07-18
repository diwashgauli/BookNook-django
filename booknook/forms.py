from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'price', 'image', 'category', 'description', 'book_condition', 'trade_condition']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
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
        }
