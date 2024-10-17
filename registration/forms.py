from django import forms
from .models import Mosque,Qarrj_Hasana_Account,Qarrj_Hasana_Apply,Zakat_Provider,BankInfo

class BankInfoForm(forms.ModelForm):
    class Meta:
        model = BankInfo
        fields = ['bank_name', 'mobile_bank_name', 'branch_name', 'account_number']

    def clean(self):
        cleaned_data = super().clean()
        bank_name = cleaned_data.get('bank_name')
        mobile_bank_name = cleaned_data.get('mobile_bank_name')

        if bank_name and mobile_bank_name:
            raise forms.ValidationError('You can only select either a bank or a mobile bank, not both.')
        if not bank_name and not mobile_bank_name:
            raise forms.ValidationError('You must select either a bank or a mobile bank.')

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
        fields = ['mosque', 'photo', 'name', 'phone_number', 'email', 'address', 'nid_no', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class QarjLoginForm(forms.Form):
    nid_no = forms.CharField(max_length=30, label='NID Number')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')



# qarrj hasana apply form

class QarrjHasanaApplyForm(forms.ModelForm):
    class Meta:
        model = Qarrj_Hasana_Apply
        fields = [
            'requested_amount_for_qarrj_hasana',
            'bank',
            'bank_account_number',
            'mobile_bank',
            'mobile_bank_number',
            'head_of_family_name',
            'total_members_boy',
            'total_members_girl',
            'total_workable_persons',
            'total_earnable_persons',
            'source_of_income',
            'total_monthly_income',
            'total_monthly_expense',
            'loan_amount',
            'monthly_savings_amount',
            'monthly_installment_amount',
            'total_unpaid_installment_amount',
            'have_bangla_translated_if_quran',
            'recite_quran_daily'
        ]


class ZakatProviderForm(forms.ModelForm):
    class Meta:
        model = Zakat_Provider
        fields = ['mosque', 'name', 'contact_number', 'address', 'donation_amount', 'transaction_screenshot']
