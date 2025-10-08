def calcular_fo_sum_square(lista_variaveis):

    # -- Calcular a função objetivo: sum(Xi^2)
    custo = 0
    for valor in lista_variaveis:
        custo += valor ** 2

    return custo

def avaliar_populacao(populacao_inicial):

    populacao = []

    for individuo in populacao_inicial:
        custo = calcular_fo_sum_square(individuo)
        populacao.append((individuo, custo))
    
    return populacao
