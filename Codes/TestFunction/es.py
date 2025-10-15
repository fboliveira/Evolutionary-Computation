import random
import problem

def criar_populacao_inicial(mu, D, min, max):

    populacao = []

    for _ in range(mu):

        individuo = []

        for _ in range(D):
            valor = random.random() * (max - min) + min
            individuo.append(valor)

        populacao.append(individuo)

    return populacao

def copia_com_mutacao(individuo, taxaMutacao, min, max):

    individuo_copia = []

    for valor in individuo:
        
        if random.random() <= taxaMutacao:
            valor *= random.random()
            valor = problem.valida_min_max(valor, min, max)

        individuo_copia.append(valor)

    return individuo_copia

def selecionar_melhores(mu : int, populacao : list, descendentes : list, estrategia):

    if estrategia == 1: # mu+lambda
        descendentes = populacao + descendentes

    descendentes.sort(key=lambda item : item[1])
    del descendentes[mu:] # [0, mu-1]

    return descendentes

if __name__ == '__main__':

    # Parâmetros do problema
    min = -100
    max = 100
    D = 100

    # Tamanho da população
    mu = 1
    # Total de descentes
    esLambda = 1
    # Número máximo de gerações
    genMax = 100
    # Taxa de Mutação
    taxaMutacao = 0.7
    # Estrategia de seleção: 1 para mu+lambda; 2 para mu, lambda
    estrategiaSelecao = 1

    # Criação da população inicial de tamanho mu
    populacao_inicial = criar_populacao_inicial(mu, D, min, max)

    # Avaliar a população inicial - P
    populacao, melhor_custo, melhor_individuo = problem.avaliar_populacao(populacao_inicial)

    print(f'População inicial - Melhor custo até agora: { melhor_custo }')

    # Enquanto o critério de parada não for atingido
    for g in range(genMax):

        # Conjunto dos descendentes
        descendentes = []

        # Para cada indíviduo na população P
        for i in range(mu):
            # Gerar lambda / mu descendentes
            num_descendentes_por_individuo = round(esLambda / mu)
            for j in range(num_descendentes_por_individuo):
                descendente = copia_com_mutacao(populacao[i][0], taxaMutacao, min, max)
                custo_descendente = problem.calcular_fo_sum_square(descendente)
                descendentes.append((descendente, custo_descendente))   

                if custo_descendente < melhor_custo:
                    melhor_custo = custo_descendente
                    melhor_individuo = descendente.copy()
        
        # Selecionar os melhores indivíduos conforme a estratégia
        populacao = selecionar_melhores(mu, populacao, descendentes, estrategiaSelecao)
        print(f'Geração: {g} - Melhor custo até agora: { melhor_custo }')

    # Imprimir o melhor resultado:
    print(f'\nMelhor Indivíduo: {melhor_individuo}\n')
    print(f'Melhor custo final: {melhor_custo}')        

