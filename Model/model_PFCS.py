'''
Nota sobre población finita (M):
    - M es el tamaño total de la población de clientes potenciales.
    - Cuando M < 30, se recomienda usar modelos de población finita (como este).
    - La llegada de un cliente afecta la tasa de futuras llegadas, ya que hay menos clientes disponibles fuera del sistema.
    - Condición de estabilidad: siempre se cumple porque M es finito (el sistema nunca se "satura" en el sentido tradicional).
'''

import math

'''1.
Probabilidad de hallar el sistema vacío u ocioso
Probabilidad que tienen los usuarios de no esperar o de ser atendidos sin esperar en cola
'''
def calcular_probabilidad_sistema_vacio(lam, mu, M):
    # Fórmula: P0 = 1 / Σ_{n=0}^{n=M} [ M! / (M-n)! * p^n ] -> Donde p = λ / μ
    if M <= 0:
        raise ValueError("La población M debe ser un entero positivo.")
    if M > 30:  # Límite práctico
        print(f"Advertencia: M = {M} es muy grande. Considera si realmente necesitas población finita.")

    p = lam / mu

    suma = 0
    # n desde 0 hasta M
    for n in range(M + 1):
        try:
            termino = math.factorial(M) / math.factorial(M - n) * (p ** n)
            suma += termino
        except OverflowError:
            raise ValueError(f"Overflow al calcular factorial({M}). M es demasiado grande.")

    if suma == 0:
        raise ValueError("Suma de términos igual a cero, porfavor verifique los parámetros")

    p0 = 1 / suma
    return p0

'''2.
Probabilidad de hallar el sistema ocupado
Utilización del sistema
Probabilidad que tienen los usuarios de esperar para ser atendidos
'''
def calcular_probabilidad_sistema_ocupado(lam, mu, M):
    # Fórmula: PE = 1 - P0
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)
    pE = 1 - p0
    return pE

'''3.
Probabilidad de hallar exactamente n clientes dentro del sistema
'''
def calcular_probabilidad_n_clientes(lam, mu, M, n):
    # Fórmula: Pn = [M! / (M-n)!] * (λ/μ)^n * P0 -> Para n = 0, 1, 2, ..., M
    if n < 0 or n > M:
        raise ValueError(f"El valor de n debe estar entre 0 y {M}")

    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)

    pn = math.factorial(M) / math.factorial(M - n) * (p ** n) * p0
    return pn

'''4.
Probabilidad de encontrar desde_n hasta_n clientes
'''
def calcular_probabilidad_acumulada(lam, mu, M, desde_n=0, hasta_n=None):
    if hasta_n is not None:
        total = 0
        for n in range(desde_n, hasta_n + 1):
            total += calcular_probabilidad_n_clientes(lam, mu, M, n)
        return total
    else:
        # Suma desde_n hasta M
        if desde_n == 0:
            return 1.0
        acumulado_hasta_desde_n_menos_1 = 0
        for n in range(0, desde_n):
            acumulado_hasta_desde_n_menos_1 += calcular_probabilidad_n_clientes(lam, mu, M, n)
        return 1 - acumulado_hasta_desde_n_menos_1

'''5.
Número esperado de clientes en el sistema
'''
def calcular_numero_esperado_clientes_sistema(lam, mu, M):
    # Fórmula: L = M - (μ/λ) * (1 - P0)
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)
    l = M - (mu / lam) * (1 - p0)
    return l

'''6.
Número esperado de clientes en la cola
'''
def calcular_numero_esperado_clientes_cola(lam, mu, M):
    # Fórmula: Lq = M - ((λ + μ)/λ) * (1 - P0)
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, M)
    lq = M - ((lam + mu) / lam) * (1 - p0)
    return lq

'''7.
Número esperado de clientes en la cola no vacía
'''
def calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, M):
    # Fórmula: Ln = Lq / PE
    lq = calcular_numero_esperado_clientes_cola(lam, mu, M)
    pE = calcular_probabilidad_sistema_ocupado(lam, mu, M)
    if pE == 0:
        raise ValueError("PE es 0 y no se puede dividir por cero")
    ln = lq / pE
    return ln

'''8.
Tiempo esperado en cola
'''
def calcular_tiempo_esperado_cola(lam, mu, M):
    # Fórmula: Wq = Lq / [(M - L) * λ]
    lq = calcular_numero_esperado_clientes_cola(lam, mu, M)
    l = calcular_numero_esperado_clientes_sistema(lam, mu, M)
    denominador = (M - l) * lam
    if denominador <= 0:
        raise ValueError("Denominador menor o igual a 0. Verifique parámetros")
    wq = lq / denominador
    return wq

'''9.
Tiempo esperado en el sistema
'''
def calcular_tiempo_esperado_sistema(lam, mu, M):
    # Fórmula: W = Wq + 1/μ
    wq = calcular_tiempo_esperado_cola(lam, mu, M)
    w = wq + (1 / mu)
    return w

'''10.
Tiempo esperado en cola para colas no vacías
'''
def calcular_tiempo_esperado_cola_no_vacia(lam, mu, M):
    # Fórmula: Wn = Wq / PE
    wq = calcular_tiempo_esperado_cola(lam, mu, M)
    pE = calcular_probabilidad_sistema_ocupado(lam, mu, M)
    if pE == 0:
        raise ValueError("PE es 0 y no se puede dividir por cero")
    wn = wq / pE
    return wn

'''11.
Calcula costos por hora
'''
def calcular_costos_hora(lam, mu, M, cte=0, cts=0, ctse=0, cs=0):

    Lq = calcular_numero_esperado_clientes_cola(lam, mu, M)
    L = calcular_numero_esperado_clientes_sistema(lam, mu, M)
    Ls = L - Lq  # Clientes en servicio

    costo_cola = cte * Lq
    costo_sistema = cts * L
    costo_servicio = ctse * Ls
    costo_servidor = cs  # Solo un servidor

    costo_total = costo_cola + costo_sistema + costo_servicio + costo_servidor

    return {
        "costo_tiempo_cola": costo_cola,
        "costo_tiempo_sistema": costo_sistema,
        "costo_tiempo_servicio": costo_servicio,
        "costo_servidor": costo_servidor,
        "costo_total_por_hora": costo_total
    }

'''12.
Calcula costos diarios
'''
def calcular_costos_diarios(lam, mu, M, cte, cts, ctse, cs, horas_laborables):

    costos_hora = calcular_costos_hora(lam, mu, M, cte, cts, ctse, cs)
    costo_total_diario = costos_hora["costo_total_por_hora"] * horas_laborables

    return {
        "costo_diario_tiempo_cola": costos_hora["costo_tiempo_cola"] * horas_laborables,
        "costo_diario_tiempo_sistema": costos_hora["costo_tiempo_sistema"] * horas_laborables,
        "costo_diario_tiempo_servicio": costos_hora["costo_tiempo_servicio"] * horas_laborables,
        "costo_diario_servidor": costos_hora["costo_servidor"] * horas_laborables,
        "costo_diario_total": costo_total_diario
    }