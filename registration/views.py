from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mosque,HomePageModel,BannerModel
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm
  
def home(request):
    home_page = HomePageModel.objects.last()  # Get the last record
    banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 banners
    # Handle mosque registration form submission
    if request.method == 'POST':
        form = MosqueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new mosque
            messages.success(request, 'Mosque registered successfully!')
            return redirect('home')  # Redirect to the same page (home)
        else:
            messages.error(request, 'Failed to register mosque. Please correct the errors.')
            print(form.errors)
    else:
        form = MosqueRegistrationForm()  # Initialize an empty form if GET request

    # Pass all context data to the template
    context = {
        'home_page': home_page,
        'banners': banners,
        'form': form,  # Add the mosque registration form to the context
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')



def qarrj_hasana_register(request):
    if request.method == 'POST':
        form = QarrjHasanaAccountForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or the same page with a success message
            return redirect('qarrj_hasana_success')
    else:
        form = QarrjHasanaAccountForm()
    
    return render(request, 'qarrj_hasana_register.html', {'form': form})