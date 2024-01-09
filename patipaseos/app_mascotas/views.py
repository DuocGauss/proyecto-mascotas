from django.shortcuts import render, redirect
from .forms import frmRegistro, frmLogin
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'app_mascotas/index.html')



def registro(request):
    if request.method == 'POST':
        form = frmRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user.save()
            messages.success(request,"Cuenta creada!")
            return redirect('index')  # Redirigir a la página de inicio después del registro
    else:
        form = frmRegistro()
    
    contexto = {
        'form': form,
    }
        
    return render(request, 'registration/registro.html', contexto)


def login_custom(request):
    if request.method == 'POST':
        form = frmLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirigir a la página de inicio después de iniciar sesión
    else:
        form = frmLogin()
    
    return render(request, 'registration/login_custom.html', {'form': form})


def logout_custom(request):
    logout(request)
    return redirect('index')