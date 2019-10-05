from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from hansweb.views import home_view
from users.forms import RegistrationForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect(home_view)
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})
