from django.db import models
from decimal import Decimal

class Global_Settings(models.Model):
    service_charge_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Global Settings - Service Charge: {self.service_charge_percentage}%"

class Mosque(models.Model):
    mosque_name = models.CharField(max_length=255)  # Required by default
    
    # Address fields
    village = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255)
    thana = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    
    # Imam details (Required)
    imam_name = models.CharField(max_length=255)  # Required by default
    imam_mobile_number = models.CharField(max_length=15)
   
    # Muazzin details
    muazzin_name = models.CharField(max_length=255, blank=True, null=True)
    muazzin_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"#{self.id} - {self.mosque_name},{self.village},{self.district},{self.thana},{self.division}"



from django.db import models

# Bank Model
class Bank(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Mobile Bank Model
class MobileBank(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Qarrj_Hasana Model
class Qarrj_Hasana_Account(models.Model):
    mosque = models.ForeignKey(
        'Mosque',
        on_delete=models.CASCADE,
        related_name='qarrj_hasana_entries'
    )
    
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    nid_no = models.CharField(max_length=20)
    
    bank = models.ForeignKey(
        'Bank',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    
    mobile_bank = models.ForeignKey(
        'MobileBank',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    mobile_bank_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"#{self.id}-{self.name} ({self.mosque.mosque_name})"




class Qarrj_Hasana_Apply(models.Model):
    qarrj_hasana = models.ForeignKey(
        Qarrj_Hasana_Account,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    requested_amount_for_qarrj_hasana = models.PositiveBigIntegerField(default=0)
    
    form_no = form_no = models.AutoField(primary_key=True)
    
    head_of_family_name = models.CharField(max_length=255)
    total_members_boy = models.PositiveIntegerField(default=0)
    total_members_girl = models.PositiveIntegerField(default=0)
    total_workable_persons = models.PositiveIntegerField(default=0)
    total_earnable_persons = models.PositiveIntegerField(default=0)
    
    source_of_income = models.CharField(max_length=255)
    
    total_monthly_income = models.PositiveIntegerField(default=0)
    total_monthly_expense = models.PositiveIntegerField(default=0)

    loan_amount = models.DecimalField(max_digits=15, decimal_places=0)
    monthly_savings_amount = models.DecimalField(max_digits=15, decimal_places=0)
    monthly_installment_amount = models.DecimalField(max_digits=15, decimal_places=0)
    total_unpaid_installment_amount = models.DecimalField(max_digits=15, decimal_places=0)
    
    have_bangla_translated_if_quran = models.BooleanField(default=False)
    recite_quran_daily = models.BooleanField(default=False)
    
    income_expense_diff_amount = models.DecimalField(max_digits=15, decimal_places=0, editable=False, default=0.00)
    
    def save(self, *args, **kwargs):
        # Calculate the income-expense difference before saving
        self.income_expense_diff_amount = self.total_monthly_income - self.total_monthly_expense
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Application {self.form_no} - {self.qarrj_hasana.name}"
    



class Zakat_Wallet(models.Model):
    mosque = models.OneToOneField('Mosque', on_delete=models.CASCADE)  # Each mosque has one Zakat Wallet
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    @property
    def disbursable_amount(self):
        # Fetch the global settings
        global_settings = Global_Settings.objects.first()
        if not global_settings:
            return self.total_amount
        
        # Calculate disbursable amount using the global service charge percentage
        service_charge_percentage = global_settings.service_charge_percentage
        return self.total_amount - (self.total_amount * service_charge_percentage / Decimal(100))
    
    def __str__(self):
        return f"Zakat Wallet for {self.mosque.mosque_name}"
    
class Zakat_Provider(models.Model):
    mosque = models.ForeignKey('Mosque', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    donation_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    donation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - Donation: {self.donation_amount or 'No Donation'}"