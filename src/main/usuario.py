from twilio.rest import Client
from pymongo import MongoClient
from bd import *
# Configuración de Twilio
#ACCOUNT_SID = ''#vacio por que no me deja hacer commit si no
#AUTH_TOKEN = ''
#TWILIO_PHONE_NUMBER = ''
#twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

class Usuario:
    def __init__(self, nombre, correo, contrasena, numero_telefono):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.numero_telefono = numero_telefono
        self.twilio_client = twilio_client

    def crear_usuario(self):
        if usuarios_collection.find_one({"nombre": self.nombre}):
            print("El usuario ya existe.")
            return
        nuevo_usuario = {
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "numero_telefono": self.numero_telefono
        }
        usuarios_collection.insert_one(nuevo_usuario)
        print("Usuario creado exitosamente.")
        
        # Enviar mensaje de texto
        #self.enviar_mensaje()
#Necesito agregar el numero a los verified caller ID en twilio para que se pueda enviar el mensaje
    def enviar_mensaje(self):
        try:
            message = self.twilio_client.messages.create(
                body="¡Cuenta creada correctamente! Bienvenido.",
                from_=TWILIO_PHONE_NUMBER,  
                to=self.numero_telefono  
            )
            print(f"Mensaje enviado con éxito: {message.sid}")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")


    @staticmethod
    def modificar_usuario(nombre_usuario):
        nuevo_nombre = input("Ingresa el nuevo nombre (dejar en blanco para no modificar): ")
        nuevo_correo = input("Ingresa el nuevo correo (dejar en blanco para no modificar): ")
        nuevo_numero_telefono = input("Ingresa el nuevo número de teléfono (dejar en blanco para no modificar): ")
        nueva_contrasena = input("Ingresa la nueva contraseña (dejar en blanco para no modificar): ")

        cambios = {}
        if nuevo_nombre:
            cambios["nombre"] = nuevo_nombre
        if nuevo_correo:
            cambios["correo"] = nuevo_correo
        if nuevo_numero_telefono:
            cambios["numero_telefono"] = nuevo_numero_telefono
        if nueva_contrasena:
            cambios["contrasena"] = nueva_contrasena

        if cambios:
            usuarios_collection.update_one({"nombre": nombre_usuario}, {"$set": cambios})
            if "nombre" in cambios:  # Si el nombre fue cambiado
               return True 
            print("Usuario modificado exitosamente.")

    @staticmethod
    def eliminar_usuario(nombre_usuario):
        usuarios_collection.delete_one({"nombre": nombre_usuario})
        print("Usuario eliminado exitosamente.")

    @staticmethod
    def iniciar_sesion():
        nombre = input("Ingrese su nombre de usuario: ")
        contrasena = input("Ingrese su contraseña: ")
        usuario = usuarios_collection.find_one({"nombre": nombre, "contrasena": contrasena})
        if usuario:
            print("Inicio de sesión exitoso.")
            return nombre
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            return None