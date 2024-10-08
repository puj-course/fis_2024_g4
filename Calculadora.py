from pymongo import MongoClient
from moves import get_move
import random
from math import sqrt
from twilio.rest import Client

# Configuración de Twilio
ACCOUNT_SID = ''#vacio por que no me deja hacer commit si no
AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Conectar a la base de datos
client = MongoClient('mongodb+srv://aiurbinamox:123@proyecto.1lqlm.mongodb.net/')
db = client['Proyecto']  
pokemon_collection = db['Pokemon'] 
usuarios_collection = db['Usuarios']
# Constantes
print("Bienvenido al Simulador")
efectividades = "tabla_efectividad.csv"
lvl = 50
EV = 250
IV = 31
continuar = 1

# Clase Pokemon
class Pokemon:
    def __init__(self, name):
        self.name = name.lower()
        self.data = self.obtener_stats()

    def obtener_stats(self):
        pokemon = pokemon_collection.find_one({"Name": self.name})  # Buscar por nombre
        if pokemon:
            return {
                'Name': pokemon['Name'],
                'Type': pokemon['Type'],
                'HP': pokemon['HP'],
                'ATK': pokemon['ATK'],
                'DEF': pokemon['DEF'],
                'SPA': pokemon['SPA'],
                'SPD': pokemon['SPD'],
                'SPE': pokemon['SPE'],
                'MOVES': pokemon['MOVES'].split(";")  # Dividir los movimientos por ';'
            }
        return None

    def stats(self):
        return self.data

# Abre archivo de efectividades
def abrir_archivo(archivo):
    with open(archivo) as f:
        contenido = f.readlines()
    return contenido

# Abre la tabla de efectividades y encuentra el tipo del ataque 
def tipo(x):
    contenido = abrir_archivo(efectividades)
    for line in contenido:
        line = line.split(",")
        if x in line:
            num = line
    return num

# Calcular cuales serán los stats después de los modificadores
def stat(pokemon):
    HP = (pokemon.stats()['HP'])
    HP = int((((((int(HP) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + lvl + 10))
    ATK = (pokemon.stats()['ATK'])
    ATK = int((((((int(ATK) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5))
    DEF = (pokemon.stats()['DEF'])
    DEF = int((((((int(DEF) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5))
    SPA = (pokemon.stats()['SPA'])
    SPA = int((((((int(SPA) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5))
    SPD = (pokemon.stats()['SPD'])
    SPD = int((((((int(SPD) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5))
    SPE = (pokemon.stats()['SPE'])
    SPE = int((((((int(SPE) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5))
    return HP, ATK, DEF, SPA, SPD, SPE

# Muestra los ataques del Pokémon elegido
def mostrar_movimientos(pokemon):
    return pokemon.stats()['MOVES']  # Devuelve la lista de movimientos

# Calcular cual es el modificador que tendrá del ataque realizado
def modifier(move, y, z):
    n = random.randint(85, 100)
    n = float(n / 100)
    if get_move(mostrar_movimientos(y)[move])[2] == y.stats()['Type']:
        STAB = 1.2
    else:
        STAB = 1
    comprobar = tipo("Atk/Def").index(z.stats()['Type'])
    efecto = tipo(get_move(mostrar_movimientos(y)[move])[2])[comprobar]
    modificar = float(efecto) * float(STAB) * float(n) * 1
    return modificar

# Calcular el daño que hará el ataque
def dano(move, y, z):
    if get_move(mostrar_movimientos(y)[move])[3] in "special":
        damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[1] / stat(z)[4])) / 50) + 2) * modifier(move, y, z))
    else:
        damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[1] / stat(z)[2])) / 50) + 2) * modifier(move, y, z))
    return damage

# Calcular vida restante del Pokémon después de recibir un ataque
def vida(m, z):
    vida_restante = int(stat(z)[0] - m)
    return vida_restante

def simular():
    y = input("Ingrese el nombre del primer Pokémon: ")
    y = y.lower()
    roll = 0
    detener = False
    pokemon_y = Pokemon(y)  # Crear objeto Pokémon
    if pokemon_y.stats() is None:
        print("Pokémon inválido")
    else:
        print("Nombre del Pokémon seleccionado: ", y.capitalize())  # Cambiado para usar capitalize()
        print("Estadísticas base del Pokémon: ", "\n", " - HP = ", pokemon_y.stats()['HP'], "\n", " - Ataque = ", pokemon_y.stats()['ATK'], "\n", " - Defensa = ", pokemon_y.stats()['DEF'], "\n",
              " - Ataque especial = ", pokemon_y.stats()['SPA'], "\n", " - Defensa Especial = ", pokemon_y.stats()['SPD'], "\n", " - Velocidad = ", pokemon_y.stats()['SPE'])
        print("Movimientos que puede aprender el Pokémon:")
        i = 0
        while i < len(mostrar_movimientos(pokemon_y)):
            print(i, " - ", mostrar_movimientos(pokemon_y)[i])
            i += 1
        move = int(input("Seleccione movimiento a ejecutar: "))
        if move >= len(mostrar_movimientos(pokemon_y)):
            detener = True
        if detener is True:
            print("Movimiento inválido")
        else:
            while get_move(mostrar_movimientos(pokemon_y)[move])[1] == 0:
                move = int(input("No se puede calcular el daño ingrese otro movimiento: "))
                if move >= len(mostrar_movimientos(pokemon_y)):
                    detener = True
            if detener is True:
                print("Movimiento inválido")
            else:
                print("El ataque seleccionado es: ", mostrar_movimientos(pokemon_y)[move])
                print("El poder del ataque es: ", get_move(mostrar_movimientos(pokemon_y)[move])[1])
                print("El HP al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[0])
                print("El ATK al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[1])
                print("El DEF al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[2])
                print("El SPA al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[3])
                print("El SPD al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[4])
                print("El SPE al nivel ", lvl, "de", y.capitalize(), "es", stat(pokemon_y)[5])
                z = input("Ingrese el nombre del Pokémon a atacar: ")
                z = z.lower()
                pokemon_z = Pokemon(z)  # Crear objeto Pokémon
                if pokemon_z.stats() is None:
                    print("Pokémon inválido")
                else:
                    roll = dano(move, pokemon_y, pokemon_z)
                    print("Nombre del Pokémon seleccionado: ", z.capitalize())  # Cambiado para usar capitalize()
                    print("El HP al nivel ", lvl, "de", z.capitalize(), "es", stat(pokemon_z)[0])
                    print("El daño infligido por ", y.capitalize(), "es: ", roll)
                    print("La vida restante de ", z.capitalize(), "es: ", vida(roll, pokemon_z))

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

def menu_principal():
    while True:
        print("\nMenu Principal:")
        print("1. Crear Usuario")
        print("2. Iniciar Sesión")
        print("3. Simular Batalla")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nombre = input("Ingrese su nombre: ")
            correo = input("Ingrese su correo: ")
            contrasena = input("Ingrese su contraseña: ")
            numero_telefono = input("Ingrese su número de teléfono: ")
            usuario = Usuario(nombre, correo, contrasena, numero_telefono)
            usuario.crear_usuario()
        elif opcion == "2":
            nombre_usuario = Usuario.iniciar_sesion()
            if nombre_usuario:
                while True:
                    print("\nMenu de Usuario:")
                    print("1. Modificar Usuario")
                    print("2. Eliminar Usuario")
                    print("3. Simular Batalla")
                    print("0. Salir al Menu Principal")

                    opcion_usuario = input("Seleccione una opción: ")
                    if opcion_usuario == "1":
                        mod=Usuario.modificar_usuario(nombre_usuario)
                        if mod:
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
