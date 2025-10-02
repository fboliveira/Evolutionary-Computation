def calcular_fo_sum_square(lista_variaveis):

    # -- Calcular a função objetivo: sum(Xi^2)
    custo = 0
    for valor in lista_variaveis:
        custo += valor ** 2

    return custo

def avaliar_populacao(populacao):

    for item in populacao:
        individuo = item[0]
        item[1] = calcular_fo_sum_square(individuo)
