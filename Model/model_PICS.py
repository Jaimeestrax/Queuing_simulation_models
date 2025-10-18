''' 1. 
Probabilidad de hallar el sistema ocupado
Probabilidad que tienen los usuarios de esperar para ser atendidos
'''
def calcular_utilizacion_sistema(lam, mu):
    # Se calcula usando ρ = λ / μ
    p = lam / mu
    if p >= 1 or p <= 0:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    return p

''' 2. 
Probabilidad de hallar el sistema vacío u ocioso
Probabilidad que tienen los usuarios de no esperar o ser atendidos sin esperar en cola
'''
def calcular_probabilidad_sistema_vacio(lam, mu):
    # P0 = 1 - λ/μ
    p0 = 1 - calcular_utilizacion_sistema(lam, mu)
    return p0

''' 3.
Probabilidad de hallar exactamente n clientes dentro del sistema
'''
def calcular_probabilidad_n_clientes(lam, mu, n):
    # Se calcula: Pn = P0 * (λ/μ)^n
    p = calcular_utilizacion_sistema(lam, mu)  # devuelve lam/mu
    p0 = calcular_probabilidad_sistema_vacio(lam, mu)
    pn = p0 * (p ** n)
    return pn

''' 4.
Probabilidad acumulada desde_n hasta_n clientes
'''
def calcular_probabilidad_acumulada(lam, mu, desde_n = 0, hasta_n = None):
    # P = 1 - sum(P0 a P_{desde_n-1})
    p = calcular_utilizacion_sistema(lam, mu)

    if hasta_n is not None:
        # Suma desde_n hasta_n cliente
        total = 0
        for n in range(desde_n, hasta_n + 1):
            total += calcular_probabilidad_n_clientes(lam, mu, n)
        return total
    else:
        # Suma desde_n hasta infinito
        if desde_n == 0:
            return 1.0 # Por definición la sumatoria es 1
        acumulado = 0
        for n in range(0, desde_n):
            acumulado += calcular_probabilidad_n_clientes(lam, mu, n)
        return 1 - acumulado

''' 5.
Número esperado de clientes en el sistema (promedio de clientes)
'''
def calcular_numero_esperado_clientes_sistema(lam, mu):
    # L = λ / (μ - λ)
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    l = lam / (mu - lam)
    return l

'''6.
Número esperado de clientes en la cola (promedio clientes que permanecen en cola)
'''
def calcular_numero_esperado_clientes_cola(lam, mu):
    # Lq = λ^2 / (μ * (μ - λ))
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    lq = (lam ** 2) / (mu * (mu - lam))
    return lq

'''7.
Número esperado de clientes en la cola no vacía (excluye momentos donde la cola estaba vacía)
'''
def calcular_numero_esperado_clientes_cola_no_vacia(lam, mu):
    # Ln = λ / (μ - λ)
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    ln = lam / (mu - lam)
    return ln

'''8.
Tiempo esperado en el sistema (promedio que se esperaria que los clientes permanezcan en el sistema desde que llegan hasta que salgan)
'''
def calcular_tiempo_esperado_sistema(lam, mu):
    # W = 1 / (μ - λ)
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    w = 1 / (mu - lam)
    return w

'''9.
Tiempo esperado en cola (promedio tiempo espera de los clientes)
'''
def calcular_tiempo_esperado_cola(lam, mu):
    # Wq = λ / (μ * (μ - λ))
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    wq = lam / (mu * (mu - lam))
    return wq

'''10.
Tiempo esperado en cola para colas no vacías (solo momentos cuando en verdad les toco esperar a los clientes)
'''
def calcular_tiempo_esperado_cola_no_vacia(lam, mu):
    # Wn = 1 / (μ - λ)
    if lam >= mu:
        raise ValueError("El sistema no cumple la condición de estabilidad ya que λ >= μ")
    wn = 1 / (mu - lam)
    return wn

'''11.
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

'''12.
Calculo de los costos diarios
'''
def calcular_costos_diarios(lam, mu, cte, cts, ctse, cs, hora_laborable):
    # lam y mu debe estar en cliente/hora

    w = calcular_tiempo_esperado_sistema(lam, mu)
    wq = calcular_tiempo_esperado_cola(lam, mu)

    ctte = lam * hora_laborable * wq * cte
    ctts = lam * hora_laborable * w * cts
    cttse = lam * hora_laborable * (1 / mu) * ctse
    ctservidor = cs * hora_laborable
    # sumatoria de todos los costos por hora
    costo_total_diario = ctte + ctts + cttse + cts

    return {
        "costo_diario_tiempo_cola": ctte,
        "costo_diario_tiempo_sistema": ctts,
        "costo_diario_tiempo_servicio": cttse,
        "costo_diario_servidor": ctservidor,
        "costo_diario_total": costo_total_diario
    }