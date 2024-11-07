from django import forms

class CrearUsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    contrasena = forms.CharField(widget=forms.PasswordInput())
    numero_telefono = forms.CharField(max_length=15)

class IniciarSesionForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget=forms.PasswordInput())
