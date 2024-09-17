from django import forms
from .models import Mosque

class MosqueRegistrationForm(forms.ModelForm):
    class Meta:
        model = Mosque
        fields = ['mosque_name', 'village', 'district', 'thana', 'division', 'imam_name', 'imam_mobile_number', 'muazzin_name', 'muazzin_mobile_number']
        widgets = {
            'mosque_name': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'thana': forms.TextInput(attrs={'class': 'form-control'}),
            'division': forms.TextInput(attrs={'class': 'form-control'}),
            'imam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'imam_mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'muazzin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'muazzin_mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
