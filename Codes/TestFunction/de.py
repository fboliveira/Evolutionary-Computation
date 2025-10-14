import random
import problem

def criar_populacao_inicial(Np, D, min, max):

    populacao = []

    for _ in range(Np):

        individuo = []

        for _ in range(D):
            valor = random.random() * (max - min) + min
            individuo.append(valor)

        populacao.append(individuo)

    return populacao

def selecionar_indices(Np, target):

    r0 = target
    r1 = target
    r2 = target

    while True:
        r0 = random.randint(0, Np - 1)

        if r0 != target:
            break

    while True:
        r1 = random.randint(0, Np - 1)

        if r1 != r0 and r1 != target:
            break

    while True:
        r2 = random.randint(0, Np - 1)

        if r2 != r1 and r2 != r0 and r2 != target:
            break

    return r0, r1, r2

def mutacao(F, min, max, xr0, xr1, xr2):

    mutante = []
    
    for i in range(len(xr1)):
        # Gerar perturbação - diferença
        diferenca = xr1[i] - xr2[i]
        
        # Mutação
        valor = xr0[i] + F * diferenca

        valor = reparar_valor(valor, min, max)
        mutante.append(valor)

    return mutante

def reparar_valor(valor, min, max):
    if valor < min:
        valor = min
    elif valor > max:
        valor = max

    return valor

def crossover(D, Cr, mutante, target):

    jrand = random.randint(0, D - 1)

    trial = []

    for i in range(D):
        if random.random() <= Cr or i == jrand:
            trial.append(mutante[i])
        else:
            trial.append(target[i])

    return trial

if __name__ == '__main__':

    # Parâmetros do problema
    min = -100
    max = 100
    D = 100

    # Criterio de parada
    gmax = 1000
    # Tamanho da população
    Np = 100
    # Coeficiente de mutação
    F = 0.4
    # Coeficiente de Crossover
    Cr = 0.7

    # Criação da população inicial - X
    populacao_inicial = criar_populacao_inicial(Np, D, min, max)

    # Avaliar a população inicial
    populacao, _, _ = problem.avaliar_populacao(populacao_inicial)

    # Enquanto o critério de parada não for atingido
    for g in range(gmax):

        nova_populacao = []

        # Para cada vetor da população
        for i in range(Np):

            # Target -> i
            # DE/rand/1/bin
            target = populacao[i][0]
            custo_target = populacao[i][1]

            # Selecionar r0, r1, r2
            r0, r1, r2 = selecionar_indices(Np, i)

            xr0 = populacao[r0][0]
            xr1 = populacao[r1][0]
            xr2 = populacao[r2][0]

            # Mutante
            mutante = mutacao(F, min, max, xr0, xr1, xr2)

            # Crossover
            # u0
            trial = crossover(D, Cr, mutante, target)
            custo_trial = problem.calcular_fo_sum_square(trial)

            # Selecao
            if (custo_trial <= custo_target):
                nova_populacao.append((trial, custo_trial))
            else:
                nova_populacao.append((target.copy(), custo_target))

        # População para a geração seguinte
        populacao = nova_populacao[:]
        populacao.sort(key=lambda item : item[1])

        melhor_custo_ate_agora = populacao[0][1]
        print(f'Geração: {g} - Melhor custo até agora: { melhor_custo_ate_agora}')


    # Imprimir o melhor resultado:
    melhor = populacao[0]
    melhor_individuo = melhor[0]
    melhor_custo = melhor[1]

    print(f'Melhor Indivíduo: {melhor_individuo}')
    print(f'Melhor custo final: {melhor_custo}')
