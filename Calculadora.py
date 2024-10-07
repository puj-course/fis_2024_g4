from pymongo import MongoClient
from moves import get_move
import random
from math import sqrt

# Conectar a la base de datos
client = MongoClient('mongodb+srv://aiurbinamox:123@proyecto.1lqlm.mongodb.net/')
db = client['Proyecto']  # Cambia 'tu_base_de_datos' por el nombre de tu base de datos
pokemon_collection = db['Pokemon']  # Cambia 'tu_coleccion_pokemon' por el nombre de tu colección

# Constantes
print("Bienvenido al Simulador")
efectividades = "tabla_efectividad.csv"
lvl = 50
EV = 250
IV = 31

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
        # Asegúrate de que los movimientos se dividan correctamente
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
def vida(m):
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

# Salida
# Escoger el Pokémon que realizará el ataque
y = input("Ingrese el nombre del primer Pokémon: ")
y = y.lower()
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
                print("Nombre del Pokémon seleccionado: ", mayus(z))
                print("El HP al nivel ", lvl, "de", mayus(z), "es", stat(z)[0])
                print("El daño infligido por ", mayus(y), "es: ", dano(move, y, z))
                print("La vida restante de ", mayus(z), "es: ", vida(dano(move, y, z)))
