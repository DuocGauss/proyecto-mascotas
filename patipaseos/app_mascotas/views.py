from django.shortcuts import render, redirect, get_object_or_404
from .models import Propietario, Cuidador, Servicio, Mascota, DetPrestacion
from .forms import frmRegistro, frmLogin, frmCuidador, frmEdit, frmServicio, frmMascota, frmDetPrestacion
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def index(request):
    default_page = 1
    page = request.GET.get('page', default_page)

    obtener = Servicio.objects.all()
    
    query = request.GET.get('q')  # Obtener el término de búsqueda del request
    
    if query:
        # Filtrar mantenciones en función de la búsqueda
        obtener = obtener.filter(
            Q(tipo_servicio__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(precio__icontains=query) |
            Q(cuidador__especializacion__icontains=query) |
            Q(cuidador__propietario__username__icontains=query)  
        )

    items_per_page = 3  # Ajusta el número de elementos por página según tus necesidades
    paginator = Paginator(obtener, items_per_page)

    try:
        obtener = paginator.page(page)
    except PageNotAnInteger:
        obtener = paginator.page(default_page)
    except EmptyPage:
        obtener = paginator.page(paginator.num_pages)

    contexto = {
        'obtener': obtener,
    }
    return render(request, 'app_mascotas/index.html', contexto)



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
    cuidador_data = None 
    form_mascota = frmMascota() 
    if request.method == 'POST':
        form_mascota = frmMascota(request.POST, request.FILES)
        if form_mascota.is_valid():
            nueva_mascota = form_mascota.save(commit=False)
            nueva_mascota.propietario = request.user  # Asigna el propietario de la mascota
            nueva_mascota.save()
            messages.success(request, 'Mascota agregada con éxito.')
            return redirect('perfil')
    else:
        form_mascota = frmMascota()
    mascotas_usuario = Mascota.objects.filter(propietario=request.user)
    check = Propietario.objects.filter(pk=request.user.id)
    if len(check) > 0:
        data = Propietario.objects.get(pk=request.user.id)
        context["data"] = data
        # Verificar si el usuario es también un cuidador
        if data.es_cuidador:
            cuidador_data = Cuidador.objects.filter(propietario=data).first()
            servicios = Servicio.objects.filter(cuidador=cuidador_data)
            context["cuidador_data"] = cuidador_data
            context["servicios"] = servicios
            context["cuidador_data"] = cuidador_data
    else:
        data = None
    context["mascotas_usuario"] = mascotas_usuario 
    context["form_mascota"] = form_mascota

    return render(request, "app_mascotas/perfil.html", context)




@login_required
def editar_perfil(request,id):
    us = request.user
    print(us)
    user_role = request.session.get('user_role', None)
    form=frmEdit(instance=us)
    contexto={
        "form":form,
        "user_role": user_role,
    }

    if request.method=="POST":
        form=frmEdit(data=request.POST,files=request.FILES,instance=us)
        #form.fields["id"].disabled=False
        if form.is_valid():
            us_buscado=Propietario.objects.get(id=us.id)
            datos_form=form.cleaned_data
            us_buscado.username=datos_form.get("username")
            us_buscado.first_name=datos_form.get("first_name")
            us_buscado.last_name=datos_form.get("last_name")
            us_buscado.email=datos_form.get("email")
            us_buscado.telefono=datos_form.get("telefono")
            us_buscado.direccion=datos_form.get("direccion")
            us_buscado.imagen=datos_form.get("imagen")
            us_buscado.save()
            messages.success(request,"Información Modificada!")
            return redirect(to="perfil")
        contexto["form"]=form
        
    return render(request,"app_mascotas/editar_perfil.html",contexto)



@login_required
def servicio(request):
    form=frmServicio(request.POST or None)
    contexto={
        "form":form
    }
    if request.method=="POST":
        form=frmServicio(data=request.POST,files=request.FILES)
        if form.is_valid():
           servicio = form.save(commit=False)
           cuidador = Cuidador.objects.get(propietario=request.user)
           servicio.cuidador_id = cuidador.id_cuidador
           servicio.save()
           messages.success(request,"Servicio Publicado!")

           return redirect(to="index")
       
    return render(request,"app_mascotas/servicio.html",contexto)



def perfil_servicio(request, id_servicio):
    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)
    cuidador = servicio.cuidador
    propietario = cuidador.propietario
    obtener = Servicio.objects.filter(cuidador=cuidador)
    mascotas_usuario = Mascota.objects.filter(propietario=propietario)

    contexto = {
        'servicio': servicio,
        'cuidador': cuidador,
        'propietario': propietario,
        'obtener': obtener,
        'mascotas_usuario': mascotas_usuario,
    }
    return render(request, 'app_mascotas/perfil_servicio.html', contexto)



@login_required
def eliminar_servicio(request,id):
    v=get_object_or_404(Servicio,pk=id)
    if request.method=="POST":
        v.delete()
        messages.success(request,"Servicio Eliminado!")
        return redirect(to="perfil")
    
    
@login_required
def modificar_servicio(request,id_servicio):
    prod=get_object_or_404(Servicio,pk=id_servicio)
    form=frmServicio(instance=prod)
    #form.fields["id"].disabled=True
    contexto={
        "form":form
    }

    if request.method=="POST":
        form=frmServicio(data=request.POST,files=request.FILES,instance=prod)
        #form.fields["id"].disabled=False
        if form.is_valid():
            search=Servicio.objects.get(pk=prod.id_servicio)
            datos_form=form.cleaned_data
            search.tipo_servicio=datos_form.get("tipo_servicio")
            search.descripcion=datos_form.get("descripcion")
            search.precio=datos_form.get("precio")
            search.save()
            messages.success(request,"Servicio Modificado!")
            return redirect(to="perfil")
        contexto["form"]=form
        
    return render(request,"app_mascotas/mod_servicio.html",contexto)



@login_required
def eliminar_mascota(request,id):
    v=get_object_or_404(Mascota,pk=id)
    if request.method=="POST":
        v.delete()
        messages.success(request,"Mascota Eliminada!")
        return redirect(to="perfil")




@login_required
def modificar_mascota(request,id_mascota):
    prod=get_object_or_404(Mascota,pk=id_mascota)
    form=frmMascota(instance=prod)
    #form.fields["id"].disabled=True
    contexto={
        "form":form
    }

    if request.method=="POST":
        form=frmMascota(data=request.POST,files=request.FILES,instance=prod)
        #form.fields["id"].disabled=False
        if form.is_valid():
            search=Mascota.objects.get(pk=prod.id_mascota)
            datos_form=form.cleaned_data
            search.nombre_mascota=datos_form.get("nombre_mascota")
            search.tipo_mascota=datos_form.get("tipo_mascota")
            search.tamaño_mascota=datos_form.get("tamaño_mascota")
            search.raza_mascota=datos_form.get("raza_mascota")
            search.imagen=datos_form.get("imagen")
            search.save()
            messages.success(request,"Servicio Modificado!")
            return redirect(to="perfil")
        contexto["form"]=form
        
    return render(request,"app_mascotas/mod_mascota.html",contexto)



def detalle_prestacion(request, id_servicio):
    servicio = Servicio.objects.get(pk=id_servicio)
    user = request.user
    propietario = servicio.cuidador.propietario

    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        if request.method == "POST":
            form = frmDetPrestacion(user, servicio.precio, data=request.POST, files=request.FILES)
            if form.is_valid():
                detalle_prestacion = form.save(commit=False)
                form.instance.id_servicio = servicio
                form.instance.id_propietario = request.user  # Propietario actual
                form.instance.id_cuidador = servicio.cuidador
                detalle_prestacion.save()
                messages.success(request, "Servicio solicitado!")
                return redirect("prestacion")
        else:
            form = frmDetPrestacion(user, servicio.precio)

        context = {
            "servicio": servicio,
            "form": form,
            "propietario": propietario,
        }

        return render(request, "app_mascotas/detalle_prestacion.html", context)
    else:
        # Si el usuario no está autenticado, redirigir al login
        return redirect(to="login_custom")




@login_required
def prestacion(request):
    cuidador = None

    try:
        cuidador = Cuidador.objects.get(propietario=request.user)
    except Cuidador.DoesNotExist:
        cuidador = None

    # Obtener todas las prestaciones relacionadas con el cuidador si existe
    prestaciones_cuidador = DetPrestacion.objects.filter(id_cuidador=cuidador) if cuidador else []

    # Obtener todas las prestaciones relacionadas con el propietario (cliente)
    prestaciones_cliente = DetPrestacion.objects.filter(id_propietario=request.user)
    
    if request.method == 'POST':
        # Obtener el ID de la prestación que se quiere cambiar
        id = request.POST.get('id')

        # Buscar la prestación
        prestacion = get_object_or_404(DetPrestacion, id=id)

        # Verificar que la prestación está pendiente antes de cambiar el estado
        if prestacion.estado == 'Pendiente':
            # Cambiar el estado de la prestación a 'Activo'
            prestacion.estado = 'Activo'
            prestacion.save()
        elif prestacion.estado == 'Activo':
            # Cambiar el estado de la prestación a 'Finalizado'
            prestacion.estado = 'Finalizado'
            prestacion.save()

    return render(request, 'app_mascotas/prestacion.html', {'prestaciones_cuidador': prestaciones_cuidador, 'prestaciones_cliente': prestaciones_cliente, 'cuidador': cuidador})
