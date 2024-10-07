from pymongo import MongoClient
from moves import get_move
import random
from math import sqrt

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
continuar=1
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

# Obtener estadísticas de Pokémon de la base de datos
def stats(pokemon_name):
    pokemon = pokemon_collection.find_one({"Name": pokemon_name.lower()})  # Buscar por nombre
    if pokemon:
        return [
            pokemon['Name'],
            pokemon['Type'],
            pokemon['HP'],
            pokemon['ATK'],
            pokemon['DEF'],
            pokemon['SPA'],
            pokemon['SPD'],
            pokemon['SPE'],
            pokemon['MOVES'].split(";")  # Dividir los movimientos por ';'
        ]
    return None

# Calcular cuales serán los stats después de los modificadores
def stat(y):
    HP = (stats(y)[2])
    HP = int(((((int(HP) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + lvl + 10)
    ATK = (stats(y)[3])
    ATK = int(((((int(ATK) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5)
    DEF = (stats(y)[4])
    DEF = int(((((int(DEF) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5)
    SPA = (stats(y)[5])
    SPA = int(((((int(SPA) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5)
    SPD = (stats(y)[6])
    SPD = int(((((int(SPD) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5)
    SPE = (stats(y)[7])
    SPE = int(((((int(SPE) + IV) * 2 + (sqrt(EV) / 4)) * lvl) / 100) + 5)
    return HP, ATK, DEF, SPA, SPD, SPE

# Muestra los ataques del Pokémon elegido
def mostrar_movimientos(y):
    # Ahora se devuelve la lista de movimientos directamente
    return stats(y)[8]  # Devuelve la lista de movimientos

# Calcular cual es el modificador que tendrá del ataque realizado
def modifier(move, y, z):
    # Determinar si el rol será bueno o malo 
    n = random.randint(85, 100)
    n = float(n / 100)
    # Verificar si el tipo del ataque es igual al tipo del Pokémon
    if get_move(mostrar_movimientos(y)[move])[2] == stats(y)[1]:
        STAB = 1.2
    else:
        STAB = 1
    # Ver en qué posición de la tabla de efectividades está el tipo del Pokémon que recibe el ataque
    comprobar = tipo("Atk/Def").index(stats(z)[1])
    # Verificar si el ataque es efectivo o no en base a su posición en la tabla de efectividades
    efecto = tipo(get_move(mostrar_movimientos(y)[move])[2])[comprobar]
    modificar = float(efecto) * float(STAB) * float(n) * 1
    return modificar

# Calcular el daño que hará el ataque
def dano(move, y, z):
    # Verificar tipo de daño
    if get_move(mostrar_movimientos(y)[move])[3] in "special":
        damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[3] / stat(z)[4])) / 50) + 2) * modifier(move, y, z))
    else:
        damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[1] / stat(z)[2])) / 50) + 2) * modifier(move, y, z))
    return damage

# Calcular vida restante del Pokémon después de recibir un ataque
def vida(m, z):
    vida_restante = int(stat(z)[0] - m)
    return vida_restante

# Convertir la primera letra en mayúscula
def mayus(y):
    letra = y.split()
    mayuscula = ord(letra[0][0])
    letra = letra[0][1:]
    mayuscula = chr(mayuscula - 32)
    mayuscula += letra
    return mayuscula
def simular():
    y = input("Ingrese el nombre del primer Pokémon: ")
    y = y.lower()
    roll=0
    detener = False
    # Detener el programa en caso de que el nombre ingresado no sea un Pokémon existente
    if stats(y) is None:
        print("Pokémon inválido")
    else:
        # Mostrar estadísticas base del Pokémon
        print("Nombre del Pokémon seleccionado: ", mayus(y))
        print("Estadísticas base del Pokémon: ", "\n", " - HP = ", stats(y)[2], "\n", " - Ataque = ", stats(y)[3], "\n", " - Defensa = ", stats(y)[4], "\n",
              " - Ataque especial = ", stats(y)[5], "\n", " - Defensa Especial = ", stats(y)[6], "\n", " - Velocidad = ", stats(y)[7])
        print("Movimientos que puede aprender el Pokémon:")
        # Mostrar movimientos
        i = 0
        while i < len(mostrar_movimientos(y)):
            print(i, " - ", mostrar_movimientos(y)[i])
            i += 1
        # Selección de movimiento y mostrar estadísticas después de modificadores
        move = int(input("Seleccione movimiento a ejecutar: "))
        # Detener el programa en caso de que se elija un movimiento que no está disponible
        if move >= len(mostrar_movimientos(y)):
            detener = True
        if detener is True:
            print("Movimiento inválido")
        else:
            # Verificar que el ataque elegido haga daño
            while get_move(mostrar_movimientos(y)[move])[1] == 0:
                move = int(input("No se puede calcular el daño ingrese otro movimiento: "))
                if move >= len(mostrar_movimientos(y)):
                    detener = True
            if detener is True:
                print("Movimiento inválido")
            else:
                # Mostrar el movimiento y las estadísticas después de los modificadores
                print("El ataque seleccionado es: ", mostrar_movimientos(y)[move])
                print("El poder del ataque es: ", get_move(mostrar_movimientos(y)[move])[1])
                print("El HP al nivel ", lvl, "de", mayus(y), "es", stat(y)[0])
                print("El ATK al nivel ", lvl, "de", mayus(y), "es", stat(y)[1])
                print("El DEF al nivel ", lvl, "de", mayus(y), "es", stat(y)[2])
                print("El SPA al nivel ", lvl, "de", mayus(y), "es", stat(y)[3])
                print("El SPD al nivel ", lvl, "de", mayus(y), "es", stat(y)[4])
                print("El SPE al nivel ", lvl, "de", mayus(y), "es", stat(y)[5])
                # Escoger el Pokémon que recibirá el ataque y mostrar su vida después de modificadores
                z = input("Ingrese el nombre del Pokémon a atacar: ")
                z = z.lower()
                if stats(z) is None:
                    print("Pokémon inválido")
                else:
                    roll=dano(move, y, z)
                    print("Nombre del Pokémon seleccionado: ", mayus(z))
                    print("El HP al nivel ", lvl, "de", mayus(z), "es", stat(z)[0])
                    print("El daño infligido por ", mayus(y), "es: ", roll)
                    print("La vida restante de ", mayus(z), "es: ", vida(roll,z))
# Variable global para almacenar el estado del usuario autenticado
nombre_usuario = None

def iniciar_sesion():
    global nombre_usuario
    nombre = input("Ingresa tu nombre de usuario: ")
    contrasena = input("Ingresa tu contraseña: ")
    
    # Buscar el usuario en la colección
    usuario = usuarios_collection.find_one({"nombre": nombre, "contrasena": contrasena})
    
    if usuario:
        nombre_usuario = usuario["nombre"]
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False
    
def crear_usuario():
    nombre = input("Ingresa tu nombre: ")
    correo = input("Ingresa tu correo: ")
    contrasena = input("Ingresa tu contraseña: ")
    numero_telefono = input("Ingresa tu número de teléfono: ")

    # Verificar si el usuario ya existe
    if usuarios_collection.find_one({"nombre": nombre}):
        print("El usuario ya existe.")
        return

    # Crear el nuevo usuario
    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "contrasena": contrasena,
        "numero_telefono": numero_telefono
    }

    usuarios_collection.insert_one(nuevo_usuario)
    print("Usuario creado exitosamente.")

def modificar_usuario(nombre_usuario):
    nuevo_nombre = input("Ingresa el nuevo nombre (dejar en blanco para no modificar): ")
    nuevo_correo = input("Ingresa el nuevo correo (dejar en blanco para no modificar): ")
    nuevo_numero_telefono = input("Ingresa el nuevo número de teléfono (dejar en blanco para no modificar): ")
    nueva_contrasena = input("Ingresa la nueva contraseña (dejar en blanco para no modificar): ")

    # Crear un diccionario con los cambios
    cambios = {}
    if nuevo_nombre:
        cambios["nombre"] = nuevo_nombre
    if nuevo_correo:
        cambios["correo"] = nuevo_correo
    if nuevo_numero_telefono:
        cambios["numero_telefono"] = nuevo_numero_telefono
    if nueva_contrasena:
        cambios["contrasena"] = nueva_contrasena

    # Actualizar el usuario
    if cambios:
        resultado = usuarios_collection.update_one({"nombre": nombre_usuario}, {"$set": cambios})
        if resultado.modified_count > 0:
            print("Usuario modificado exitosamente.")
            if "nombre" in cambios:  # Si el nombre fue cambiado
               return True 
        else:
            print("No se encontraron cambios para modificar.")
    else:
        print("No se realizaron modificaciones.")



def eliminar_usuario(nombre_usuario):
    # Eliminar el usuario
    resultado = usuarios_collection.delete_one({"nombre": nombre_usuario})
    
    if resultado.deleted_count > 0:
        print("Usuario eliminado exitosamente.")
    else:
        print("No se encontró un usuario con ese nombre.")



# Salida
# Escoger el Pokémon que realizará el ataque
while continuar != 0:
    opcion=int(input("1.-Iniciar Sesion\n2.-Crear Usuario\n3.-Calcular Daño\n0.-Salir\n"))
    if opcion==1:
        sesion_iniciada=iniciar_sesion()
        if sesion_iniciada:
            while continuar!=0:
                subopcion=int(input("1.-Modificar Usuario\n2.-Eliminar Usuario\n3.-Calcular Daño\n0.-Salir\n"))
                if subopcion==1:
                    mod=modificar_usuario(nombre_usuario)
                    if mod:
                        break
                elif subopcion==2:
                    eliminar_usuario(nombre_usuario)
                    break
                elif subopcion==3:
                    simular()
                else:
                    continuar=0
    elif opcion==2:
        crear_usuario()
    elif opcion==3:
        simular()
    else:
        continuar=0
