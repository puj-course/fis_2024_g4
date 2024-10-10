from pymongo import MongoClient
from moves import get_move
import random
from math import sqrt
from twilio.rest import Client
from usuario import *
from pokemon import *
from calculadora import*
from bd import *


print("Bienvenido al Simulador")

def menu_principal():
    while True:#menu principal
        print("\nMenu Principal:")
        print("1. Crear Usuario")
        print("2. Iniciar Sesión")
        print("3. Simular Batalla")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":#Inputs y llamado de la funcion de crear usario
            nombre = input("Ingrese su nombre: ")
            correo = input("Ingrese su correo: ")
            contrasena = input("Ingrese su contraseña: ")
            numero_telefono = input("Ingrese su número de teléfono: ")
            usuario = Usuario(nombre, correo, contrasena, numero_telefono)
            usuario.crear_usuario()
        elif opcion == "2":
            nombre_usuario = Usuario.iniciar_sesion()
            if nombre_usuario:#validacion de usuario
                while True:#submenu al estar logeado
                    print("\nMenu de Usuario:")
                    print("1. Modificar Usuario")
                    print("2. Eliminar Usuario")
                    print("3. Simular Batalla")
                    print("0. Salir al Menu Principal")

                    opcion_usuario = input("Seleccione una opción: ")
                    if opcion_usuario == "1":
                        mod=Usuario.modificar_usuario(nombre_usuario)
                        if mod:#comprobacion de si el nombre fue cambiado para volver al menu anterior
                            break
                    elif opcion_usuario == "2":
                        Usuario.eliminar_usuario(nombre_usuario)
                        break
                    elif opcion_usuario == "3":
                        simular()
                    elif opcion_usuario == "0":
                        break
                    else:
                        print("Opción inválida.")
        elif opcion == "3":
            simular()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

# Iniciar el programa
menu_principal()
