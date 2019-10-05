from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from hansweb.views import home_view
from users.forms import RegistrationForm


def registration_view(request):
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


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            return redirect('account_view')
        else:
            messages.error(request, "Password change failed!")
    else:
        form = PasswordChangeForm(request.user, request.POST)
    return render(request, 'account/change_password.html', {'form': form})
