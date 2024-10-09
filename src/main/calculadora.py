from moves import get_move
import random
from math import sqrt
from pokemon import Pokemon
from bd import *
import os

efectividades = os.path.join(os.path.dirname(__file__), '..', '..', 'jupyter', 'datasets', 'tabla_efectividad.csv')
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




