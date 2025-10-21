# importación de las funciones del modelo que permiten hallar los calculos
from Model.model_PFCS import (
    calcular_probabilidad_sistema_vacio,
    calcular_probabilidad_sistema_ocupado,
    calcular_probabilidad_n_clientes,
    calcular_probabilidad_acumulada,
    calcular_numero_esperado_clientes_sistema,
    calcular_numero_esperado_clientes_cola,
    calcular_numero_esperado_clientes_cola_no_vacia,
    calcular_tiempo_esperado_cola,
    calcular_tiempo_esperado_sistema,
    calcular_tiempo_esperado_cola_no_vacia,
    calcular_costos_diarios,
    calcular_costos_hora
)

# interfaz del menu a mostrarse
def mostrar_menu_calculos():
    print("\n=== Cálculos disponibles para PFCS (M/M/1/M/M) ===")
    print("1. Probabilidad de hallar sistema vacío (p0)")
    print("2. Probabilidad de hallar sistema ocupado (pE)")
    print("3. Probabilidad de hallar exactamente n clientes dentro del sistema (Pn)")
    print("4. Probabilidad acumulada (desde n hasta m clientes) (Pn)")
    print("5. Número esperado de clientes en el sistema (l)")
    print("6. Número esperado de clientes en cola (lq)")
    print("7. Número esperado de clientes en cola no vacía (ln)")
    print("8. Tiempo esperado en cola (wq)")
    print("9. Tiempo esperado en el sistema (w)")
    print("10. Tiempo esperado en cola no vacía (wn)")
    print("11. Calcular costos por hora")
    print("12. Calcular costos diarios")
    print("0. Volver al menú principal")

# registro de datos
def obtener_opcion_calculo():
    while True:
        try:
            opcion = int(input("\nSeleccione una opción de cálculo: "))
            if 0 <= opcion <= 12:
                return opcion
            else:
                print("Opción no válida. Ingrese un número entre 0 y 12")
        except ValueError:
            print("Por favor, ingrese un número válido")

def solicitar_n(M):
    while True:
        try:
            n = int(input(f"Ingrese el número de clientes (n entre 0 y {M}): "))
            if 0 <= n <= M:
                return n
            else:
                print(f"n debe estar entre 0 y {M}")
        except ValueError:
            print("Ingrese un número entero válido")

def solicitar_rango_n(M):
    while True:
        try:
            desde = int(input(f"Ingrese el valor inicial (desde_n entre 0 y {M}): "))
            if desde < 0 or desde > M:
                print(f"El valor inicial debe estar entre 0 y {M}")
                continue
            hasta_input = input(f"Ingrese el valor final (hasta_n) o presione Enter para {M}: ")
            if hasta_input.strip() == "":
                return desde, M
            hasta = int(hasta_input)
            if hasta < desde or hasta > M:
                print(f"El valor final debe estar entre {desde} y {M}")
                continue
            return desde, hasta
        except ValueError:
            print("Ingrese valores enteros válidos")

def solicitar_costos():
    print("\n--- Ingrese los costos unitarios (deje en blanco para 0) ---")
    try:
        cte = float(input("Costo por tiempo en cola (CTE, $/h): ") or "0")
        cts = float(input("Costo por tiempo en sistema (CTS, $/h): ") or "0")
        ctse = float(input("Costo por tiempo en servicio (CTSE, $/h): ") or "0")
        cs = float(input("Costo del servidor por hora (Cs, $/h): ") or "0")
        return cte, cts, ctse, cs
    except ValueError:
        print("Entrada inválida. Se usarán costos = 0.")
        return 0, 0, 0, 0

def solicitar_horas_laborables():
    while True:
        try:
            horas = float(input("Ingrese las horas laborables por día: "))
            if horas > 0:
                return horas
            else:
                print("Las horas deben ser mayores a 0.")
        except ValueError:
            print("Ingrese un número válido.")

# visualizacion de resultados
def mostrar_resultados_pfcs(params):
    lam = params['lam']
    mu = params['mu']
    M = params['M']

    # Validar que M sea entero positivo
    if M <= 0:
        print("\nError: La población M debe ser un entero positivo.")
        return

    # Mostrar información contextual
    print(f"\nInformación contextual:")
    print(f"   - Población total (M): {M}")
    print(f"   - Regla empírica: Si M < 30, se recomienda usar modelos de población finita.")
    if M < 30:
        print(f"   - Modelo de población finita es apropiado.")
    else:
        print(f"   - Podrías considerar un modelo de población infinita (como PICS) si es aplicable.")
    
    # Calcular P0 para validar si es posible continuar
    try:
        p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)
        print(f"\nProbabilidad de sistema vacío: {p0:.6f} - ({p0 * 100}%)")
    except ValueError as e:
        print(f"\nNo se pueden realizar cálculos: {e}")
        return

    # opciones del menu
    continuar = True
    while continuar:
        mostrar_menu_calculos()
        opcion = obtener_opcion_calculo()

        try:
            if opcion == 0:
                continuar = False

            elif opcion == 1:
                p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)
                print(f"\nProbabilidad de hallar el sistema vacío u ocioso (p0): {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tienen los usuarios de no esperar: {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tiene los usuarios de ser atendidos sin esperar en cola: {p0:.6f} - ({p0 * 100}%)")

            elif opcion == 2:
                pE = calcular_probabilidad_sistema_ocupado(lam, mu, M)
                print(f"\nProbabilidad de sistema ocupado (pE): {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad de utilización del sistema: {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad que tienen los usuarios de esperar para ser atendidos: {pE:.6f} - ({pE * 100}%)")

            elif opcion == 3:
                n = solicitar_n(M)
                pn = calcular_probabilidad_n_clientes(lam, mu, M, n)
                print(f"\nProbabilidad de hallar exactamente {n} cliente(s) en el sistema P({n}): {pn:.6f}")

            elif opcion == 4:
                desde, hasta = solicitar_rango_n(M)
                prob = calcular_probabilidad_acumulada(lam, mu, M, desde_n=desde, hasta_n=hasta)
                print(f"\nProbabilidad de {desde} a {hasta} cliente(s) en el sistema: {prob:.6f}")

            elif opcion == 5:
                l = calcular_numero_esperado_clientes_sistema(lam, mu, M)
                print(f"\nNúmero esperado de clientes en el sistema (l): {l:.2f} clientes")

            elif opcion == 6:
                lq = calcular_numero_esperado_clientes_cola(lam, mu, M)
                print(f"\nNúmero esperado de clientes en la cola (lq): {lq:.2f} clientes")

            elif opcion == 7:
                ln = calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, M)
                print(f"\nNúmero esperado de clientes en la cola no vacía (ln): {ln:.2f} clientes")

            elif opcion == 8:
                wq = calcular_tiempo_esperado_cola(lam, mu, M)
                print(f"\nTiempo esperado en cola (wq): {wq:.2f} h/c")

            elif opcion == 9:
                w = calcular_tiempo_esperado_sistema(lam, mu, M)
                print(f"\nTiempo esperado en el sistema (w): {w:.2f} h/c")

            elif opcion == 10:
                wn = calcular_tiempo_esperado_cola_no_vacia(lam, mu, M)
                print(f"\nTiempo esperado en cola no vacía (wn): {wn:.2f} h/c")

            elif opcion == 11:
                cte, cts, ctse, cs = solicitar_costos()
                costos = calcular_costos_hora(lam, mu, M, cte, cts, ctse, cs)
                print("\n=== Costos por hora ===")
                for clave, valor in costos.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/h")

            elif opcion == 12:
                cte, cts, ctse, cs = solicitar_costos()
                horas = solicitar_horas_laborables()
                costos_diarios = calcular_costos_diarios(lam, mu, M, cte, cts, ctse, cs, horas)
                print("\n=== Costos diarios ===")
                for clave, valor in costos_diarios.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/d")

        except ValueError as e:
            print(f"\nError en el menú: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        if opcion != 0:
            input("\nPresione Enter para continuar...")