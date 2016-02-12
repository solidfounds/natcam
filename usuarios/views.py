from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Autentificacion Satisfactoria')
                else:
                    return HttpResponse('cuenta desabilitada')
            else:
                return HttpResponse('Logueo Invalido')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
