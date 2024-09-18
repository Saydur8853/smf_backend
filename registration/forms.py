from django import forms
from .models import Mosque, Qarrj_Hasana_Account

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


class QarrjHasanaAccountForm(forms.ModelForm):
    class Meta:
        model = Qarrj_Hasana_Account
        fields = [
            'mosque', 'name', 'phone_number', 'email', 'address', 'nid_no',
            'bank', 'bank_account_number', 'mobile_bank', 'mobile_bank_number'
        ]
        widgets = {
            'mosque': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_no': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_bank': forms.Select(attrs={'class': 'form-control'}),
            'mobile_bank_number': forms.TextInput(attrs={'class': 'form-control'}),
        }