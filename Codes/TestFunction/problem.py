import math

def calcular_fo_sum_square(lista_variaveis):

    # -- Calcular a função objetivo: sum(Xi^2)
    custo = 0
    for valor in lista_variaveis:
        custo += valor ** 2

    return custo

def avaliar_populacao(populacao_inicial):

    populacao = []
    melhor_custo = math.inf
    melhor_individuo = []

    for individuo in populacao_inicial:
        custo = calcular_fo_sum_square(individuo)
        populacao.append((individuo, custo))

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_individuo = individuo.copy()

    
    return populacao, melhor_custo, melhor_individuo

def valida_min_max(valor, min, max):
    if ( valor < min ):
        valor = min

    if ( valor > max ):
        valor = max    
    
    return valor
