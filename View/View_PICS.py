# importación de las funciones del modelo que permiten hallar los calculos
from Model.model_PICS import (
    calcular_utilizacion_sistema,
    calcular_probabilidad_sistema_vacio,
    calcular_probabilidad_n_clientes,
    calcular_probabilidad_acumulada,
    calcular_numero_esperado_clientes_sistema,
    calcular_numero_esperado_clientes_cola,
    calcular_numero_esperado_clientes_cola_no_vacia,
    calcular_tiempo_esperado_sistema,
    calcular_tiempo_esperado_cola,
    calcular_tiempo_esperado_cola_no_vacia,
    calcular_costos_hora,
    calcular_costos_diarios
)

# interfaz del menu a mostrarse
def mostrar_menu_calculos():
    print("\n=========== Cálculos disponibles para el modelo PICS ========")
    print("1. Probabilidad de hallar el sistema ocupado")
    print("2. Probabilidad de hallar el sistema vacio")
    print("3. Probabilidad de hallar exactamente n clientes en el sistema")
    print("4. Probabilidad de hallar desde n hasta m clientes")
    print("5. Número esperado de clientes en el sistema")
    print("6. Número esperado de clientes en cola")
    print("7. Número esperado de clientes en cola no vacía")
    print("8. Tiempo esperado en el sistema")
    print("9. Tiempo esperado en cola")
    print("10. Tiempo esperado en cola no vacía")
    print("11. Calcular costos por hora")
    print("12. Calcular costos diarios")
    print("0. Volver al menú principal")

# toma de datos
def obtener_opcion_calculo():
    while True:
        try:
            opcion = int(input("\nSeleccione una opción de cálculo: "))
            if 0 <= opcion <= 12:
                return opcion
            else:
                print("Opción no válida. Ingrese un número entre 0 y 12")
        except ValueError:
            print("Por favor ingrese un número válido")

def solicitar_n():
    while True:
        try:
            n = int(input("Ingrese el número de clientes (n ≥ 0): "))
            if n >= 0:
                return n
            else:
                print("El valor de n no puede ser negativo")
        except ValueError:
            print("Ingrese un número entero válido.")

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
def mostrar_resultados_pics(params):
    lam = params['lam']
    mu = params['mu']

    # Validar condición de estabilidad
    try:
        p = calcular_utilizacion_sistema(lam, mu)
        print(f"\nEl sistema es estable ya que p = {p:.6f} < 1")
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
                p = calcular_utilizacion_sistema(lam, mu)
                # interpretaciones de la probabilidad encontrada
                print(f"\nProbabilidad de que el sistema este ocupado: {p:.6f} - ({p * 100}%)")
                print(f"Probabilidad que tienen los usuarios de ser atendidos: {p:.6f} - ({p * 100}%)")

            elif opcion == 2:
                p0 = calcular_probabilidad_sistema_vacio(lam, mu)
                # interpretaciones de la probabilidad encontrada
                print(f"\nProbabilidad de hallar el sistema vacio u ocioso: {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tienen los usuarios de no esperar: {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tiene los usuarios de ser atendidos sin esperar en cola: {p0:.6f} - ({p0 * 100}%)")

            elif opcion == 3:
                n = solicitar_n()
                pn = calcular_probabilidad_n_clientes(lam, mu, n)
                print(f"\nProbabilidad de encontrar {n} usuario(s) en el sistema: {pn:.6f}")

            elif opcion == 4:
                desde, hasta = solicitar_rango_n()
                # interpretaciones de la probabilidad encontrada
                if hasta is None:
                    prob = calcular_probabilidad_acumulada(lam, mu, desde_n=desde)
                    print(f"\nProbabilidad de encontrar al menos {desde} usuario(s) en el sistema: {prob:.6f}")
                else:
                    prob = calcular_probabilidad_acumulada(lam, mu, desde_n=desde, hasta_n=hasta)
                    print(f"\nProbabilidad de encontrar desde {desde} a {hasta} usuario(s) en el sistema: {prob:.6f}")

            elif opcion == 5:
                l = calcular_numero_esperado_clientes_sistema(lam, mu)
                print(f"\nNúmero esperado de clientes en el sistema (promedio clientes): {l:.2f} clientes")

            elif opcion == 6:
                lq = calcular_numero_esperado_clientes_cola(lam, mu)
                print(f"\nNúmero esperado de clientes en cola (promedio clientes en cola): {lq:.2f} clientes")

            elif opcion == 7:
                ln = calcular_numero_esperado_clientes_cola_no_vacia(lam, mu)
                print(f"\nNúmero esperado de clientes en cola no vacía (solo cuando habia cola): {ln:.2f} clientes")

            elif opcion == 8:
                w = calcular_tiempo_esperado_sistema(lam, mu)
                print(f"\nTiempo esperado en el sistema: {w:.2f} c/h")

            elif opcion == 9:
                wq = calcular_tiempo_esperado_cola(lam, mu)
                print(f"\nTiempo esperado en cola: {wq:.2f} c/h")

            elif opcion == 10:
                wn = calcular_tiempo_esperado_cola_no_vacia(lam, mu)
                print(f"\nTiempo esperado en cola no vacía: {wn:.2f} c/h")

            elif opcion == 11:
                cte, cts, ctse, cs = solicitar_costos()
                costos = calcular_costos_hora(lam, mu, cte, cts, ctse, cs)
                print("\n=== Costos por hora ===")
                for clave, valor in costos.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}")

            elif opcion == 12:
                cte, cts, ctse, cs = solicitar_costos()
                horas = solicitar_horas_laborables()
                costos_diarios = calcular_costos_diarios(lam, mu, cte, cts, ctse, cs, horas)
                print("\n=== Costos diarios ===")
                for clave, valor in costos_diarios.items():
                    print(f"{clave.replace('_', ' ').title()}: ${valor:.4f}")

        except ValueError as e:
            print(f"\nSe ha presentado un error en el menú: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        if opcion != 0:
            input("\nPresione Enter para continuar...")