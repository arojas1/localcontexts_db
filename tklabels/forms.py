from email.mime import audio
from django import forms
from .models import *

class CustomizeTKLabelForm(forms.ModelForm):
    class Meta:
        model = TKLabel
        fields = ['name', 'language', 'label_text', 'audiofile']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'label-template-name', 'class': 'w-100', 'autocomplete': 'off'}),
            'language': forms.TextInput(attrs={'class': 'languageListInput w-100', 'placeholder': 'English', 'autocomplete': 'off'}),
            'label_text': forms.Textarea(attrs={'class': 'w-100 margin-top-1 margin-bottom-2', 'id': 'label-template-text', 'style': 'height: 150px; padding: 10px;'}),
        }

class EditTKLabelForm(forms.ModelForm):
    class Meta:
        model = TKLabel
        fields = ['name', 'language', 'label_text', 'audiofile']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-100', 'autocomplete': 'off'}),
            'language': forms.TextInput(attrs={'class': 'languageListInput w-100', 'placeholder': 'English', 'autocomplete': 'off'}),
            'label_text': forms.Textarea(attrs={'class': 'w-100 margin-top-1 margin-bottom-2', 'id': 'label-template-text', 'style': 'height: 150px; padding: 10px;'}),
        }