from django import forms


class EstudianteForm(forms.Form):
    nombre_completo = forms.CharField(label='Nombre completo', required=False)
    documento_identidad = forms.IntegerField(label='Documento de identidad', required=False)
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)
    programa_academico = forms.CharField(label='Programa académico', required=False)
