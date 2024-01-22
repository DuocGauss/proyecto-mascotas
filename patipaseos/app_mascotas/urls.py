from django.urls import path, include
from . import views





urlpatterns = [
    path("", views.index, name="index"),
    path('registro/',views.registro, name='registro'),
    path('login_custom/', views.login_custom, name='login_custom'),
    path('logout_custom/', views.logout_custom, name='logout_custom'),
    path('cuidador/', views.cuidador, name='cuidador'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/<int:id>',views.editar_perfil, name='editar_perfil'),
    path('servicio/',views.servicio,name="servicio"),
    path('perfil_servicio/<int:id_servicio>/', views.perfil_servicio, name='perfil_servicio'),
    path('eliminar_servicio/<int:id>',views.eliminar_servicio,name="eliminar_servicio"),
    path('mod_servicio/<int:id_servicio>',views.modificar_servicio,name="modificar_servicio"),
    path('eliminar_mascota/<int:id>',views.eliminar_mascota,name="eliminar_mascota"),
    path('mod_mascota/<int:id_mascota>',views.modificar_mascota,name="modificar_mascota"),
    path('detalle_prestacion/<int:id_servicio>/', views.detalle_prestacion, name='detalle_prestacion'),
    path('prestacion/',views.prestacion,name="prestacion"),
    path('prestacion_cuidador/',views.prestacion_cuidador,name="prestacion_cuidador"),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<username>/', views.conversation, name='conversation'),
    path('send_message/<username>/', views.send_message, name='send_message'),
    path('eliminar_resena/<int:id>',views.eliminar_resena,name="eliminar_resena"),
    path('editar_cuidador/<int:id_cuidador>',views.editar_cuidador,name="editar_cuidador"),
]