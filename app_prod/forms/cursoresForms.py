from django import forms

class AumentarDisminuirCantidadForm(forms.Form):
    cantidad = forms.IntegerField()