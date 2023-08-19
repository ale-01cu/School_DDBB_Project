from django import forms
from app_prod.helpers.ver_proveedores import get_proveedores


class ProductosForms(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    cant_stock = forms.IntegerField()
    precio = forms.FloatField()
    imagen = forms.CharField(label='Url Imagen', max_length=200)
    id_proveedor = forms.ChoiceField(label='Proveedor', choices=get_proveedores)
    categoria = forms.ChoiceField(label='Seleccione el tipo de producto', choices=[('movil', 'Movil'), ('componente_pc', 'Componente de pc'), ('equipo_hogar', 'Equipo del hogar')])


    tamanio_pantalla = forms.CharField(max_length=10, label="Tamaño de la pantalla", required=False)
    espacio = forms.CharField(max_length=10, label="Espacio", required=False)
    memoria_ram = forms.CharField(max_length=10, label="Memoria RAM", required=False)
    
    consumo = forms.CharField(max_length=10, label="Consumo de energia", required=False)