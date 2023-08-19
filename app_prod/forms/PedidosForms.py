from django import forms

class PedidoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1)
    info_contacto = forms.CharField(max_length=255, label='Informacion de Contacto')
    dir_envio = forms.CharField(max_length=255, label='Direccion de envio')