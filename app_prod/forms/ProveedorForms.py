from django import forms


class ProveedorForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50)
    telefono = forms.CharField(max_length=255, label='Telefono')