import random
from datetime import datetime


# Variables globales
bingo_info = {"fecha": "", "hora": "", "costo": float(0)}
compras = []
compras_copia = []
numeros_de_serie = set()

numeros_sorteados = []
juego_iniciado = False

# Función para mostrar el menú principal
def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Configurar información del Bingo")
    print("2. Comprar Bingos")
    print("3. Visualizar compras")
    print("4. Jugar al Bingo")
    print("0. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


# Función para configurar la información del Bingo
def configurar_informacion():
    global bingo_info
    print("\n--- CONFIGURAR INFORMACIÓN DEL BINGO ---")

    # Validar la fecha
    while True:
        fecha = input("Ingrese la fecha (dd/mm/yyyy): ")
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            bingo_info["fecha"] = fecha
            break
        except ValueError:
            print("Fecha no válida. Asegúrese de usar el formato dd/mm/yyyy.")

    # Validar la hora
    while True:
        hora = input("Ingrese la hora (HH:MM): ")
        try:
            datetime.strptime(hora, "%H:%M")
            bingo_info["hora"] = hora
            break
        except ValueError:
            print("Hora no válida. Asegúrese de usar el formato HH:MM.")

    # Validar el costo
    while True:
        try:
            costo = float(input("Ingrese el costo del Bingo: S/ "))
            if costo > 0:
                bingo_info["costo"] = costo
                break
            else:
                print("El costo debe ser un número positivo.")
        except ValueError:
            print("Costo no válido. Ingrese un número válido.")

    print(
        f"\nInformación configurada:\nFecha: {bingo_info['fecha']} - Hora: {bingo_info['hora']} - Costo: S/ {bingo_info['costo']}"
    )


# Función para comprar Bingos
def comprar_bingos():
    global compras, bingo_info
    print("\n--- COMPRAR BINGOS ---")

    # Validación del nombre (solo letras)
    while True:
        nombre = input("Nombre: ")
        if nombre.isalpha():  # Verifica que el nombre contenga solo letras
            break  # Sale del bucle si el nombre es válido
        else:
            print("El nombre debe contener solo letras. Intente de nuevo.")

    # Validación del DNI (solo números y exactamente 8 dígitos)
    while True:
        dni = input("DNI: ")
        if dni.isdigit() and len(dni) == 8:  # Verifica que el DNI contenga solo números y tenga 8 dígitos
            break  # Sale del bucle si el DNI es válido
        else:
            print("El DNI debe contener solo numeros y 8 dígitos. Intente de nuevo.")

    # Validación del correo electrónico (debe contener al menos un @ y un punto)
    while True:
        email = input("Email: ")
        if "@" in email and "." in email:  # Verifica que el correo contenga al menos un @ y un punto
            break  # Sale del bucle si el correo es válido
        else:
            print("El correo electrónico debe contener al menos un '@' y un punto. Intente de nuevo.")

    # Validación de la cantidad de Bingos (solo números enteros positivos)
    while True:
        cantidad_bingos = input("Cantidad de Bingos: ")
        if cantidad_bingos.isdigit():  # Verifica si la entrada son solo dígitos
            cantidad_bingos = int(cantidad_bingos)  # Convierte la cadena a un número entero
            if cantidad_bingos > 0:  # Verifica que el número sea positivo
                break  # Sale del bucle si la cantidad es válida
            else:
                print("La cantidad debe ser un número entero positivo. Intente de nuevo.")
        else:
            print("La cantidad debe ser un número entero, no letras ni otros caracteres. Intente de nuevo.")

    total_costo = cantidad_bingos * bingo_info['costo']
    print(f"Costo total: S/ {total_costo}")

    # Confirmar compra
    while True:
        confirmar = input("(A)ceptar o (C)ancelar: ").upper()
        if confirmar in ['A', 'C']:
            break
        else:
            print("Opción no válida. Por favor, seleccione (A)ceptar o (C)ancelar.")
    if confirmar == 'A':
        bingos_generados = generar_bingos(cantidad_bingos)
        fecha_compra = datetime.now().strftime("%d/%m/%Y %H:%M")
        compras.append({
            "nombre": nombre,
            "dni": dni,
            "email": email,
            "cantidad": cantidad_bingos,
            "costo_total": total_costo,
            "fecha": fecha_compra,
            "bingos": bingos_generados
        })
        print("Compra realizada correctamente!")
        print(f"Fecha de compra: {fecha_compra}")
        for bingo in bingos_generados:
            print(f"Número de serie: {bingo['serie']}")
            imprimir_bingo(bingo["numeros"])
    else:
        print("Compra cancelada.")


# Función para generar Bingos
def generar_bingos(cantidad):
    bingos = []
    global numeros_de_serie
    for _ in range(cantidad):
        while True:
            serie = random.randint(1000, 9999)
            if serie not in numeros_de_serie:
                numeros_de_serie.add(serie)
                break
        bingo = {
            "serie": f"{serie}",
            "numeros": generar_numeros_bingo()
        }
        bingos.append(bingo)
    return bingos


# Función para generar los números de una cartilla de Bingo
def generar_numeros_bingo():
    bingo = []
    for i in range(5):
        if i == 0:
            columna = random.sample(range(1, 16), 5)
        elif i == 1:
            columna = random.sample(range(16, 31), 5)
        elif i == 2:
            columna = random.sample(range(31, 46), 5)
        elif i == 3:
            columna = random.sample(range(46, 61), 5)
        elif i == 4:
            columna = random.sample(range(61, 76), 5)
        bingo.append(columna)
    return bingo


# Función para imprimir una cartilla de Bingo
def imprimir_bingo(numeros):
    print(" B    I    N    G    O")
    for fila in range(5):
        for columna in range(5):
            if fila == 2 and columna == 2:
                print(" * ", end="  ")  # Espacio del centro del bingo
            else:
                print(f"{numeros[columna][fila]:<3}", end="  ")
        print()


# Función para visualizar las compras
def visualizar_compras():
    global compras
    print("\n--- VISUALIZAR COMPRAS ---")

    # Título adicional con "Hola" y la hora actual
    hora_actual = datetime.now().strftime("%H:%M:%S")  # Obtiene la hora en formato HH:MM:SS
    print(f"Hora actual: {hora_actual}")

    if len(compras) == 0:
        print("No se han realizado compras aún.")
    else:
        # Agregar columna de Hora al lado de Fecha
        print(f"{'Nombre':<20}{'Fecha':<20}{'Hora':<10}{'Cantidad':<10}{'Total (S/)':<10}")
        total_recaudado = 0
        for compra in compras:
            # Extraer solo la hora de la fecha de compra
            hora_compra = compra['fecha'].split()[1]  # Obtener la hora del campo 'fecha'
            print(
                f"{compra['nombre']:<20}{compra['fecha'][:10]:<20}{hora_compra:<10}{compra['cantidad']:<10}{compra['costo_total']:<10}")
            total_recaudado += compra['costo_total']
        print(f"\nTotal recaudado: S/ {total_recaudado}")


def jugar_bingo():
    global compras, numeros_sorteados, juego_iniciado, compras_copia
    compras_copia = compras
    """
    Función para iniciar el juego de bingo.
    """
    if len(compras) == 0:
        print("No hay compras registradas. No se puede iniciar el juego.")
        return

    if juego_iniciado:
        print("El juego ya ha sido iniciado.")
        return

    print("\n--- JUGAR AL BINGO ---")
    juego_iniciado = True
    numeros_disponibles = list(range(1, 76))
    ganador_encontrado = False
    tabla_bingo = [
        ['--', '--', '--', '--', '--', '--', '--', '--', '--', "--", "--", "--", "--", "--", "--"],
        ['--', '--', '--', '--', '--', '--', '--', '--', '--', "--", "--", "--", "--", "--", "--"],
        ['--', '--', '--', '--', '--', '--', '--', '--', '--', "--", "--", "--", "--", "--", "--"],
        ['--', '--', '--', '--', '--', '--', '--', '--', '--', "--", "--", "--", "--", "--", "--"],
        ['--', '--', '--', '--', '--', '--', '--', '--', '--', "--", "--", "--", "--", "--", "--"]
    ]

    while numeros_disponibles and not ganador_encontrado:
        tecla = input("Presione 'S' para sortear el siguiente número: ").upper()
        if tecla == 'S':
            numero_sorteado = random.choice(numeros_disponibles)
            numeros_disponibles.remove(numero_sorteado)
            numeros_sorteados.append(numero_sorteado)
            print(f"\n    JUEGO DEL BINGO")
            print(f"\nNúmero sorteado: {numero_sorteado}")

            fila = 0
            numero_copia = numero_sorteado
            while numero_copia > 15:
                fila += 1
                numero_copia -= 15
            columna = numero_copia - 1
            tabla_bingo[fila][columna] = numero_sorteado

            letras_bingo = {0: "B", 1: "I", 2: "N", 3: "G", 4: "O"}
            for i in range(len(tabla_bingo)):
                for j in range(len(tabla_bingo[0]) + 1):
                    if j == 0:
                        print(letras_bingo[i], end=" ")
                    else:
                        print(tabla_bingo[i][j - 1], end=" ")
                print()
            # Marcar los números en las tarjetas
            for compra in compras:
                for bingo in compra['bingos']:
                    marcar_numero_en_bingo(bingo['numeros'], numero_sorteado)

            # Mostrar el tablero general actualizado
            print("\n--- TABLEROS ACTUALIZADOS ---")
            for compra in compras:
                print(f"\nPropietario: {compra['nombre']}")
                for bingo in compra['bingos']:
                    print(f"Número de serie: {bingo['serie']}")
                    imprimir_bingo(bingo['numeros'])

            # Verificar si hay ganador
            for compra in compras:
                for bingo in compra['bingos']:
                    if verificar_bingo(bingo['numeros']):
                        print("\n¡BINGO!")
                        print(f"Tarjeta ganadora con número de serie {bingo['serie']}")
                        print(f"Propietario: {compra['nombre']}")
                        print("Tarjeta ganadora:")
                        imprimir_bingo(bingo['numeros'])
                        guardar_resultados(numeros_sorteados, compra, bingo)
                        ganador_encontrado = True
                        break
                if ganador_encontrado:
                    break
        else:
            print("Entrada no válida. Presione 'S' para continuar.")

    if not ganador_encontrado:
        print("No hubo ganador en este juego.")
        guardar_resultados(numeros_sorteados, None, None)

        # Reiniciar el juego para futuras partidas
    juego_iniciado = False
    numeros_sorteados.clear()

# Función para marcar el número en la tarjeta de bingo
def marcar_numero_en_bingo(numeros_bingo, numero_sorteado):
    for columna in numeros_bingo:
        for idx, num in enumerate(columna):
            if isinstance(num, int):
                if num == numero_sorteado:
                    columna[idx] = str(num)+"*"

# Función para verificar si una tarjeta de bingo ha ganado
def verificar_bingo(numeros_bingo):
    # Verificar tarjeta
    for fila in range(5):
        for columna in range(5):
            if isinstance(numeros_bingo[columna][fila],int):
                return False
    return True

def guardar_resultados(numeros_sorteados, compra_ganadora, bingo_ganador):
    nombre_archivo = "resultados_bingo.txt"
    with open(nombre_archivo, "w") as archivo:
        archivo.write("===== Números sorteados en orden =====\n")
        archivo.write(", ".join(map(str, numeros_sorteados)) + "\n")
        archivo.write("\n===== Información de la tarjeta ganadora =====\n")
        archivo.write(f"Número de serie: {bingo_ganador['serie']}\n")
        archivo.write(f"Propietario: {compra_ganadora['nombre']}\n")
        archivo.write("Tarjeta ganadora:\n")
        for fila in range(5):
            for columna in range(5):
                num = bingo_ganador['numeros'][columna][fila]
                archivo.write(f"{num:3} ")
            archivo.write("\n")
    print(f"\nResultados guardados en {nombre_archivo}")

# Programa principal
def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            configurar_informacion()
        elif opcion == "2":
            if bingo_info["costo"] == 0:
                print("Primero debe configurar la información del Bingo.")
            else:
                comprar_bingos()
        elif opcion == "3":
            visualizar_compras()
        elif opcion == "4":
            jugar_bingo()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intente de nuevo.")


# Ejecutar el programa principal
if __name__ == "__main__":
    main()