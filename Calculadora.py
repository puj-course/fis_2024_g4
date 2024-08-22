from math import sqrt
from moves import get_move
import random

#Constantes
print("Bienvenido al Simulador")
efectividades="tabla_efectividad.csv"
estadisticas="pokemon_data.csv"
lvl=50
EV=250
IV=31
continuar=1

#abre archivo
def abrir_archivo(archivo):
	with open(archivo) as f:
		contenido=f.readlines()
	return contenido
#Abre la tabla de efectividades y encuentra el tipo del ataque 
def tipo(x):
	contenido=abrir_archivo(efectividades)
	for line in contenido:
		line=line.split(",")
		if x in line:
			num=line
	return num

#Abre el archivo y muestra la informacion basica del pokemon elegido
def stats(y):
	contenido=abrir_archivo(estadisticas)
	estadistica=[]
	linec="0"
	for line in contenido:
		line=line.split(",")
		if y in line:
			estadistica=line[0:]
	return estadistica
#Calcular cuales seran los stats despues de los modificadores
def stat(y):
	HP=(stats(y)[2])
	HP=int((((int(HP)+IV)*2+(sqrt(EV)/4))*lvl)/100)+lvl+10	
	ATK=(stats(y)[3])
	ATK=int((((int(ATK)+IV)*2+(sqrt(EV)/4))*lvl)/100)+5
	DEF=(stats(y)[4])
	DEF=int((((int(DEF)+IV)*2+(sqrt(EV)/4))*lvl)/100)+5
	SPA=(stats(y)[5])
	SPA=int((((int(SPA)+IV)*2+(sqrt(EV)/4))*lvl)/100)+5
	SPD=(stats(y)[6])
	SPD=int((((int(SPD)+IV)*2+(sqrt(EV)/4))*lvl)/100)+5
	SPE=(stats(y)[7])
	SPE=int((((int(SPE)+IV)*2+(sqrt(EV)/4))*lvl)/100)+5
	return HP, ATK, DEF, SPA, SPD, SPE
#Muestra los ataques del pokemon elegido
def mostrar_movimnientos(y):
	contenido=stats(y)[8]
	movimientos=[]
	line=contenido.split(";")
	movimientos=line[0:]
	return movimientos
#Calcular cual es el modificador que tendra de el ataque realizado
def modifier(move, y, z):
	#Determinar si el rol sera bueno o malo 
	n=random.randint(85, 100)
	n=float(n/100)
	#Verificar si el tipo del ataque es igual al tipo del pokemon
	if get_move(mostrar_movimnientos(y)[move])[2]==stats(y)[1]:
		STAB=1.2
	else:
		STAB=1
	#Ver en que posicion de la tabla de efectividaes esta el tipo del pokemon que recibe el ataque
	comprobar=tipo("Atk/Def").index(stats(z)[1])
	#Verificar si el ataque es efectivo o no en base a su posicion en la tabla de efectividades
	efecto=tipo(get_move(mostrar_movimnientos(y)[move])[2])[comprobar]
	modificar=float(efecto)*float(STAB)*float(n)*1
	return modificar

#Calcular el daño que hara el ataque
def dano(move, y, z):
	#Verificar tipo de daño
	if get_move(mostrar_movimnientos(y)[move])[3] in "special":
		damage=int((((((2*lvl)/5)+2)*get_move(mostrar_movimnientos(y)[move])[1]*(stat(y)[3]/stat(z)[4]))/50)+2)*modifier(move, y, z)
	else:
		damage=int((((((2*lvl)/5)+2)*get_move(mostrar_movimnientos(y)[move])[1]*(stat(y)[1]/stat(z)[2]))/50)+2)*modifier(move, y, z)
	return damage
#Calcular vida restante del pokemon despues de recibir un ataque
def vida(m):
	vida_restante=int(stat(z)[0]-m)
	if vida_restante < 0:
		vida_restante=0
	return vida_restante

#Convertir la primera letra en mayuscula
def mayus(y):
	letra=y.split()
	mayuscula=ord(letra[0][0])
	letra=letra[0][1:]
	mayuscula=chr(mayuscula-32)
	mayuscula+=letra
	return mayuscula

#Salida
while continuar == 1:
#Escoger el pokemon que realizara el ataque
	y=input("Ingrese el nombre del primer Pokemon: ")
	y=y.lower()
	detener=False
#Detener el programa en caso de que el nombre ingresado no sea un pokemon existente
	if y not in stats(y):
		print("Pokemon invalido")
	else:
		#Mostrar estadisticas base del pokemon
		print("Nombre del Pokemon seleccionado: ", mayus(y))
		print("Estadisticas base del Pokemon: ", "\n", " - HP = ", stats(y)[2], "\n", " - Ataque = ", stats(y)[3], "\n", " - Defensa = ", stats(y)[4], "\n",
		 " - Ataque especial = ", stats(y)[5], "\n", " - Defensa Especial = ", stats(y)[6], "\n", " - Velocidad = ", stats(y)[7])
		print("Movimientos que puede aprender el Pokemon:")
		#Mostrar movimientos
		i=0
		while i<len(mostrar_movimnientos(y)):
			print(i, " - ", mostrar_movimnientos(y)[i])
			i+=1
		#Seleccion de movimiento y mostrar estadisticas despues de modificadores
		move=int(input("Seleccione movimiento a ejecutar: "))
		#Detener el programa  en caso de que se eliga un movimiento que no esta disponible
		if move >= len(mostrar_movimnientos(y)):
			detener=True
		if detener is True:
			print("Movimietno invalido")
		else:
			#Verificar que el ataque elegido haga daño
			while get_move(mostrar_movimnientos(y)[move])[1]==0:
				move=int(input("No se puede calcular el daño ingrese otro movimiento: "))
				if move >= len(mostrar_movimnientos(y)):
					detener=True
			if detener is True:
				print("Movimietno invalido")
			else:
				#Mostrar el movimiento y las estadisticas despues de los modificadores
				print("El ataque seleccionado es: ", mostrar_movimnientos(y)[move])
				print("El poder del ataque es: ", get_move(mostrar_movimnientos(y)[move])[1])
				print("El hp al nivel ", lvl, "de", mayus(y), "es", stat(y)[0])
				print("El atk al nivel ", lvl, "de", mayus(y), "es", stat(y)[1])
				print("El def al nivel ", lvl, "de", mayus(y), "es", stat(y)[2])
				print("El spa al nivel ", lvl, "de", mayus(y), "es", stat(y)[3])
				print("El spd al nivel ", lvl, "de", mayus(y), "es", stat(y)[4])
				print("El spe al nivel ", lvl, "de", mayus(y), "es", stat(y)[5])
				#Escoger el pokemon que recibira el ataque y mostrar su vida despues de modificadores
				z=input("Ingrese el nombre a atacar pokemon: ")
				z=z.lower()
				if z not in stats(z):
					print("Pokemon invalido")
				else:
					print("Nombre del pokemon seleccionado: ", mayus(z))
					print("El hp al nivel ", lvl, "de", mayus(z), "es", stat(z)[0])
					#Calcula el daño y la vida restante del pokemon que recibe el ataque
					m=dano(move, y, z)
					print("El daño que realizo ", mayus(y), "a", mayus(z), "fue de: ", m)
					print(mayus(z), "quedo con un HP de: ", vida(m))
	continuar=int(input("Desea continuar?:\n 1.-Si\n 2.-No\n"))
if continuar !=1:
	print("Gracias por usar el programa!")
