from django.contrib import admin
from decimal import Decimal
from .models import AdminInformation,HomePageModel,BannerModel,Global_Settings, Mosque,Bank, MobileBank,BankInfo, Qarrj_Hasana_Account,Qarrj_Hasana_Apply, Zakat_Provider,Zakat_Receiver,ImageCardBlog,EmployeeInfo,AboutUsBlock,TeamMemberBlock,Attendance
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from datetime import datetime, timedelta

class AdminInformationAdmin(admin.ModelAdmin):
    list_display = ('phone_number_primary', 'phone_number_secondery', 'email_address', 'website_link')
    search_fields = ('email_address', 'phone_number_primary', 'phone_number_secondery')
    list_filter = ('website_link',)

    fieldsets = (
        (None, {
            'fields': ('phone_number_primary', 'phone_number_secondery', 'email_address')
        }),
        ('Links', {
            'fields': ('facebook_link', 'linkedin_link', 'youtube_link', 'website_link')
        }),
        ('Address', {
            'fields': ('address',)
        }),
    )

    ordering = ('email_address',)

admin.site.register(AdminInformation, AdminInformationAdmin)

@admin.register(HomePageModel)
class HomePageModelAdmin(admin.ModelAdmin):
    list_display = ("admin_photo",)

@admin.register(BannerModel)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ("admin_photo",)
    

@admin.register(Global_Settings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('service_charge_percentage',)

class MosqueAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('id','mosque_id','mosque_name', 'village', 'district', 'thana', 'division', 'imam_name', 'imam_mobile_number', 'muazzin_name', 'muazzin_mobile_number')
    
    # Enable searching by these fields
    search_fields = ('mosque_name', 'village', 'district', 'imam_name','imam_mobile_number', 'muazzin_name', 'muazzin_mobile_number')

    # Add filters for the list view
    list_filter = ('division', 'district', 'thana')

admin.site.register(Mosque, MosqueAdmin)

# Register Bank model
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Mobile Bank model
@admin.register(MobileBank)
class MobileBankAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Bank Info model
@admin.register(BankInfo)
class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('get_bank_or_mobile_bank', 'branch_name', 'account_number')
    search_fields = ('account_number', 'branch_name', 'bank_name__name', 'mobile_bank_name__name')
    list_filter = ('bank_name', 'mobile_bank_name')

    def get_bank_or_mobile_bank(self, obj):
        if obj.bank_name:
            return obj.bank_name
        elif obj.mobile_bank_name:
            return obj.mobile_bank_name
        return 'N/A'

    get_bank_or_mobile_bank.short_description = 'Bank/Mobile Bank'

@admin.register(Qarrj_Hasana_Account)
class QarrjHasanaAccountAdmin(admin.ModelAdmin):
    list_display = ('id','admin_photo','name', 'mosque', 'phone_number', 'nid_no')
    search_fields = ('name', 'phone_number', 'nid_no')
    list_filter = ('mosque','mosque__district',)
    raw_mosque_name_fields = ('mosque',)
    



@admin.register(Qarrj_Hasana_Apply)
class QarrjHasanaApplyAdmin(admin.ModelAdmin):
    list_display = (
        'form_no','qarrj_hasana','requested_amount_for_qarrj_hasana',
        'total_monthly_income', 'total_monthly_expense','loan_amount',
        'total_unpaid_installment_amount','income_expense_diff_amount', 'bank_account_number','mobile_bank_number',
        'status', 'applied_on'  # Added fields
    )
    
    search_fields = (
        'form_no', 'requested_amount_for_qarrj_hasana','bank_account_number', 'mobile_bank_number', 
    )
    list_filter = (
        'qarrj_hasana__mosque', 'have_bangla_translated_if_quran', 'recite_quran_daily', 'status'  # Optionally add 'status' to filters
    )
    # readonly_fields = ('income_expense_diff_amount',)  # Make the calculated field read-only
    exclude = ('income_expense_diff_amount',)
    
    def get_readonly_fields(self, request, obj=None):
        # Optionally, make income_expense_diff_amount read-only only when editing
        if obj:
            return self.readonly_fields + ('form_no','income_expense_diff_amount',)  # Add form_no to readonly fields if needed
        return self.readonly_fields
    
def approve_qarj_application(request, application_id):
    application = Qarrj_Hasana_Apply.objects.get(id=application_id)
    application.status = 'approved'
    application.save()
    messages.success(request, 'Application approved successfully.')
    return redirect('admin_dashboard')  # Or wherever you want to redirect

# @admin.register(Zakat_Wallet)
# class ZakatWalletAdmin(admin.ModelAdmin):
#     list_display = ('mosque', 'total_amount', 'disbursable_amount', 'approved_zakat_holders_count','zakat_amount_for_each_person')
    
#     # Enable search functionality
#     search_fields = ('mosque__mosque_name', 'mosque__id')  # Search by mosque name

#     # Enable filters
#     list_filter = ('mosque__district', 'mosque__division')  # Filter by mosque's district and division
    
#     readonly_fields = ('total_amount', 'disbursable_amount', 'approved_zakat_holders_count', 'zakat_amount_for_each_person')

#     def has_add_permission(self, request):
#         # Prevent manual creation of Personal Zakat Wallets from the admin interface
#         return False

#     def has_delete_permission(self, request, obj=None):
#         # Prevent deletion of Personal Zakat Wallets from the admin interface
#         return False

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



class ZakatReceiverAdmin(admin.ModelAdmin):
    list_display = ('name', 'mosque', 'phone_number', 'nid_no', 'verification')
    search_fields = ('name', 'phone_number', 'nid_no', 'mosque__mosque_name')
    list_filter = ('verification', 'mosque__district')
    
    def save_model(self, request, obj, form, change):
        # Ensure that the save method logic in the model is respected
        super().save_model(request, obj, form, change)

# class PersonalZakatWalletAdmin(admin.ModelAdmin):
#     list_display = ('receiver', 'amount')
#     search_fields = ('receiver__name', 'receiver__mosque__mosque_name')
    
#     def has_add_permission(self, request):
#         # Prevent manual creation of Personal Zakat Wallets from the admin interface
#         return False

#     def has_delete_permission(self, request, obj=None):
#         # Prevent deletion of Personal Zakat Wallets from the admin interface
#         return False


admin.site.register(Zakat_Receiver, ZakatReceiverAdmin)
# admin.site.register(Personal_Zakat_Wallet, PersonalZakatWalletAdmin)


@admin.register(ImageCardBlog)
class ImageCardBlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)



@admin.register(EmployeeInfo)
class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display = ('emp_name','emp_DOB', 'emp_designation', 'emp_DOJ', 'emp_email','emp_pin', 'emp_phone')
    search_fields = ('emp_code', 'emp_name', 'emp_email')  # Fields to search in the admin
    list_filter = ('emp_designation', 'emp_DOJ')  # Add filter options in the admin
    ordering = ('emp_code',)  # Order by date of joining
    # readonly_fields = ('emp_code',)  # Make emp_code read-only in the admin

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing employee
            return self.readonly_fields + ('emp_code',)
        return self.readonly_fields



admin.site.register(AboutUsBlock)
admin.site.register(TeamMemberBlock)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('emp_code', 'emp_name', 'attd_date', 'in_time', 'out_time', 'total_workhour')
    list_filter = ('attd_date',)  # Filter by date
    search_fields = ('emp_code', 'emp_name')  # Search by employee code or name
    readonly_fields = ('total_workhour',)  # Make the total_workhour field read-only

    # Method to calculate total work hours
    def total_workhour(self, obj):
        if obj.out_time and obj.in_time:
            # Extract time from datetime fields
            in_time = obj.in_time.time()  # Ensure it's a time object
            out_time = obj.out_time.time()  # Ensure it's a time object
            # Combine with attd_date
            in_datetime = datetime.combine(obj.attd_date, in_time)
            out_datetime = datetime.combine(obj.attd_date, out_time)
            total_hours = out_datetime - in_datetime
            
            # Return total hours as a string (you can format this further if needed)
            return str(total_hours)
        return "N/A"

    total_workhour.short_description = "Total Work Hours"

# Register the model and the admin class
admin.site.register(Attendance, AttendanceAdmin)