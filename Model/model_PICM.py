import math

''' 1. 
Probabilidad de hallar el sistema completamente vacío
Probabilidad de que todos los servidores estén desocupados u ociosos a la vez
'''
def calcular_probabilidad_sistema_vacio(lam, mu, k):
    # Fórmula: P0 = 1 / [ Σ_{n=0}^{n=k-1} (ρ^n / n!) + (ρ^k / k!) * (kμ / (kμ - λ)) ] -> Donde ρ = λ / μ
    
    p = lam / mu

    if p < k or k <= 0:
        raise ValueError("El sistema no cumple la condición de estabilidad")

    # Sumatoria desde n=0 hasta n=k-1
    suma = 0
    for n in range(k):
        suma += (p ** n) / math.factorial(n)

    # Término adicional para n >= k
    termino_k = (p ** k) / math.factorial(k)
    denominador = k * mu - lam
    if denominador <= 0:
        raise ValueError("El sistema es inestable ya que λ >= k*μ")
    termino_adicional = termino_k * (k * mu / denominador)

    # Calculo completo de la formula
    p0 = 1 / (suma + termino_adicional)
    return p0

''' 2. 
Probabilidad de que un usuario que llega tenga que esperar
Probabilidad de que haya k o más usuarios en el sistema
'''
def calcular_probabilidad_k_clientes(lam, mu, k):
    # Fórmula: [((λ/μ)^k / k!) * (kμ/kμ-λ) * P0]
    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, k)

    if k * mu <= lam:
        raise ValueError("El sistema es inestable ya que λ >= k*μ")

    pk = (1 / math.factorial(k)) * (p ** k) * (k * mu / (k * mu - lam)) * p0
    return pk

''' 3.
Probabilidad de que un usuario que llega no tenga que esperar
'''
def calcular_probabilidad_no_esperar(lam, mu, k):
    # Fórmula: 1 - Pk
    pk = calcular_probabilidad_k_clientes(lam, mu, k)
    p_ne = 1 - pk
    return p_ne

''' 4.
Probabilidad de hallar exactamente n clientes dentro del sistema
'''
def calcular_probabilidad_n_clientes(lam, mu, k, n):
    """
    Fórmula:
    Pn = 
        P0 * (λ/μ)^n / n!       si n < k
        P0 * (λ/μ)^n / (k! * k^(n-k))   si n >= k
    """
    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, k)

    if n < k:
        pn = p0 * (p ** n) / math.factorial(n)
    else:  # n >= k
        pn = p0 * (p ** n) / (math.factorial(k) * (k ** (n - k)))

    return pn

'''5.
Número esperado de clientes en la cola (promedio clientes que permanecen en cola)
'''
def calcular_numero_esperado_clientes_cola(lam, mu, k):
    # Fórmula: Lq = [λ * μ * (λ/μ)^k * P0] / [(k-1)! * (kμ - λ)^2]
    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, k)

    if k * mu <= lam:
        raise ValueError("El sistema es inestable ya que λ >= k*μ")

    numerador = lam * mu * (p ** k) * p0
    denominador = math.factorial(k - 1) * ((k * mu - lam) ** 2)
    lq = numerador / denominador
    return lq

''' 6.
Número esperado de clientes en el sistema (promedio de clientes)
'''
def calcular_numero_esperado_clientes_sistema(lam, mu, k):
    # Fórmula: L = Lq + λ/μ
    lq = calcular_numero_esperado_clientes_cola(lam, mu, k)
    l = lq + (lam / mu)
    return l

'''7.
Número esperado de clientes en la cola no vacía (excluye momentos donde la cola estaba vacía)
'''
def calcular_numero_esperado_clientes_cola_no_vacia(lam, mu, k):
    # Fórmula: Ln = Lq / Pk
    lq = calcular_numero_esperado_clientes_cola(lam, mu, k)
    pk = calcular_probabilidad_k_clientes(lam, mu, k)
    if pk == 0:
        raise ValueError("Pk es 0 y no se puede dividir por cero")
    ln = lq / pk
    return ln

'''8.
Tiempo esperado en cola (promedio tiempo espera de los clientes)
'''
def calcular_tiempo_esperado_cola(lam, mu, k):
    # Fórmula: Wq = [μ * (λ/μ)^k * P0] / [(k-1)! * (kμ - λ)^2]
    p = lam / mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu, k)

    numerador = mu * (p ** k) * p0
    denominador = math.factorial(k - 1) * ((k * mu - lam) ** 2)
    wq = numerador / denominador
    return wq

'''9.
Tiempo esperado en el sistema (promedio que se esperaria que los clientes permanezcan en el sistema desde que llegan hasta que salgan)
'''
def calcular_tiempo_esperado_sistema(lam, mu, k):
    # Fórmula: W = Wq + 1/μ
    wq = calcular_tiempo_esperado_cola(lam, mu, k)
    w = wq + (1 / mu)
    return w

'''10.
Tiempo esperado en cola para colas no vacías (solo momentos cuando en verdad les toco esperar a los clientes)
'''
def calcular_tiempo_esperado_cola_no_vacia(lam, mu, k):
    # Fórmula: Wn = Wq / Pk
    wq = calcular_tiempo_esperado_cola(lam, mu, k)
    pk = calcular_probabilidad_k_clientes(lam, mu, k)
    if pk == 0:
        raise ValueError("Pk es 0 y no se puede dividir por cero")
    wn = wq / pk
    return wn

'''11.
Tiempo de utilización del sistema
'''
def calcular_utilizacion_sistema(lam, mu, k):
    # Fórmula: ρ = λ / (k * μ)
    p = lam / (k * mu)
    if p >= 1:
        raise ValueError("El sistema no cumple la condición de estabilidad")
    return p

'''12.
Probabilidad acumulada desde_n hasta_n clientes
'''
def calcular_probabilidad_acumulada(lam, mu, k, desde_n=0, hasta_n=None):
    if hasta_n is not None:
        total = 0
        for n in range(desde_n, hasta_n + 1):
            total += calcular_probabilidad_n_clientes(lam, mu, k, n)
        return total
    else:
        # Suma desde_n hasta infinito
        if desde_n == 0:
            return 1.0
        acumulado_hasta_desde_n_menos_1 = 0
        for n in range(0, desde_n):
            acumulado_hasta_desde_n_menos_1 += calcular_probabilidad_n_clientes(lam, mu, k, n)
        return 1 - acumulado_hasta_desde_n_menos_1

'''13.
Calculo de los costos por hora
'''
def calcular_costos_hora(lam, mu, cte = 0, cts = 0, ctse = 0, cs = 0):
    # sumatoria de todos los costos por hora
    costo_total_por_hora = cte + cts + ctse + cs

    # dados en dolares por hora
    return {
        "costo_tiempo_cola": cte,
        "costo_tiempo_sistema": cts,
        "costo_tiempo_servicio": ctse,
        "costo_servidor": cs,
        "costo_total_por_hora": costo_total_por_hora
    }

'''14.
Calculo de los costos diarios
'''
def calcular_costos_diarios(lam, mu, k, cte, cts, ctse, cs, hora_laborable):
    # lam y mu debe estar en cliente/hora

    w = calcular_tiempo_esperado_sistema(lam, mu)
    wq = calcular_tiempo_esperado_cola(lam, mu)

    ctte = lam * hora_laborable * wq * cte
    ctts = lam * hora_laborable * w * cts
    cttse = lam * hora_laborable * (1 / mu) * ctse
    ctservidor = k * cs * hora_laborable
    # sumatoria de todos los costos por dia
    costo_total_diario = ctte + ctts + cttse + cts

    return {
        "costo_diario_tiempo_cola": ctte,
        "costo_diario_tiempo_sistema": ctts,
        "costo_diario_tiempo_servicio": cttse,
        "costo_diario_servidor": ctservidor,
        "costo_diario_total": costo_total_diario
    }