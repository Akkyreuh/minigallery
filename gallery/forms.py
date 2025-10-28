from django import forms
from .models import Image, PurchasePrediction

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'image'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            })
        }
        labels = {
            'title': 'Titre',
            'url': 'URL de l\'image'
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'image'
            }),
            'image_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Titre',
            'image_file': 'Fichier image'
        }

class PredictionForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Homme'),
        ('Female', 'Femme'),
    ]
    
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Âge (18-100)'
        }),
        label='Âge'
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Genre'
    )
    
    estimated_salary = forms.IntegerField(
        min_value=1000,
        max_value=500000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Salaire estimé (€)'
        }),
        label='Salaire estimé (€)'
    )