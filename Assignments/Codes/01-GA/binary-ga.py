import random

# Parâmetros do problema
min = -100
max = 100
D = 5

# Parâmetros do GA
tam_pop = 5
crossover = 0.80
mutacao = 0.05
geracoes = 100

# Representação binária
precisao = 5

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

    print(individuo)
    populacao.append(individuo)

# Avaliar a população inicial:
for ind in populacao:
    custo = calcular_fo(ind)    
    custos_fo.append(custo)
    print(custo)

# Classificar a população - ranking linear

# Iterar sobre as gerações - critério de parada: número máximo de gerações
for g in range(geracoes):

    # Selecionar os progenitores
    # Operações de reprodução
    # - Crossover
    # - Mutação
    # Avaliar os descendentes
    # Classificar progenitores e descendentes
    # Definir a população sobrevivente
    pass

# Imprimir o melhor resultado:
