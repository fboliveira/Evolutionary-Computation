import random

# Parâmetros do problema
min = -100
max = 100
D = 100

# Parâmetros do GA
tam_pop = 100
crossover = 0.80 # operador principal
mutacao = 0.1 # operador secundário
geracoes = 200

# Cromossomos - quantidade de variaveis
tamanho_cromossomos = D

def calcular_fo(individuo):

    # -- Calcular a função objetivo: sum(Xi^2)
    custo = 0
    for valor in individuo:
        custo += valor ** 2

    return custo

def valida_min_max(valor):
    if ( valor < min ):
        valor = min

    if ( valor > max ):
        valor = max    
    
    return valor

populacao = []
custos_fo = []

# Geração da população inicial
# range: [start, stop[
# start < stop
for i in range(tam_pop):

    individuo = []
    for c in range(tamanho_cromossomos):
        valor = random.uniform(min, max)
        individuo.append(valor)

    # print(individuo)
    # Avaliar o indivíduo
    custo = calcular_fo(individuo)
    populacao.append((individuo, custo))

# print(populacao)
# item: ([ individuo ], [ custo_individuo ])

pressao_seletiva = 1.2

# Iterar sobre as gerações - critério de parada: número máximo de gerações
for g in range(geracoes):

    # Classificar a população - ranking linear
    populacao.sort(key = lambda item : item[1], reverse=True)

    melhor_custo_ate_agora = populacao[tam_pop - 1][1]
    print(f'Geração: {g} - Melhor custo até agora: { melhor_custo_ate_agora}')

    fitness = []
    soma_fitness = 0.0

    for i in range(1, tam_pop + 1):
        fitness_individuo = 2 - pressao_seletiva + 2 * ( pressao_seletiva - 1 ) * ( (i - 1) / (tam_pop - 1) )
        # print(fitness_individuo)
        soma_fitness += fitness_individuo
        fitness.append(fitness_individuo)

    descendentes = []    
    reproducao = round(crossover * tam_pop)

    # Seleção por roleta - critério: fitness
    proporcao_fitness = []
    proporcao = 0.0
    for f in fitness:
        proporcao += f / soma_fitness
        proporcao_fitness.append(proporcao)

    # Processo de reprodução
    for r in range(reproducao):
        # Selecionar os progenitores
        # Return the next random floating-point number in the range 0.0 <= X < 1.0
        prob_individuo1 = random.random()

        indice_individuo1 = 0
        for i, p in enumerate(proporcao_fitness):
            if (prob_individuo1 <= p):
                indice_individuo1 = i
                break
        
        prob_individuo2 = random.random()

        indice_individuo2 = 0
        for i, p in enumerate(proporcao_fitness):
            if (prob_individuo2 <= p):
                indice_individuo2 = i
                break

        progenitor1 = populacao[indice_individuo1][0]
        progenitor2 = populacao[indice_individuo2][0]

        # Operações de reprodução
        # - Crossover       
        alpha = random.random()
        
        # D1 = alpha * P1 + (1 - alpha) * P2
        descendente1 = []
        # D2 = alpha * P2> + (1 - alpha) * P1
        descendente2 = []

        # [3.5 2.8 4.9]
        # [5.8 4.2 3.7]
        for i in range(tamanho_cromossomos):
            v1 = alpha * progenitor1[i] + (1 - alpha) * progenitor2[i]
            v2 = alpha * progenitor2[i] + (1 - alpha) * progenitor1[i]

            descendente1.append( valida_min_max(v1) )
            descendente2.append( valida_min_max(v2) )

        # - Mutação
        # -- Uma possível mutação de uma variável apenas no descendente
        r_mutacao = random.random()
        if (r_mutacao <= mutacao):
            ponto_de_mutacao = random.randint(0, tamanho_cromossomos - 1)
            gama = random.random()

            valor = descendente1[ponto_de_mutacao] * gama
            descendente1[ponto_de_mutacao] = valida_min_max(valor)


        # -- Avaliar a possibilidade de mutação em cada uma das variáveis
        for i in range(tamanho_cromossomos):            
            r_mutacao = random.random()
            ponto_de_mutacao = i
            if (r_mutacao <= mutacao):            
                gama = random.random()

                valor = descendente2[ponto_de_mutacao] * gama
                descendente2[ponto_de_mutacao] = valida_min_max(valor)

        custo_descendente1 = calcular_fo(descendente1)
        custo_descendente2 = calcular_fo(descendente2)

        # Avaliar os descendentes
        descendentes.append((descendente1, custo_descendente1))
        descendentes.append((descendente2, custo_descendente2))

    # União das duas populações: atual (progenitores) + descendentes
    nova_populacao = populacao + descendentes
    
    # Classificar progenitores e descendentes
    # Ordenando de maneira ascendente pela função de custo
    nova_populacao.sort(key=lambda item : item[1])
       
    # Definir a população sobrevivente    
    # - Seleção dos n primeiros melhores (Elitismo: 100%)
    populacao = nova_populacao[0:tam_pop]
    # Outras possibilidades para definir a população sobrevivente:
    # - Fitness e roleta
    # - Torneio: progenitores e descendentes
    # - Parte com Elitismo (5%), parte roleta (ranking, 75%), parte aleatória (20%) 

# Imprimir o melhor resultado:
melhor = populacao[0]
melhor_individuo = melhor[0]
melhor_custo = melhor[1]

print(f'Melhor custo final: {melhor_custo}')
print(f'Melhor Indivíduo: {melhor_individuo}')
