from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CrearUsuarioForm, IniciarSesionForm
from .models import Usuario  # Si es necesario, importa el modelo de Usuario desde donde lo tengas
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'..', '..', 'main'))

from calculadora import *
from moves import get_move
import random
from math import sqrt
from pokemon import Pokemon
from bd import *

def menu_principal(request):
    if request.method == "POST":
        opcion = request.POST.get('opcion')

        if opcion == "1":  # Crear usuario
            return redirect('crear_usuario')  # Redirige a la vista de crear usuario
        
        elif opcion == "2":  # Iniciar sesión
            return redirect('iniciar_sesion')  # Redirige a la vista de iniciar sesión
        
        elif opcion == "3":  # Simular batalla
            return redirect('simulador')  # Redirige a la vista de simulador

    return render(request, 'simulador/menu.html')

def crear_usuario(request):
    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            numero_telefono = form.cleaned_data['numero_telefono']
            
            # Crear un nuevo usuario
            usuario = Usuario(nombre, correo, contrasena, numero_telefono)
            usuario.crear_usuario()

            # Redirigir a otra página después de la creación del usuario
            return redirect('menu_principal')  # Redirige a la página principal después de crear el usuario

    else:
        form = CrearUsuarioForm()

    return render(request, 'simulador/crear_usuario.html', {'form': form})
    
def iniciar_sesion(request):
    if request.method == "POST":
        nombre_usuario = request.POST['nombre_usuario']  # Obtén el nombre de usuario del formulario
        contrasena = request.POST['contrasena']  # Obtén la contraseña del formulario
        
        # Llama al método estático correctamente
        nombre = Usuario.iniciar_sesion(nombre_usuario, contrasena)
        
        if nombre:
            # Si el nombre es devuelto, redirige al usuario a su página principal
            return redirect('menu_usuario', nombre_usuario=nombre)
        else:
            # Si no, muestra un error en el formulario
            return render(request, 'simulador/iniciar_sesion.html', {'error': 'Nombre de usuario o contraseña incorrectos.'})
    else:
        # Si no es una solicitud POST, simplemente renderiza el formulario de inicio de sesión
        return render(request, 'simulador/iniciar_sesion.html')

def menu_usuario(request, nombre_usuario):
    # Aquí puedes agregar más opciones para el usuario después de que inicie sesión
    return render(request, 'simulador/menu_usuario.html', {'nombre_usuario': nombre_usuario})
