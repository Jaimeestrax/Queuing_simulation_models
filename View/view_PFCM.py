# importación de las funciones del modelo que permiten hallar los calculos
from Model.model_PFCM import (
    calcular_probabilidad_sistema_vacio,
    calcular_probabilidad_n_clientes,
    calcular_probabilidad_sistema_ocupado,
    calcular_probabilidad_no_esperar,
    calcular_numero_esperado_clientes_sistema,
    calcular_numero_esperado_clientes_cola,
    calcular_numero_esperado_clientes_cola_no_vacia,
    calcular_tiempo_esperado_cola,
    calcular_tiempo_esperado_sistema,
    calcular_tiempo_esperado_cola_no_vacia,
    calcular_probabilidad_acumulada,
    calcular_costos_hora,
    calcular_costos_diarios
)

# interfaz del menu a mostrarse
def mostrar_menu_calculos():
    print("\n=== Cálculos disponibles para PFCM (M/M/k/M/M) ===")
    print("1. Probabilidad de sistema vacío (P0)")
    print("2. Probabilidad de sistema ocupado (PE)")
    print("3. Probabilidad de no esperar (P_NE)")
    print("4. Probabilidad de exactamente n clientes en el sistema (Pn)")
    print("5. Probabilidad acumulada (desde n hasta m clientes)")
    print("6. Número esperado de clientes en cola (Lq)")
    print("7. Número esperado de clientes en el sistema (L)")
    print("8. Número esperado de clientes en cola no vacía (Ln)")
    print("9. Tiempo esperado en cola (Wq)")
    print("10. Tiempo esperado en el sistema (W)")
    print("11. Tiempo esperado en cola no vacía (Wn)")
    print("12. Calcular costos por hora")
    print("13. Calcular costos diarios")
    print("0. Volver al menú principal")

# registro de datos
def obtener_opcion_calculo():
    while True:
        try:
            opcion = int(input("\nSeleccione una opción de cálculo: "))
            if 0 <= opcion <= 13:
                return opcion
            else:
                print("Opción no válida. Ingrese un número entre 0 y 13")
        except ValueError:
            print("Por favor, ingrese un número válido")

def solicitar_n(M):
    while True:
        try:
            n = int(input(f"Ingrese el número de clientes (n entre 0 y {M}): "))
            if 0 <= n <= M:
                return n
            else:
                print(f"El valor de n debe estar entre 0 y {M}")
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
def mostrar_resultados_pfcm(params):
    lam = params['lam']
    mu = params['mu']
    k = params['k']
    M = params['M']

    # Validar que k y M sean enteros positivos y k <= M
    if k <= 0 or M <= 0:
        print("\nError: k y M deben ser enteros positivos")
        return
    if k > M:
        print(f"\nError: k ({k}) no puede ser mayor que M ({M})")
        return

    # Mostrar información contextual
    print(f"\nInformación contextual:")
    print(f"   - Población total (M): {M}")
    print(f"   - Número de servidores (k): {k}")
    print(f"   - Regla empírica: Si M < 30, se recomienda usar modelos de población finita.")
    if M < 30:
        print(f"   - Modelo de población finita es apropiado.")
    else:
        print(f"   - Podrías considerar un modelo de población infinita (como PICM) si es aplicable.")

    # Calcular P0 para validar si es posible continuar
    try:
        p0 = calcular_probabilidad_sistema_vacio(lam, mu, k, M)
        print(f"\nProbabilidad de sistema vacío (P0): {p0:.6f} - ({p0 * 100}%)")
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
                p0 = calcular_probabilidad_sistema_vacio(lam, mu, k, M)
                print(f"\nProbabilidad de hallar el sistema completamente vacío (P0): {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad de que todos los servidores estén desocupados u ociosos a la vez: {p0:.6f} - ({p0 * 100}%)")

            elif opcion == 2:
                pE = calcular_probabilidad_sistema_ocupado(lam, mu, k, M)
                print(f"\nProbabilidad de hallar el sistema completamente ocupado (PE): {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad de que un usuario que llega tenga que esperar: {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad de que haya k o más usuarios en el sistema: {pE:.6f} - ({pE * 100}%)")

            elif opcion == 3:
                pNE = calcular_probabilidad_no_esperar(lam, mu, k, M)
                print(f"\nProbabilidad de no esperar (P_NE): {pNE:.6f}")

            elif opcion == 4:
                n = solicitar_n(M)
                pn = calcular_probabilidad_n_clientes(lam, mu, k, M, n)
                print(f"\nProbabilidad de hallar exactamente {n} cliente(s) dentro del sistema (Pn): {pn:.6f}")

            elif opcion == 5:
                desde, hasta = solicitar_rango_n(M)
                prob = calcular_probabilidad_acumulada(lam, mu, k, M, desde_n=desde, hasta_n=hasta)
                print(f"\nProbabilidad de {desde} a {hasta} cliente(s) en el sistema: {prob:.6f}")

            elif opcion == 6:
                lq = calcular_numero_esperado_clientes_cola(lam, mu, k, M)
                print(f"\nNúmero esperado en cola (Lq): {lq:.2f} clientes")

            elif opcion == 7:
                l = calcular_numero_esperado_clientes_sistema(lam, mu, k, M)
                print(f"\nNúmero esperado en el sistema (L): {l:.2f} clientes")
                print(f"   - Clientes fuera del sistema (M-L): {M - l:.2f} clientes")

            elif opcion == 8:
                ln = calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, k, M)
                print(f"\nNúmero esperado en cola no vacía (Ln): {ln:.6f} clientes")

            elif opcion == 9:
                wq = calcular_tiempo_esperado_cola(lam, mu, k, M)
                print(f"\nTiempo esperado en cola (Wq): {wq:.2f} h/c")

            elif opcion == 10:
                w = calcular_tiempo_esperado_sistema(lam, mu, k, M)
                print(f"\nTiempo esperado en el sistema (W): {w:.2f} h/c")

            elif opcion == 11:
                wn = calcular_tiempo_esperado_cola_no_vacia(lam, mu, k, M)
                print(f"\nTiempo esperado en cola no vacía (Wn): {wn:.2f} h/c")

            elif opcion == 12:
                cte, cts, ctse, cs = solicitar_costos()
                costos = calcular_costos_hora(lam, mu, k, M, cte, cts, ctse, cs)
                print("\n=== Costos por hora ===")
                for clave, valor in costos.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/h")

            elif opcion == 13:
                cte, cts, ctse, cs = solicitar_costos()
                horas = solicitar_horas_laborables()
                costos_diarios = calcular_costos_diarios(lam, mu, k, M, cte, cts, ctse, cs, horas)
                print("\n=== Costos diarios ===")
                for clave, valor in costos_diarios.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/d")

        except ValueError as e:
            print(f"\nError en el menú: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        if opcion != 0:
            input("\nPresione Enter para continuar...")