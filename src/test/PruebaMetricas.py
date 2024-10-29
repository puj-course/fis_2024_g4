import os
import ast
from radon.complexity import cc_visit
from radon.raw import analyze

directorio = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'main')

# Función para calcular la complejidad ciclomatica
def calcular_complejidad_ciclomatica(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    resultados = cc_visit(contenido)
    return [(resultado.name, resultado.complexity) for resultado in resultados]

# Función para analizar longitud de código
def analizar_longitud_codigo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    analisis = analyze(contenido)
    return (analisis.loc, analisis.lloc, analisis.comments)

# Función para calcular la profundidad de anidado
def calcular_profundidad_anidado(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    profundidad_maxima = 0
    profundidad_actual = 0

    for linea in lineas:
        # Ignorar líneas vacías
        if not linea.strip():
            continue

        # Contar el nivel de indentación
        nivel_indentacion = len(linea) - len(linea.lstrip(' \t'))

        # Comprobar si la línea es un bloque de código
        if linea.strip().startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:', 'else:', 'elif ', 'except ')):
            # Actualizar la profundidad actual
            profundidad_actual = (nivel_indentacion // 4) + 1  # Suponiendo 4 espacios por nivel de indentación
            profundidad_maxima = max(profundidad_maxima, profundidad_actual)
        else:
            # Resetear si encontramos un bloque que no crea nueva profundidad
            if nivel_indentacion < profundidad_actual * 4:
                profundidad_actual = (nivel_indentacion // 4) + 1

    return profundidad_maxima
# Función para calcular fan-in y fan-out
def calcular_fan_in_out(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    tree = ast.parse(contenido)
    
    fan_out = {}
    fan_in = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            fan_out[node.name] = 0  # Inicializa el fan-out
            fan_in[node.name] = 0    # Inicializa el fan-in
            # Contar fan-out
            for n in ast.walk(node):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                    fan_out[node.name] += 1

    # Contar fan-in
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in fan_in:
                fan_in[node.func.id] += 1

    return fan_in, fan_out

# Función para calcular la longitud de identificadores

def longitud_identificadores(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        tree = ast.parse(contenido)
        longitudes = []
        identificadores_vistos = set()  # Usar un conjunto para evitar duplicados

        # Recorre el árbol de sintaxis
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name not in identificadores_vistos:
                    longitudes.append((node.name, len(node.name)))
                    identificadores_vistos.add(node.name)  # Agregar a los vistos
            elif isinstance(node, ast.Name):
                if node.id not in identificadores_vistos:
                    longitudes.append((node.id, len(node.id)))
                    identificadores_vistos.add(node.id)  # Agregar a los vistos
            elif isinstance(node, ast.arg):
                if node.arg not in identificadores_vistos:
                    longitudes.append((node.arg, len(node.arg)))
                    identificadores_vistos.add(node.arg)  # Agregar a los vistos

    return longitudes  # Retorna la lista de tuplas (nombre, longitud)


# Función para procesar todos los archivos en un directorio
def procesar_directorio(directorio):
    # Inicializa contadores para las métricas totales
    total_lineas_codigo = 0
    total_lineas_ejecutables = 0
    total_lineas_comentarios = 0
    anidado_mayor = 0
    total_fan_in = 0
    total_fan_out = 0
    total_identificadores = 0

    for nombre_archivo in os.listdir(directorio):
        if nombre_archivo.endswith('.py'):
            ruta_archivo = os.path.join(directorio, nombre_archivo)
            # Calcular métricas
            complejidad_resultados = calcular_complejidad_ciclomatica(ruta_archivo)
            longitud_resultados = analizar_longitud_codigo(ruta_archivo)
            profundidad_resultados = calcular_profundidad_anidado(ruta_archivo)
            fan_in, fan_out = calcular_fan_in_out(ruta_archivo)
            longitudes_identificadores = longitud_identificadores(ruta_archivo)

            # Imprimir resultados
            print(f"\n--- Análisis de {ruta_archivo} ---")
            for nombre, complejidad in complejidad_resultados:
                print(f"Nombre: {nombre}, Complejidad: {complejidad}")
            print(f"Líneas totales de código: {longitud_resultados[0]}")
            print(f"Líneas de código ejecutables: {longitud_resultados[1]}")
            print(f"Líneas de comentarios: {longitud_resultados[2]}")
            print(f"Profundidad de anidado: {profundidad_resultados}")
            print(f"Fan-in: {fan_in}")
            print(f"Fan-out: {fan_out}")

            # Imprimir longitudes de identificadores y contar
            print(f"Longitudes de identificadores:")
            for nombre, longitud in longitudes_identificadores:
                print(f"  {nombre}: {longitud}")
                total_identificadores += 1  # Contar identificadores

            # Acumula totales
            total_lineas_codigo += longitud_resultados[0]
            total_lineas_ejecutables += longitud_resultados[1]
            total_lineas_comentarios += longitud_resultados[2]
            if(profundidad_resultados>anidado_mayor):
                anidado_mayor=profundidad_resultados

            # Sumar valores de fan_in si es un diccionario
            if isinstance(fan_in, dict):
                total_fan_in += sum(fan_in.values())  # Sumar todos los valores del diccionario
            else:
                total_fan_in += fan_in  # Si es un entero

            # Sumar valores de fan_out si es un diccionario
            if isinstance(fan_out, dict):
                total_fan_out += sum(fan_out.values())  # Sumar todos los valores del diccionario
            else:
                total_fan_out += fan_out  # Si es un entero

    # Imprimir resultados totales
    print("\n--- Resultados Totales ---")
    print(f"Líneas totales de código: {total_lineas_codigo}")
    print(f"Líneas de código ejecutables: {total_lineas_ejecutables}")
    print(f"Líneas de comentarios: {total_lineas_comentarios}")
    print(f"Profundidad de Mayor profundidad de anidado : {anidado_mayor}")
    print(f"Fan-in total: {total_fan_in}")
    print(f"Fan-out total: {total_fan_out}")
    print(f"Total de identificadores: {total_identificadores}")
    
# Llama a la función para procesar el directorio
procesar_directorio(directorio)
