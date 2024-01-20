from django import forms
from .models import Propietario, Cuidador, Servicio, Mascota, DetPrestacion, Resena
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
 



class frmRegistro(UserCreationForm):
    class Meta:
        model = Propietario
        fields = ['rut','username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'direccion', 'telefono']
        
        
class frmLogin(AuthenticationForm):
    class Meta:
        model = Propietario  # Reemplaza 'CustomUser' con el nombre de tu modelo de usuario personalizado
        fields = ['username', 'password'] 
        
        
class frmCuidador(forms.ModelForm):
    class Meta:
        model = Cuidador
        exclude = ['disponibilidad']
        fields = ['especializacion', 'experiencia']
        
        
class frmEdit(UserChangeForm):
    class Meta:
        model=Propietario
        fields=["username","first_name","last_name","email","direccion","telefono","imagen"] 
        
        
class frmServicio(forms.ModelForm):
    class Meta:
        model=Servicio
        fields=["tipo_servicio","descripcion","precio"]
        
        
class frmMascota(forms.ModelForm):
    class Meta:
        model=Mascota
        fields=["nombre_mascota","tipo_mascota","tamaño_mascota","raza_mascota", "imagen"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))
        
        # Asegúrate de que los campos que deseas que sean opcionales tengan required=False
        self.fields['raza_mascota'].required = False
        self.fields['imagen'].required = False
        
        

class frmDetPrestacion(forms.ModelForm):
    class Meta:
        model = DetPrestacion
        fields = '__all__'
        exclude = ['id_servicio', 'id_propietario', 'id_cuidador']
        widgets = {
            'fecha_prestacion': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.HiddenInput(),  # Ocultar el campo estado
        }   
    valor_total = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, user, servicio_precio=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las mascotas del usuario actual
        self.fields['id_mascota'].queryset = Mascota.objects.filter(propietario=user)

        # Asignar el precio del servicio al valor_total
        if servicio_precio is not None:
            self.fields['valor_total'].initial = servicio_precio

    def clean(self):
        cleaned_data = super().clean()
        # Establecer el estado como "Activo" al guardar
        cleaned_data['estado'] = 'Pendiente'
        return cleaned_data

        
    

class frmResena(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['texto', 'calificacion']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3}),
            'calificacion': forms.HiddenInput(),  # Campo oculto para almacenar la calificación
        }