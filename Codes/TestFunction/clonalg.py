import math
import random
import problem

def criar_anticorpo(L):
    anticorpo = []
    for _ in range(L):
        bit = random.randint(0, 1)
        anticorpo.append(bit)

    return anticorpo

# Geração da população inicial Ab
def criar_populacao_inicial(N, L):

    populacaoAb = []

    for _ in range(N):
        anticorpo = criar_anticorpo(L)
        populacaoAb.append(anticorpo)

    return populacaoAb

def decodifica(Ab, D, precisao):

    populacaoAb_real = []

    for anticorpo in Ab:

        # Decodificar de binário para inteiro
        lista_de_inteiros = []

        # Para cada variavel:
        for i in range(D):
            # Para cada bit na precisão
            valor_inteiro = 0
            for b in range(precisao):
                valor_inteiro += pow(2, precisao - 1 - b) * anticorpo[ i * precisao + b ]

            lista_de_inteiros.append(valor_inteiro)
            
        # Transformar de inteiro para real
        real = []
        for inteiro in lista_de_inteiros:
            valor_real = ( inteiro * (( max - min ) / ( pow(2, precisao) - 1 )) ) + min
            real.append(valor_real)

        populacaoAb_real.append(real)

    return populacaoAb_real

def calcular_custo(Ab, N, D, precisao):

    populacaoAb_real = decodifica(Ab, D, precisao)

    # Avaliar a população inicial
    populacaoAb_custo, _, _ = problem.avaliar_populacao(populacaoAb_real)

    populacaoAb = []

    for i in range(N):
        populacaoAb.append((Ab[i].copy(), populacaoAb_custo[i][1]))

    # Ordenando de maneira ascendente pela função de custo
    populacaoAb.sort(key=lambda item : item[1])

    return populacaoAb

def select(Ab, n):
    return Ab[0:n]

def clona(Abn, N, beta):

    clones_anticorpos = []

    i = 1

    for anticorpo in Abn:

        nc = math.ceil((beta * N) / i)
        i = i + 1

        for _ in range(nc):
            clones_anticorpos.append(anticorpo[0][:])

    return clones_anticorpos

def hypermut(clones, L, tm):

    for anticorpo in clones:

        for i in range(L):            
            r_mutacao = random.random()
            ponto_de_mutacao = i #bit corrente
            if r_mutacao <= tm:
                
                if anticorpo[ponto_de_mutacao] == 1:
                    anticorpo[ponto_de_mutacao] = 0
                else:
                    anticorpo[ponto_de_mutacao] = 1

    return clones

def insere(Ab, Abn, N):
    Ab = Ab + Abn
    Ab.sort(key=lambda item : item[1])
    return Ab[0:N]

def gera(d, L):

    Abd = []

    for _ in range(d):
        Abd.append(criar_anticorpo(L))

    return Abd

def replace(Ab, Abd, N, d):
    del Ab[N-d:N]
    return Ab + Abd

if __name__ == '__main__':

    # Parâmetros do problema
    min = -100
    max = 100
    D = 100

    # Representação binária
    precisao = 30

    # Comprimento dos anticorpos
    L = precisao * D

    # Tamanho da Ab composta por N anticorpos
    N = 100

    # Quantidade de gerações - critério de parada
    gen = 100

    # Número n de anticorpos a serem selecionados para clonagem
    n = 20

    # Fator multiplicativo beta usado na definição da quantidade de clones;
    beta = 0.3
    
    # Quantidade d de anticorpos com baixa afinidade que serão substituı́dos.
    d = 10

    # Taxa de mutação - hyperm
    tm = 0.7

    populacaoAb_inicial = criar_populacao_inicial(N, L)
    
    # Decodifica e calcula fitness
    populacaoAb = calcular_custo(populacaoAb_inicial, N, D, precisao)

    # Enquanto o critério de parada não for atingido
    for g in range(gen):

        Abn = select(populacaoAb, n)
        clones = clona(Abn, N, beta)
        clones_mut = hypermut(clones, L, tm)

        Ab_clones = calcular_custo(clones_mut, len(clones_mut), D, precisao)

        Ab = select(Ab_clones, n)
        Ab = insere(Ab, Abn, N)

        Abd = gera(d, L)

        populacaoAb = replace(Ab, Abd, N, d)

        melhor = populacaoAb[0]
        melhor_custo = melhor[1]
        print(f'Geracao: {g} \tMelhor custo: {melhor_custo}')

    # Imprimir o melhor resultado - memória:
    melhor = populacaoAb[0]
    melhor_individuo = melhor[0]
    melhor_custo = melhor[1]

    print(f'Melhor Indivíduo: {melhor_individuo}')
    print(f'Melhor custo final: {melhor_custo}')
