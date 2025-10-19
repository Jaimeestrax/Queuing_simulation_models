# vinculación hacia las vistas
from View.view_PICS import mostrar_resultados_pics
from View.view_PICM import mostrar_resultados_picm
from View.view_PFCS import mostrar_resultados_pfcs
from View.view_PFCM import mostrar_resultados_pfcm

# interfaz del menu principal para escoger el modelo
def mostrar_menu():
    print("\n=== Bienvenido a la calculadora de sistemas de colas ===")
    print("Seleccione el modelo de cola:")
    print("1. PICS (M/M/1)")
    print("2. PICM (M/M/k)")
    print("3. PFCS (M/M/1/M/M)")
    print("4. PFCM (M/M/k/M/M)")
    print("0. Salir")

# operaciones de ingreso de datos
def obtener_opcion():
    while True:
        try:
            opcion = int(input("\nIngrese su opción: "))
            if opcion in [0, 1, 2, 3, 4]:
                return opcion
            else:
                print("Opción no válida. Intente de nuevo")
        except ValueError:
            print("Por favor, ingrese un número válido")

def obtener_parametros_pics():
    print("\n--- Parámetros para el modelo PICS (M/M/1) ---")
    
    lam = float(input("Ingrese la tasa de llegada (lambda): "))
    mu = float(input("Ingrese la tasa de servicio (mu): "))
    if lam <= 0 or mu <= 0:
        raise ValueError("Las tasas deben ser positivas")
    if lam >= mu:
        print("Advertencia: El sistema no cumple la condición de estabilidad")
    
    return {"lam": lam, "mu": mu}

def obtener_parametros_picm():
    print("\n--- Parámetros para PICM (M/M/k) ---")

    lam = float(input("Ingrese la tasa de llegada (lambda): "))
    mu = float(input("Ingrese la tasa de servicio por servidor (mu): "))
    k = int(input("Ingrese el número de servidores (k): "))
    if lam <= 0 or mu <= 0 or k <= 0:
        raise ValueError("Todos los parámetros deben ser positivos")
    if lam >= c * mu:
        print("Advertencia: El sistema no cumple con la condición de estabilidad")
    
    return {"lam": lam, "mu": mu, "k": k}

def obtener_parametros_pfcs():
    print("\n--- Parámetros para PFCS (M/M/1/M/M) ---")

    lam = float(input("Ingrese la tasa de llegada (lambda): "))
    mu = float(input("Ingrese la tasa de servicio (mu): "))
    K = int(input("Ingrese la capacidad máxima del sistema (M): "))
    if lam <= 0 or mu <= 0 or M <= 0:
        raise ValueError("Todos los parámetros deben ser positivos")
    
    return {"lam": lam, "mu": mu, "M": M}

def obtener_parametros_pfcm():
    print("\n--- Parámetros para PFCM (M/M/k/M/M) ---")

    lam = float(input("Ingrese la tasa de llegada (lambda): "))
    mu = float(input("Ingrese la tasa de servicio por servidor (mu): "))
    k = int(input("Ingrese el número de servidores (k): "))
    M = int(input("Ingrese la capacidad máxima del sistema (M): "))
    if lam <= 0 or mu <= 0 or k <= 0 or M <= 0:
        raise ValueError("Todos los parámetros deben ser positivos.")
    if M < k:
        print("Advertencia: La capacidad es menor que el número de servidores")
    
    return {"lam": lam, "mu": mu, "k": k, "M": M}

# vinculación con las vistas y el menu según las opciones
def ejecutar_opcion(opcion):
    try:
        if opcion == 1:
            params = obtener_parametros_pics()
            mostrar_resultados_pics(params)
        elif opcion == 2:
            params = obtener_parametros_picm()
            mostrar_resultados_picm(params)
        elif opcion == 3:
            params = obtener_parametros_pfcs()
            mostrar_resultados_pfcs(params)
        elif opcion == 4:
            params = obtener_parametros_pfcm()
            mostrar_resultados_pfcm(params)
        elif opcion == 0:
            print("Saliendo del programa...")
            return False
    except ValueError as e:
        print(f"Error en los datos ingresados: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return True

# inicio del programa
def iniciar():
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = obtener_opcion()
        continuar = ejecutar_opcion(opcion)