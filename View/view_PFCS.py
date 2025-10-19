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
    calcular_tiempo_esperado_cola_no_vacia
)

# interfaz del menu a mostrarse
def mostrar_menu_calculos():
    print("\n=== Cálculos disponibles para PFCS (M/M/1/M/M) ===")
    print("1. Probabilidad de hallar sistema vacío")
    print("2. Probabilidad de hallar sistema ocupado")
    print("3. Probabilidad de hallar exactamente n clientes dentro del sistema")
    print("4. Número esperado de clientes en el sistema")
    print("5. Número esperado de clientes en cola")
    print("6. Número esperado de clientes en cola no vacía")
    print("7. Tiempo esperado en cola")
    print("8. Tiempo esperado en el sistema")
    print("9. Tiempo esperado en cola no vacía")
    print("10. Probabilidad acumulada (desde n hasta m clientes)")
    print("0. Volver al menú principal")

# registro de datos
def obtener_opcion_calculo():
    while True:
        try:
            opcion = int(input("\nSeleccione una opción de cálculo: "))
            if 0 <= opcion <= 10:
                return opcion
            else:
                print("Opción no válida. Ingrese un número entre 0 y 10")
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
                print(f"\nProbabilidad de hallar el sistema vacío u ocioso: {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tienen los usuarios de no esperar: {p0:.6f} - ({p0 * 100}%)")
                print(f"Probabilidad que tiene los usuarios de ser atendidos sin esperar en cola: {p0:.6f} - ({p0 * 100}%)")

            elif opcion == 2:
                pE = calcular_probabilidad_sistema_ocupado(lam, mu, M)
                print(f"\nProbabilidad de sistema ocupado: {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad de utilización del sistema: {pE:.6f} - ({pE * 100}%)")
                print(f"Probabilidad que tienen los usuarios de esperar para ser atendidos: {pE:.6f} - ({pE * 100}%)")

            elif opcion == 3:
                n = solicitar_n(M)
                pn = calcular_probabilidad_n_clientes(lam, mu, M, n)
                print(f"\nProbabilidad de hallar exactamente {n} cliente(s) en el sistema: {pn:.6f}")

            elif opcion == 4:
                l = calcular_numero_esperado_clientes_sistema(lam, mu, M)
                print(f"\nNúmero esperado de clientes en el sistema: {l:.2f} clientes")

            elif opcion == 5:
                lq = calcular_numero_esperado_clientes_cola(lam, mu, M)
                print(f"\nNúmero esperado de clientes en la cola: {lq:.2f} clientes")

            elif opcion == 6:
                ln = calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, M)
                print(f"\nNúmero esperado de clientes en la cola no vacía: {ln:.2f} clientes")

            elif opcion == 7:
                wq = calcular_tiempo_esperado_cola(lam, mu, M)
                print(f"\nTiempo esperado en cola: {wq:.2f} h/c")

            elif opcion == 8:
                w = calcular_tiempo_esperado_sistema(lam, mu, M)
                print(f"\nTiempo esperado en el sistema: {w:.2f} h/c")

            elif opcion == 9:
                wn = calcular_tiempo_esperado_cola_no_vacia(lam, mu, M)
                print(f"\nTiempo esperado en cola no vacía: {wn:.2f} h/c")

            elif opcion == 10:
                desde, hasta = solicitar_rango_n(M)
                prob = calcular_probabilidad_acumulada(lam, mu, M, desde_n=desde, hasta_n=hasta)
                print(f"\nProbabilidad de {desde} a {hasta} cliente(s) en el sistema: {prob:.6f}")

        except ValueError as e:
            print(f"\nError en el menú: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        if opcion != 0:
            input("\nPresione Enter para continuar...")