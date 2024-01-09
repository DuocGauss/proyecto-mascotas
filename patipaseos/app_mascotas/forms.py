from django import forms
from .models import Propietario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
 



class frmRegistro(UserCreationForm):
    class Meta:
        model = Propietario
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        
        
class frmLogin(AuthenticationForm):
    class Meta:
        model = Propietario  # Reemplaza 'CustomUser' con el nombre de tu modelo de usuario personalizado
        fields = ['username', 'password']  