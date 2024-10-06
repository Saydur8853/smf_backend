from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mosque,HomePageModel,BannerModel
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm

# def home(request):
#     return render(request, 'index.html')
# def home(request):
#     home_page = HomePageModel.objects.last()  # Assuming there's only one record
#     return render(request, 'index.html', {'home_page': home_page})


# def banner_view(request):
#     banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 images
#     return render(request, 'index.html', {'banners': banners})
    
def home(request):
    home_page = HomePageModel.objects.last()  # Get the last record
    banners = BannerModel.objects.all().order_by('-id')[:5]  # Get the last 5 banners
    return render(request, 'index.html', {'home_page': home_page, 'banners': banners})


def about(request):
    return render(request, 'about.html')

def mosque_registration(request):
    if request.method == 'POST':
        form = MosqueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new mosque
            messages.success(request, 'Mosque registered successfully!')
            return redirect('mosque_registration')  # Redirect to the same page
        else:
            messages.error(request, 'Failed to register mosque. Please correct the errors.')
    else:
        form = MosqueRegistrationForm()

    context = {'form': form}
    return render(request, 'mosque/mosque_registration.html', context)



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