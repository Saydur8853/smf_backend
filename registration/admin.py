from django.contrib import admin
from decimal import Decimal
from .models import Global_Settings, Mosque,Bank, MobileBank, Qarrj_Hasana_Account,Qarrj_Hasana_Apply,Zakat_Wallet, Zakat_Provider


@admin.register(Global_Settings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('service_charge_percentage',)

class MosqueAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('id','mosque_name', 'village', 'district', 'thana', 'division', 'imam_name', 'imam_mobile_number', 'muazzin_name', 'muazzin_mobile_number')
    
    # Enable searching by these fields
    search_fields = ('mosque_name', 'village', 'district', 'imam_name','imam_mobile_number', 'muazzin_name', 'muazzin_mobile_number')

    # Add filters for the list view
    list_filter = ('division', 'district', 'thana')

admin.site.register(Mosque, MosqueAdmin)

admin.site.register(Bank)
admin.site.register(MobileBank)

@admin.register(Qarrj_Hasana_Account)
class QarrjHasanaAccountAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'mosque', 'phone_number', 'nid_no', 'bank', 'mobile_bank')
    search_fields = ('name', 'phone_number', 'nid_no')
    list_filter = ('mosque__district', 'bank', 'mobile_bank')
    raw_mosque_name_fields = ('mosque',)
    



@admin.register(Qarrj_Hasana_Apply)
class QarrjHasanaApplyAdmin(admin.ModelAdmin):
    list_display = (
        'form_no', 'qarrj_hasana', 'head_of_family_name', 'total_members_boy', 
        'total_members_girl', 'total_workable_persons', 'total_earnable_persons',
        'source_of_income', 'total_monthly_income', 'total_monthly_expense',
        'loan_amount', 'monthly_savings_amount', 'monthly_installment_amount',
        'total_unpaid_installment_amount', 'have_bangla_translated_if_quran',
        'recite_quran_daily', 'income_expense_diff_amount'
    )
    search_fields = (
        'form_no', 'head_of_family_name', 'source_of_income', 'loan_amount',
        'monthly_savings_amount', 'monthly_installment_amount', 'total_unpaid_installment_amount'
    )
    list_filter = (
        'qarrj_hasana__mosque', 'have_bangla_translated_if_quran', 'recite_quran_daily'
    )
    # readonly_fields = ('income_expense_diff_amount',)  # Make the calculated field read-only
    exclude = ('income_expense_diff_amount',)
    
    def get_readonly_fields(self, request, obj=None):
        # Optionally, make income_expense_diff_amount read-only only when editing
        if obj:
            return self.readonly_fields + ('form_no',)  # Add form_no to readonly fields if needed
        return self.readonly_fields
    


@admin.register(Zakat_Wallet)
class ZakatWalletAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'total_amount', 'disbursable_amount')
    # Enable search functionality
    search_fields = ('mosque__mosque_name','mosque__id')  # Search by mosque name

    # Enable filters
    list_filter = ('mosque__district', 'mosque__division')  # Filter by mosque's district and division
    
    readonly_fields = ('total_amount', 'disbursable_amount')

class ZakatProviderAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'name', 'contact_number', 'donation_amount', 'donation_date')
    search_fields = ('name', 'contact_number', 'mosque__mosque_name')
    list_filter = ('mosque__district', 'donation_date')

    def save_model(self, request, obj, form, change):
        # Call the parent save method to handle the rest of the save operation
        super().save_model(request, obj, form, change)
        
        # Get or create the Zakat Wallet for the specific mosque
        zakat_wallet, created = Zakat_Wallet.objects.get_or_create(mosque=obj.mosque)
        
        # Ensure total_amount is treated as Decimal
        zakat_wallet.total_amount = Decimal(zakat_wallet.total_amount)
        
        if obj.donation_amount and obj.donation_amount > Decimal('0.00'):
            # Only add donation amount if it's a new entry or if donation_amount has changed
            if not change or (obj.donation_amount and obj.donation_amount > Decimal('0.00')):
                zakat_wallet.total_amount += obj.donation_amount
                zakat_wallet.save()

admin.site.register(Zakat_Provider, ZakatProviderAdmin)