from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mosque
from .forms import MosqueRegistrationForm, QarrjHasanaAccountForm

def home(request):
    return render(request, 'home.html')

    
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