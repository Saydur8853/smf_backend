from django.db import models
from decimal import Decimal
from django.contrib.auth.hashers import make_password
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.exceptions import ValidationError  

class AdminInformation(models.Model):
    phone_number_primary = models.CharField(max_length=20)
    phone_number_secondery = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(max_length=254, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Admin Info: {self.phone_number_primary} - {self.phone_number_secondery} - {self.email_address}"

class HomePageModel(models.Model):
    smf_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.smf_logo.url))
    admin_photo.short_description = 'Image'
    admin_photo.allow_tags= True
    

    def __str__(self):
        return self.smf_logo.name.split('/')[-1] if self.smf_logo else "No logo uploaded"

class BannerModel(models.Model):
    banner_image = models.ImageField(upload_to='banner/', blank=True, null=True)

    def admin_photo(self):
        if self.banner_image:
            return mark_safe(
                f'<img src="{self.banner_image.url}" width="300" height="170" '
                f'style="margin-right: 2px; border: 2px solid green;"/>'
            )
        return "No image"

    admin_photo.short_description = 'Image'

    def __str__(self):
        return self.banner_image.name.split('/')[-1] if self.banner_image else "No image uploaded"


class Global_Settings(models.Model):
    service_charge_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Global Settings - Service Charge: {self.service_charge_percentage}%"


class Mosque(models.Model):
    mosque_id = models.CharField(max_length=10, editable=False, unique=True, blank=True)  # Unique mosque ID
    mosque_name = models.CharField(max_length=255)  # Required by default
    
    # Address fields
    village = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    thana = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    
    # Imam details (Required)
    imam_name = models.CharField(max_length=255)  # Required by default
    imam_mobile_number = models.CharField(max_length=15)
   
    # Muazzin details
    muazzin_name = models.CharField(max_length=255, blank=True, null=True)
    muazzin_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.mosque_id:
            # Generate mosque_id
            last_mosque = Mosque.objects.order_by('id').last()
            if last_mosque:
                last_id = int(last_mosque.mosque_id[1:])  # Remove 'M' and convert to int
                new_id = last_id + 1
            else:
                new_id = 1
            self.mosque_id = f"M{new_id:03d}"  # Format as M001, M002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.mosque_id} - {self.mosque_name},{self.village},{self.district},{self.thana},{self.division}"


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

# Bank Info model
class BankInfo(models.Model):
    bank_name = models.ForeignKey(Bank, null=True, blank=True, on_delete=models.SET_NULL)
    mobile_bank_name = models.ForeignKey(MobileBank, null=True, blank=True, on_delete=models.SET_NULL)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=50)

    def __str__(self):
        if self.bank_name:
            return f'{self.bank_name} - {self.branch_name}'
        elif self.mobile_bank_name:
            return f'{self.mobile_bank_name}'
        return 'Bank Info'

    def get_branch_name(self):
        """Returns 'Mobile Banking' if it's a mobile bank, else returns the branch name."""
        if self.mobile_bank_name:
            return "Mobile Banking"
        return self.branch_name or ""

    def clean(self):
        """Custom validation to ensure that only one of bank_name or mobile_bank_name is selected."""
        if self.bank_name and self.mobile_bank_name:
            raise ValidationError('You can only select either a bank or a mobile bank, not both.')
        if not self.bank_name and not self.mobile_bank_name:
            raise ValidationError('You must select either a bank or a mobile bank.')

    class Meta:
        verbose_name = 'Bank Info'
        verbose_name_plural = 'Bank Info'


class Qarrj_Hasana_Account(models.Model):
    mosque = models.ForeignKey(
        'Mosque',
        on_delete=models.CASCADE,
        related_name='qarrj_hasana_entries'
    )
    photo = models.ImageField(upload_to='q_hasana_profile/', blank=True, null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=80, blank=True, null=True)
    address = models.CharField(max_length=255)
    nid_no = models.CharField(max_length=30, unique=True)  # Unique constraint added
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"#{self.id}-{self.name} ({self.mosque.mosque_name})"
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Qarrj_Hasana_Account, self).save(*args, **kwargs)

    def admin_photo(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.photo.url}" width="50" height="50" '
            )
        return "No image"

    admin_photo.short_description = 'Image'



class Qarrj_Hasana_Apply(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('close', 'close'),
    ]
    qarrj_hasana = models.ForeignKey(
        Qarrj_Hasana_Account,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    requested_amount_for_qarrj_hasana = models.PositiveBigIntegerField()
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

    
    form_no = form_no = models.AutoField(primary_key=True)
    
    head_of_family_name = models.CharField(max_length=255)
    total_members_boy = models.PositiveIntegerField()
    total_members_girl = models.PositiveIntegerField()
    total_workable_persons = models.PositiveIntegerField()
    total_earnable_persons = models.PositiveIntegerField()
    
    source_of_income = models.CharField(max_length=255)
    
    total_monthly_income = models.PositiveIntegerField()
    total_monthly_expense = models.PositiveIntegerField()

    loan_amount = models.DecimalField(max_digits=15, decimal_places=0)
    monthly_savings_amount = models.DecimalField(max_digits=15, decimal_places=0)
    monthly_installment_amount = models.DecimalField(max_digits=15, decimal_places=0)
    total_unpaid_installment_amount = models.DecimalField(max_digits=15, decimal_places=0)
    
    have_bangla_translated_if_quran = models.BooleanField(default=False)
    recite_quran_daily = models.BooleanField(default=False)
    
    income_expense_diff_amount = models.DecimalField(max_digits=15, decimal_places=0, editable=False,)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Default to 'Pending'
    applied_on = models.DateTimeField(auto_now_add=True)
    transaction_screenshot = models.ImageField(upload_to='qarrj_transaction_screenshots/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the income-expense difference before saving
        self.income_expense_diff_amount = self.total_monthly_income - self.total_monthly_expense
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Application for {self.requested_amount_for_qarrj_hasana} - {self.status}- {self.applied_on}"
    



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
    
    @property
    def approved_zakat_holders_count(self):
        # Count the number of approved Zakat_Receiver for this mosque
        return Zakat_Receiver.objects.filter(mosque=self.mosque, verification=True).count()
    
    @property
    def zakat_amount_for_each_person(self):
        # Calculate zakat amount for each person
        if self.approved_zakat_holders_count > 0:
            return self.disbursable_amount / self.approved_zakat_holders_count
        return Decimal('0.00')
    
    def __str__(self):
        return f"Zakat Wallet for {self.mosque.mosque_name}"
    
class Zakat_Provider(models.Model):
    mosque = models.ForeignKey('Mosque', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    donation_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    transaction_screenshot = models.ImageField(upload_to='zakat_provider_trs_ss/', blank=True, null=True)
    donation_date = models.DateField(auto_now_add=True)
   
    
    def __str__(self):
        return f"{self.name} - Donation: {self.donation_amount or 'No Donation'}"
    


class Zakat_Receiver(models.Model):
    mosque = models.ForeignKey('Mosque', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
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
    
    form_no = models.AutoField(primary_key=True)
    
    head_of_family_name = models.CharField(max_length=255, blank=True, null=True)
    total_members_boy = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_members_girl = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_workable_persons = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_earnable_persons = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    source_of_income = models.CharField(max_length=255, blank=True, null=True)
    
    total_monthly_income = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_monthly_expense = models.PositiveIntegerField(default=0, blank=True, null=True)

    loan_amount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    monthly_savings_amount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    monthly_installment_amount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    total_unpaid_installment_amount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    
    have_bangla_translated_if_quran = models.BooleanField(default=False)
    recite_quran_daily = models.BooleanField(default=False)
    
    income_expense_diff_amount = models.DecimalField(max_digits=15, decimal_places=0, editable=False, default=0.00, blank=True, null=True)
    note = models.CharField(max_length=300, blank=True, null=True)
    
    verification = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate the income-expense difference before saving
        self.income_expense_diff_amount = self.total_monthly_income - self.total_monthly_expense
        
        # Handle verification and distribute zakat funds
        if self.verification:
            # Get the mosque's zakat wallet
            
            
            # Get all verified receivers for this mosque
            verified_receivers = Zakat_Receiver.objects.filter(mosque=self.mosque, verification=True)
            total_receivers = verified_receivers.count()
            
            if total_receivers > 0:
                mosque_wallet = Zakat_Wallet.objects.get(mosque=self.mosque)
                # Calculate the share for each receiver
                share_amount = mosque_wallet.disbursable_amount / total_receivers
                
                # Create or update the personal zakat wallet for this receiver
                personal_wallet, created = Personal_Zakat_Wallet.objects.get_or_create(receiver=self)
                personal_wallet.amount = share_amount
                personal_wallet.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.form_no} - {self.name} ({self.mosque.mosque_name})"

class Personal_Zakat_Wallet(models.Model):
    receiver = models.OneToOneField('Zakat_Receiver', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    @property
    def amount(self):
        # Fetch the Zakat_Wallet for the receiver's mosque
        zakat_wallet = Zakat_Wallet.objects.filter(mosque=self.receiver.mosque).first()
        if zakat_wallet:
            return zakat_wallet.zakat_amount_for_each_person
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        # Set the amount to zakat_amount_for_each_person before saving
        self.amount = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Personal Zakat Wallet for {self.receiver.name} - Amount: {self.amount}"