import math

'''1.
Probabilidad de hallar el sistema completamente vacío
Probabilidad de que todos los servidores estén desocupados u ociosos a la vez
'''
def calcular_probabilidad_sistema_vacio(lam, mu, k, M):
    # Fórmula: P0 = 1 / [ Σ_{n=0}^{n=k-1} (M! / ((M-n)! n!)) * ρ^n + Σ_{n=k}^{n=M} (M! / ((M-n)! k! k^(n-k))) * ρ^n ] -> Donde ρ = λ / μ
    if k <= 0 or M <= 0:
        raise ValueError("k y M deben ser enteros positivos")
    if k > M:
        raise ValueError("k no puede ser mayor que M")

    p = lam / mu

    suma = 0.0

    # Primera suma: n desde 0 hasta k-1
    for n in range(k):
        termino = math.factorial(M) / (math.factorial(M - n) * math.factorial(n)) * (p ** n)
        suma += termino

    # Segunda suma: n desde k hasta M
    for n in range(k, M + 1):
        termino = math.factorial(M) / (math.factorial(M - n) * math.factorial(k) * (k ** (n - k))) * (p ** n)
        suma += termino

    if suma == 0:
        raise ValueError("La suma de términos es cero. Verifica los parámetros")

    p0 = 1 / suma
    return p0

'''2.
Probabilidad de hallar exactamente n clientes dentro del sistema
'''
def calcular_probabilidad_n_clientes(lam, mu, k, M, n):
    """
    Fórmula:
    Pn = 
        P0 * (M! / ((M-n)! n!)) * (λ/μ)^n       si 0 ≤ n ≤ k
        P0 * (M! / ((M-n)! k! k^(n-k))) * (λ/μ)^n   si k ≤ n ≤ M
    """
    if n < 0 or n > M:
        raise ValueError(f"El valor de n debe estar entre 0 y {M}")

    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, k, M)

    if n <= k:
        pn = p0 * (math.factorial(M) / (math.factorial(M - n) * math.factorial(n))) * (p ** n)
    else:  # n > k
        pn = p0 * (math.factorial(M) / (math.factorial(M - n) * math.factorial(k) * (k ** (n - k)))) * (p ** n)

    return pn

'''3.
Probabilidad de hallar el sistema completamente ocupado
Probabilidad de que un usuario que llega tenga que esperar
Probabilidad de que haya k o más usuarios en el sistema
'''
def calcular_probabilidad_sistema_ocupado(lam, mu, k, M):
    # Fórmula: PE = Σ_{n=k}^{n=M} Pn = 1 - Σ_{n=0}^{n=k-1} Pn
    suma_hasta_k_menos_1 = 0
    for n in range(k):  # n desde 0 hasta k-1
        suma_hasta_k_menos_1 += calcular_probabilidad_n_clientes(lam, mu, k, M, n)
    pE = 1 - suma_hasta_k_menos_1
    return pE

'''4.
Probabilidad de no esperar
'''
def calcular_probabilidad_no_esperar(lam, mu, k, M):
    # Fórmula: P_NE = 1 - PE
    pE = calcular_probabilidad_sistema_ocupado(lam, mu, k, M)
    pNE = 1 - pE
    return pNE

'''5.
Número esperado de clientes en el sistema
'''
def calcular_numero_esperado_clientes_sistema(lam, mu, k, M):
    """
    Fórmula: L = Σ_{n=0}^{n=k-1} n*Pn + Σ_{n=k}^{n=M} (n-k)*Pn + k*(1 - Σ_{n=0}^{n=k-1} Pn)
    
    Explicación:
    - Primer término: clientes en servicio cuando hay menos de k clientes.
    - Segundo término: clientes en cola (n-k) cuando hay n ≥ k.
    - Tercer término: k servidores siempre ocupados cuando hay k o más clientes.
    """

    # Suma 1: Σ_{n=0}^{n=k-1} n * Pn
    suma1 = 0.0
    for n in range(k):
        pn = calcular_probabilidad_n_clientes(lam, mu, k, M, n)
        suma1 += n * pn

    # Suma 2: Σ_{n=k}^{n=M} (n - k) * Pn
    suma2 = 0.0
    for n in range(k, M + 1):
        pn = calcular_probabilidad_n_clientes(lam, mu, k, M, n)
        suma2 += (n - k) * pn

    # Suma 3: k * (1 - Σ_{n=0}^{n=k-1} Pn)
    suma_pn_hasta_k_menos_1 = 0.0
    for n in range(k):
        suma_pn_hasta_k_menos_1 += calcular_probabilidad_n_clientes(lam, mu, k, M, n)
    suma3 = k * (1 - suma_pn_hasta_k_menos_1)

    l = suma1 + suma2 + suma3
    return l

'''6.
Número esperado de clientes en la cola
'''
def calcular_numero_esperado_clientes_cola(lam, mu, k, M):
    # Fórmula: Lq = Σ_{n=k+1}^{n=M} (n - k) * Pn
    lq = 0.0
    for n in range(k + 1, M + 1):
        pn = calcular_probabilidad_n_clientes(lam, mu, k, M, n)
        lq += (n - k) * pn
    return lq

'''7.
Número esperado de clientes en la cola no vacía
'''
def calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, k, M):
    # Fórmula: Ln = Lq / PE
    lq = calcular_numero_esperado_clientes_cola(lam, mu, k, M)
    pE = calcular_probabilidad_sistema_ocupado(lam, mu, k, M)
    if pE == 0:
        raise ValueError("PE es 0 y no se puede dividir por cero")
    ln = lq / pE
    return ln

'''8.
Tiempo esperado en cola
'''
def calcular_tiempo_esperado_cola(lam, mu, k, M):
    # Fórmula: Wq = Lq / [(M - L) * λ]
    lq = calcular_numero_esperado_clientes_cola(lam, mu, k, M)
    l = calcular_numero_esperado_clientes_sistema(lam, mu, k, M)
    denominador = (M - l) * lam
    if denominador <= 0:
        raise ValueError("Denominador menor o igual a 0. Verifica los parámetros")
    wq = lq / denominador
    return wq

'''9.
Tiempo esperado en el sistema
'''
def calcular_tiempo_esperado_sistema(lam, mu, k, M):
    # Fórmula: W = Wq + 1/μ
    wq = calcular_tiempo_esperado_cola(lam, mu, k, M)
    w = wq + (1 / mu)
    return w

'''10.
Tiempo esperado en cola para colas no vacías
'''
def calcular_tiempo_esperado_cola_no_vacia(lam, mu, k, M):
    # Fórmula: Wn = Wq / PE
    wq = calcular_tiempo_esperado_cola(lam, mu, k, M)
    pE = calcular_probabilidad_sistema_ocupado(lam, mu, k, M)
    if pE == 0:
        raise ValueError("PE es 0 y no se puede dividir por cero")
    wn = wq / pE
    return wn

'''11.
Probabilidad de encontrar entre desde_n hast_n clientes
'''
def calcular_probabilidad_acumulada(lam, mu, k, M, desde_n=0, hasta_n=None):
    if hasta_n is not None:
        total = 0
        for n in range(desde_n, hasta_n + 1):
            total += calcular_probabilidad_n_clientes(lam, mu, k, M, n)
        return total
    else:
        # Suma desde_n hasta M
        if desde_n == 0:
            return 1.0
        acumulado_hasta_desde_n_menos_1 = 0
        for n in range(0, desde_n):
            acumulado_hasta_desde_n_menos_1 += calcular_probabilidad_n_clientes(lam, mu, k, M, n)
        return 1 - acumulado_hasta_desde_n_menos_1

'''12.
Calcula costos por hora 
'''
def calcular_costos_hora(lam, mu, k, M, cte=0, cts=0, ctse=0, cs=0):

    Lq = calcular_numero_esperado_clientes_cola(lam, mu, k, M)
    L = calcular_numero_esperado_clientes_sistema(lam, mu, k, M)
    Ls = L - Lq  # Clientes en servicio

    costo_cola = cte * Lq
    costo_sistema = cts * L
    costo_servicio = ctse * Ls
    costo_servidor = cs * k  # k servidores

    costo_total = costo_cola + costo_sistema + costo_servicio + costo_servidor

    return {
        "costo_tiempo_cola": costo_cola,
        "costo_tiempo_sistema": costo_sistema,
        "costo_tiempo_servicio": costo_servicio,
        "costo_servidor": costo_servidor,
        "costo_total_por_hora": costo_total
    }

'''13.
Calcula costos por dia
'''
def calcular_costos_diarios(lam, mu, k, M, cte, cts, ctse, cs, horas_laborables):

    costos_hora = calcular_costos_hora(lam, mu, k, M, cte, cts, ctse, cs)
    costo_total_diario = costos_hora["costo_total_por_hora"] * horas_laborables

    return {
        "costo_diario_tiempo_cola": costos_hora["costo_tiempo_cola"] * horas_laborables,
        "costo_diario_tiempo_sistema": costos_hora["costo_tiempo_sistema"] * horas_laborables,
        "costo_diario_tiempo_servicio": costos_hora["costo_tiempo_servicio"] * horas_laborables,
        "costo_diario_servidor": costos_hora["costo_servidor"] * horas_laborables,
        "costo_diario_total": costo_total_diario
    }