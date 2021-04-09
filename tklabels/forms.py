from django import forms
from .models import *

class CustomiseTKLabelForm(forms.ModelForm):
    class Meta:
        model = TKLabel
        fields = ['name', 'default_text']
        widgets = {
            'name': forms.TextInput(attrs={'size': 40, 'id': 'label-title-name'}),
            'default_text': forms.Textarea(attrs={'rows': 4, 'cols': 204, 'id': 'label-template-text'}),
        }

class ApproveAndEditTKLabelForm(forms.ModelForm):
    class Meta:
        model = TKLabel
        fields = ['name', 'default_text']
        widgets = {
            'name': forms.TextInput(attrs={'size': 40}),
            'default_text': forms.Textarea(attrs={'rows': 4, 'cols': 204}),
        }

# class AddTKNoticeMessage(forms.ModelForm):
#     class Meta:
#         model = TKNotice
#         fields = ['message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 4, 'cols': 204}),
#         }