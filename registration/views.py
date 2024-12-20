from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.utils import timezone

from django.contrib.auth.hashers import check_password
from .models import Mosque,HomePageModel,BannerModel,Qarrj_Hasana_Account,Qarrj_Hasana_Apply,AdminInformation,BankInfo,ImageCardBlog,AboutUsBlock,TeamMemberBlock,EmployeeInfo,Attendance
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm, QarrjHasanaApplyForm,ZakatProviderForm,ZakatReceiverForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def home(request):
    home_page = HomePageModel.objects.last()  # Get the last record
    banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 banners
    admin_info = AdminInformation.objects.first()
    bank_info_list = BankInfo.objects.all()
    image_card_blogs = ImageCardBlog.objects.all()
    

    # Handle mosque registration form submission
    if request.method == 'POST' and 'mosque_submit' in request.POST:
        form = MosqueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mosque registered successfully!')
            return redirect('home')  # Redirect to the same page (home)
        else:
            messages.error(request, 'Failed to register mosque. Please correct the errors.')
    else:
        form = MosqueRegistrationForm()  # Initialize an empty form if GET request

    # Handle Qarj Hasana registration form submission
    qarj_form = QarrjHasanaAccountForm(request.POST, request.FILES) if request.method == 'POST' and 'qarj_submit' in request.POST else QarrjHasanaAccountForm()

    if qarj_form.is_valid():
        qarj_form.save()
        return redirect('home')  # Adjust as per your flow
    
    # Handle Zakat Provider form submission
    zakat_form = ZakatProviderForm(request.POST, request.FILES) if request.method == 'POST' and 'zakat_submit' in request.POST else ZakatProviderForm()

    if zakat_form.is_valid():
        zakat_form.save()
        messages.success(request, 'Zakat Provider data submitted successfully!')
        return redirect('home')
    elif request.method == 'POST' and 'zakat_submit' in request.POST:
        messages.error(request, 'Failed to submit Zakat Provider data. Please correct the errors.')

    # Handle Zakat Receiver form submission
    zakat_receiver_form = ZakatReceiverForm(request.POST or None)
    if request.method == 'POST' and 'zakat_receiver_submit' in request.POST and zakat_receiver_form.is_valid():
        zakat_receiver_form.save()
        messages.success(request, 'Zakat Receiver data submitted successfully!')
        return redirect('home')
    elif request.method == 'POST' and 'zakat_receiver_submit' in request.POST:
        messages.error(request, 'Failed to submit Zakat Receiver data. Please correct the errors.')


    # Handle Qarj Hasana login
    if request.method == 'POST' and 'login_submit' in request.POST:
        nid_no = request.POST.get('nid_no')
        password = request.POST.get('password')

        try:
            # Attempt to find the user by NID
            account = Qarrj_Hasana_Account.objects.get(nid_no=nid_no)

            # Check password validity
            if check_password(password, account.password):
                # Store the user's name in the session
                request.session['logged_in_user'] = account.name
                request.session['logged_in_nid'] = account.nid_no

                messages.success(request, f'Logged in successfully as {account.name}')
                return redirect('dashboard')  # Redirect to the dashboard page after successful login
            else:
                messages.error(request, 'Invalid NID or password.')
        except Qarrj_Hasana_Account.DoesNotExist:
            messages.error(request, 'No account found with this NID.')

    context = {
        'home_page': home_page,
        'banners': banners,
        'form': form,  # Mosque registration form
        'qarj_form': qarj_form,  # Qarj Hasana registration form
        'zakat_form': zakat_form,  # Zakat Provider form
        'zakat_receiver_form': zakat_receiver_form, # Zakat receiver form
        'admin_info': admin_info,
        'bank_info_list': bank_info_list,
        'image_card_blogs': image_card_blogs,
    }

    return render(request, 'index.html', context)

def dashboard(request):
    # Check if the user is logged in
    logged_in_user = request.session.get('logged_in_user')
    logged_in_nid = request.session.get('logged_in_nid')

    if not logged_in_nid:
        return redirect('home')  # Redirect to the home page if not logged in

    # Retrieve the logged-in user's account using `nid_no`
    account = Qarrj_Hasana_Account.objects.get(nid_no=logged_in_nid)

    # Retrieve the most recent application for the user
    recent_application = Qarrj_Hasana_Apply.objects.filter(qarrj_hasana=account).order_by('-applied_on').first()
    has_pending_application = recent_application and recent_application.status == 'pending'

    # Initialize the status variable
    status = ""

    if has_pending_application:
        # Include the requested amount for the pending application
        status = f"Your application status is: {recent_application.get_status_display()} for {recent_application.requested_amount_for_qarrj_hasana} taka."
    elif recent_application:
        status = f"Your application status is: {recent_application.get_status_display()}  for {recent_application.requested_amount_for_qarrj_hasana} taka."
    else:
        status = "No applications found."

    # Handle Qarj Hasana Apply form submission
    if request.method == 'POST' and 'qarj_apply_submit' in request.POST:
        if has_pending_application:
            messages.error(request, 'You cannot apply again while you have a pending application.')
            return redirect('dashboard')  # Redirect to refresh the dashboard
        
        qarj_apply_form = QarrjHasanaApplyForm(request.POST)
        if qarj_apply_form.is_valid():
            qarj_apply_instance = qarj_apply_form.save(commit=False)
            qarj_apply_instance.qarrj_hasana = account  # Link the application to the logged-in user's account
            qarj_apply_instance.save()
            messages.success(request, 'Qarj Hasana Application submitted successfully!')
            return redirect('dashboard')  # Redirect to refresh the dashboard
        else:
            messages.error(request, 'Failed to submit the application. Please correct the errors.')
    else:
        qarj_apply_form = QarrjHasanaApplyForm()  # Initialize an empty form

    context = {
        'logged_in_user': account.name,  # Pass the logged-in user's name to the dashboard
        'user_photo': account.photo.url if account.photo else None,  # Pass the user's photo URL or None if not available
        'associate_mosque': account.mosque,
        'phone_number': account.phone_number,
        'nid': account.nid_no,
        'qarj_apply_form': qarj_apply_form,
        'has_pending_application': has_pending_application,
        'status': status,  # Now the status is defined
    }

    return render(request, 'dashboard.html', context)




def logout_view(request):
    # Get the logged-in user's name before logging them out
    logged_in_user = request.session.get('logged_in_user')
    # Add a success message after logout
    if logged_in_user:
        messages.success(request, f'Logged out successfully as {logged_in_user}')
    # Redirect to the home page
    return redirect('home')


def about(request):
    admin_info = AdminInformation.objects.first()
    about_content = AboutUsBlock.objects.first()
    team_members = TeamMemberBlock.objects.all()

    context = {
        'admin_info': admin_info,
        'about_content': about_content,
        'team_members': team_members, 
        
    }
    return render(request, 'about.html', context)


def attendance(request):
    admin_info = AdminInformation.objects.first()
    about_content = AboutUsBlock.objects.first()
    employees = EmployeeInfo.objects.all()

    if request.method == 'POST':
        user = request.POST.get('user')
        psw = request.POST.get('psw')

        try:
            employee = EmployeeInfo.objects.get(emp_email=user, emp_pin=psw)
            request.session['emp_code'] = employee.emp_code
            request.session['emp_name'] = employee.emp_name
            request.session['emp_email'] = employee.emp_email
            request.session['emp_phone'] = employee.emp_phone
            request.session['emp_designation'] = employee.emp_designation
            request.session['emp_photo'] = employee.photo.url  # Store the URL of the photo

            return redirect('success_page')  # Redirect to success page
        except EmployeeInfo.DoesNotExist:
            messages.error(request, None)

    context = {
        'admin_info': admin_info,
        'about_content': about_content,
        'employees': employees,
    
        
    }
    return render(request, 'attendance.html', context)

@csrf_exempt
def success_page(request):
    # Retrieve employee data from session
    emp_data = {
        'emp_code': request.session.get('emp_code'),
        'emp_name': request.session.get('emp_name'),
        'emp_email': request.session.get('emp_email'),
        'emp_phone': request.session.get('emp_phone'),
        'emp_designation': request.session.get('emp_designation'),
        'emp_photo': request.session.get('emp_photo'),
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'check_in':
            # Create a new attendance record with the current datetime
            attendance, created = Attendance.objects.get_or_create(
                emp_code=emp_data['emp_code'],
                attd_date=timezone.now().date(),  # Use current date for attendance
                defaults={
                    'emp_name': emp_data['emp_name'],
                    'in_time': timezone.now(),  # Use current datetime
                }
            )
            return JsonResponse({'status': 'checked_in', 'in_time': attendance.in_time})

        elif action == 'sign_out':
            # Update the out_time for the attendance record of the current day
            try:
                attendance = Attendance.objects.get(emp_code=emp_data['emp_code'], attd_date=timezone.now().date())
                attendance.out_time = timezone.now()  # Use current datetime
                attendance.save()
                return JsonResponse({'status': 'signed_out', 'out_time': attendance.out_time})
            except Attendance.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Check-in record not found'}, status=400)

    return render(request, 'success.html', {'employee': emp_data})


def search_mosques(request):
    query = request.GET.get('q', '').strip()
    if query:
        mosques = Mosque.objects.filter(mosque_name__icontains=query)
    else:
        mosques = Mosque.objects.all()
    
    mosque_list = [{
        'id': mosque.id,
        'mosque_name': mosque.mosque_name,
        'mosque_id': mosque.mosque_id,
        'village': mosque.village,
        'district': mosque.district,
        'thana': mosque.thana,
        'division': mosque.division,
        # 'imam_name': mosque.imam_name,
        # 'muazzin_name': mosque.muazzin_name,
        # 'imam_mobile_number': mosque.imam_mobile_number,
        # 'muazzin_mobile_number': mosque.muazzin_mobile_number,
    } for mosque in mosques]
    
    return JsonResponse(mosque_list, safe=False)
