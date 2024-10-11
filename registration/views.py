from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mosque,HomePageModel,BannerModel
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm
  

def home(request):
    home_page = HomePageModel.objects.last()  # Get the last record
    banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 banners

    # Handle mosque registration form submission
    if request.method == 'POST' and 'mosque_submit' in request.POST:
        form = MosqueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mosque registered successfully!')
            return redirect('home')  # Redirect to the same page (home)
        else:
            messages.error(request, 'Failed to register mosque. Please correct the errors.')
            print(form.errors)
    else:
        form = MosqueRegistrationForm()  # Initialize an empty form if GET request

    # Handle Qarj Hasana registration form submission
    qarj_form = QarrjHasanaAccountForm(request.POST, request.FILES) if request.method == 'POST' and 'qarj_submit' in request.POST else QarrjHasanaAccountForm()

    if qarj_form.is_valid():
        qarj_form.save()
        return redirect('home')  # Adjust as per your flow

    # Pass all context data to the template
    context = {
        'home_page': home_page,
        'banners': banners,
        'form': form,  # Mosque registration form
        'qarj_form': qarj_form,  # Qarj Hasana registration form
    }

    return render(request, 'index.html', context)  


def about(request):
    return render(request, 'about.html')


