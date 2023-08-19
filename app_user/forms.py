from django import forms
from .helpers.jefes import get_empleados

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(label= 'Contraseña', widget=forms.TextInput(attrs={'type': 'password', 'autocomplete': 'off'}))


class Registro(LoginForm):
    re_password = forms.CharField(label= 'Confirmar Contraseña', widget=forms.TextInput(attrs={'type': 'password'}))
    email = forms.EmailField(label='Correo', max_length=255, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    
    
class RegistroAdminForm(Registro):
    salario = forms.FloatField(label='Salario')
    experiencia = forms.IntegerField(label='Años de Experiencia', min_value=0)
    jefe = forms.ChoiceField(label='Jefe', choices=get_empleados)