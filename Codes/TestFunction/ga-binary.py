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

# Representação binária
precisao = 30

# Cromossomo - quantidade de variaveis * precisao
tamanho_cromossomo = D * precisao

def calcular_fo(individuo):

    # Decodificar de binário para inteiro
    lista_de_inteiros = []

    # Para cada variavel:
    for i in range(D):
        # Para cada bit na precisão
        valor_inteiro = 0
        for b in range(precisao):
            # 2^indice
            #  6543210 6543210 
            # i = 2 * 
            # [0101010 0010101 0010101 0010101 0010101]
            #          b
            valor_inteiro += pow(2, precisao - 1 - b) * individuo[ i * precisao + b ]

        lista_de_inteiros.append(valor_inteiro)
        
    # Transformar de inteiro para real
    real = []
    for inteiro in lista_de_inteiros:
        valor_real = ( inteiro * (( max - min ) / ( pow(2, precisao) - 1 )) ) + min
        real.append(valor_real)

    # -- Calcular a função objetivo: sum(Xi^2)
    custo = 0
    for valor in real:
        custo += valor ** 2

    return custo

populacao = []
custos_fo = []

# Geração da população inicial
# range: [start, stop[
# start < stop
for i in range(tam_pop):

    individuo = []
    # for d in range(D):
    #     for p in range(precisao):
    for c in range(tamanho_cromossomo):
        bit = random.randint(0, 1)
        individuo.append(bit)

    # print(individuo)
    # Avaliar o indivíduo
    custo = calcular_fo(individuo)
    populacao.append((individuo, custo))

# # Avaliar a população inicial:
# for ind in populacao:
#     custo = calcular_fo(ind)    
#     custos_fo.append(custo)
#     print(custo)

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
        # [ 14.4; 49.2; 5.5; 30.9 ]
        # [ 14.4; 63.6; 69.1; 100 ]
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
        ponto_de_corte = random.randint(0, tamanho_cromossomo - 1)
        # D1 = P1_1 + P2_2
        descendente1 = progenitor1[0:ponto_de_corte] + progenitor2[ponto_de_corte:len(progenitor2)]
        # D2 = P2_1 + P1_2
        descendente2 = progenitor2[0:ponto_de_corte] + progenitor1[ponto_de_corte:len(progenitor1)]

        # - Mutação
        # -- Uma possível mutação de um bit apenas no descendente
        # [01001 1 0100]
        r_mutacao = random.random()
        if (r_mutacao <= mutacao):
            ponto_de_mutacao = random.randint(0, tamanho_cromossomo - 1)
            if ( descendente1[ponto_de_mutacao] == 1 ):
                descendente1[ponto_de_mutacao] = 0
            else:
                descendente1[ponto_de_mutacao] = 1

        # -- Avaliar a possibilidade de mutação em cada um dos bit
        # [1101100100]
        for i in range(tamanho_cromossomo):            
            r_mutacao = random.random()
            ponto_de_mutacao = i
            if (r_mutacao <= mutacao):
                
                if ( descendente2[ponto_de_mutacao] == 1 ):
                    descendente2[ponto_de_mutacao] = 0
                else:
                    descendente2[ponto_de_mutacao] = 1

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
