from django import forms

class ExcelSearchForm(forms.Form):
    archivo = forms.FileField(label="Archivo Excel (.xlsx)")
    texto = forms.CharField(label="Texto a buscar", max_length=100)
