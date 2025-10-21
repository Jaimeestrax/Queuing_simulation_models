# importación de las funciones del modelo que permiten hallar los calculos
from Model.model_PICM import (
    calcular_probabilidad_sistema_vacio,
    calcular_probabilidad_k_clientes,
    calcular_probabilidad_no_esperar,
    calcular_probabilidad_n_clientes,
    calcular_numero_esperado_clientes_cola,
    calcular_numero_esperado_clientes_sistema,
    calcular_numero_esperado_clientes_cola_no_vacia,
    calcular_tiempo_esperado_cola,
    calcular_tiempo_esperado_sistema,
    calcular_tiempo_esperado_cola_no_vacia,
    calcular_utilizacion_sistema,
    calcular_probabilidad_acumulada,
    calcular_costos_hora,
    calcular_costos_diarios
)

# interfaz del menu a mostrarse
def mostrar_menu_calculos():
    print("\n=== Cálculos disponibles para PICM (M/M/k) ===")
    print("1. Utilización del sistema (p)")
    print("2. Probabilidad de sistema vacío (p0)")
    print("3. Probabilidad de exactamente n clientes en el sistema (Pn)")
    print("4. Probabilidad acumulada (desde n hasta m clientes) (Pn)")
    print("5. Probabilidad de al menos k usuarios (Pk) → usuario espera")
    print("6. Probabilidad de no esperar (Pne)")
    print("7. Número esperado de clientes en cola (L)")
    print("8. Número esperado de clientes en el sistema (Lq)")
    print("9. Número esperado en cola no vacía (Ln)")
    print("10. Tiempo esperado en cola (W)")
    print("11. Tiempo esperado en el sistema (Wq)")
    print("12. Tiempo esperado en cola no vacía (Wn)")
    print("13. Calcular costos por hora")
    print("14. Calcular costos diarios")
    print("0. Volver al menú principal")

# registro de datos
def obtener_opcion_calculo():
    while True:
        try:
            opcion = int(input("\nSeleccione una opción de cálculo: "))
            if 0 <= opcion <= 14:
                return opcion
            else:
                print("Opción no válida. Ingrese un número entre 0 y 14")
        except ValueError:
            print("Por favor, ingrese un número válido")

def solicitar_n():
    while True:
        try:
            n = int(input("Ingrese el número de clientes (n ≥ 0): "))
            if n >= 0:
                return n
            else:
                print("n debe ser un entero no negativo")
        except ValueError:
            print("Ingrese un número entero válido")

def solicitar_rango_n():
    while True:
        try:
            desde = int(input("Ingrese el valor inicial (desde_n ≥ 0): "))
            if desde < 0:
                print("El valor inicial debe ser ≥ 0")
                continue
            hasta_input = input("Ingrese el valor final (hasta_n) o presione Enter para infinito: ")
            if hasta_input.strip() == "":
                return desde, None
            hasta = int(hasta_input)
            if hasta < desde:
                print("El valor final debe ser ≥ valor inicial")
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
        print("Entrada inválida. Se usarán costos = 0")
        return 0, 0, 0, 0

def solicitar_horas_laborables():
    while True:
        try:
            horas = float(input("Ingrese las horas laborables por día: "))
            if horas > 0:
                return horas
            else:
                print("Las horas deben ser mayores a 0")
        except ValueError:
            print("Ingrese un número válido")

# visualizacion de resultados
def mostrar_resultados_picm(params):
    lam = params['lam']
    mu = params['mu']
    k = params['k']

    # Validar estabilidad
    try:
        p = calcular_utilizacion_sistema(lam, mu, k)
        print(f"\nEl sistema es estable ya que p = {p:.6f} (< 1)")
    except ValueError as e:
        print(f"\nNo se pudo realizar el cálculo: {e}")
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
                p = calcular_utilizacion_sistema(lam, mu, k)
                print(f"\nProbabilidad de que el sistema este ocupado (p): {p:.6f} - ({p * 100}%)")
                print(f"Utilización del sistema: {p:.6f} - ({p * 100}%)")

            elif opcion == 2:
                p0 = calcular_probabilidad_sistema_vacio(lam, mu, k)
                print(f"\nProbabilidad de hallar el sistema vacío (p0): {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad de que todos los servidores esten desocupados a la vez: {p0:.6f} - ({p0 * 100}%)")

            elif opcion == 3:
                n = solicitar_n()
                pn = calcular_probabilidad_n_clientes(lam, mu, k, n)
                print(f"\nProbabilidad de hallar exactamente {n} usuario(s) dentro del sistema P({n}): {pn:.6f}")

            elif opcion == 4:
                desde, hasta = solicitar_rango_n()
                if hasta is None:
                    prob = calcular_probabilidad_acumulada(lam, mu, k, desde_n=desde)
                    print(f"\nProbabilidad de encontrar al menos {desde} cliente(s) en el sistema: {prob:.6f}")
                else:
                    prob = calcular_probabilidad_acumulada(lam, mu, k, desde_n=desde, hasta_n=hasta)
                    print(f"\nProbabilidad de encontrar desde {desde} a {hasta} cliente(s) en el sistema: {prob:.6f}")
            
            elif opcion == 5:
                pk = calcular_probabilidad_k_clientes(lam, mu, k)
                print(f"\nProbabilidad de que {k} usuario(s) que llega tenga que esperar (Pk): {pk:.6f}")
                print(f"Probabilidad de que haya {k} o más usuarios en el sistema: {pk:.6f}")

            elif opcion == 6:
                p_ne = calcular_probabilidad_no_esperar(lam, mu, k)
                print(f"\nProbabilidad de que un usuario que llega no tenga que esperar (Pne): {p_ne:.6f}")

            elif opcion == 7:
                lq = calcular_numero_esperado_clientes_cola(lam, mu, k)
                print(f"\nNúmero esperado de clientes en cola (lq): {lq:.2f}")

            elif opcion == 8:
                l = calcular_numero_esperado_clientes_sistema(lam, mu, k)
                print(f"\nNúmero esperado de clientes en el sistema (l): {l:.2f}")

            elif opcion == 9:
                ln = calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, k)
                print(f"\nNúmero esperado de clientes en cola no vacía (ln): {ln:.2f}")

            elif opcion == 10:
                wq = calcular_tiempo_esperado_cola(lam, mu, k)
                print(f"\nTiempo esperado en cola (wq): {wq:.2f} h/c")

            elif opcion == 11:
                w = calcular_tiempo_esperado_sistema(lam, mu, k)
                print(f"\nTiempo esperado en el sistema (wc): {w:.2f} h/c")

            elif opcion == 12:
                wn = calcular_tiempo_esperado_cola_no_vacia(lam, mu, k)
                print(f"\nTiempo esperado en cola no vacía (wn): {wn:.2f} h/c")

            elif opcion == 13:
                cte, cts, ctse, cs = solicitar_costos()
                costos = calcular_costos_hora(lam, mu, cte, cts, ctse, cs)
                print("\n=== Costos por hora ===")
                for clave, valor in costos.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/h")

            elif opcion == 14:
                cte, cts, ctse, cs = solicitar_costos()
                horas = solicitar_horas_laborables()
                costos_diarios = calcular_costos_diarios(lam, mu, k, cte, cts, ctse, cs, horas)
                print("\n=== Costos diarios ===")
                for clave, valor in costos_diarios.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}/d")

        except ValueError as e:
            print(f"\nSe ha presentado un error en el menú: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        if opcion != 0:
            input("\nPresione Enter para continuar...")