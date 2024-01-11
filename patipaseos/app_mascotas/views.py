from django.shortcuts import render, redirect
from .models import Propietario, Cuidador
from .forms import frmRegistro, frmLogin, frmCuidador
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


@login_required
def cuidador(request):
    form=frmCuidador(request.POST or None)
    contexto={
        "form":form
    }
    if request.method=="POST":
        form=frmCuidador(data=request.POST,files=request.FILES)
        if form.is_valid():
           propietario = request.user  # Suponiendo que el usuario actual está autenticado
           cuidador = form.save(commit=False)
           cuidador.propietario = propietario
           form.save()
           # Actualizar es_cuidador a True
           propietario.es_cuidador = True
           propietario.save()
           messages.success(request,"Registrado como Cuidador!")

           return redirect(to="index")
       
    return render(request,"app_mascotas/cuidador.html",contexto)



@login_required
def perfil(request):
    context = {}
    check = Propietario.objects.filter(pk=request.user.id)
    if len(check) > 0:
        data = Propietario.objects.get(pk=request.user.id)
        context["data"] = data
        # Verificar si el usuario es también un cuidador
        if data.es_cuidador:
            cuidador_data = Cuidador.objects.filter(propietario=data).first()
            context["cuidador_data"] = cuidador_data
    else:
        data = None  # Define data como None si el usuario no existe

    contexto = {
        'data': data, 
        'cuidador_data': cuidador_data if data and data.es_cuidador else None,  # Define cuidador_data como None si el usuario no es cuidador
    }
    return render(request, "app_mascotas/perfil.html", contexto)
