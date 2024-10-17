from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Mosque,HomePageModel,BannerModel,Qarrj_Hasana_Account,Qarrj_Hasana_Apply,AdminInformation,BankInfo
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm, QarrjHasanaApplyForm,ZakatProviderForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def home(request):
    home_page = HomePageModel.objects.last()  # Get the last record
    banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 banners
    admin_info = AdminInformation.objects.first()
    bank_info_list = BankInfo.objects.all()
    

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
        'admin_info': admin_info,
        'bank_info_list': bank_info_list,
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
    return render(request, 'about.html')