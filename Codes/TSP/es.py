import time
import tsp
import local_search
import ga as ag

class Individual:

    def __init__(self, candidate, fs):
        self.candidate = candidate
        self.fs = fs

    def print(self):
        print(f"{self.fs}")

def ES(d, params):

    mu = 10
    n_lambda = 5 * mu # (10, 50)-ES
    mutation_rate = 0.8
    generation_max = 10
    strategy = 1 # 1 - (mu+lambda) / 2 - (mu, lambda)
    
    # VND
    max_k = 2 

    t_init = time.time()
    chart_data = []

    population = [] # 2
    ind_star = Individual([], float("inf")) #3 e #4

    # candidate, fs, _ = tsp.greedy_build(d)
    # individual = Individual(candpopulationidate, fs)
    # population.append(individual)

    # Generate initial population - size: mu
    for _ in range(mu - len(population)):
        candidate, fs = ag.random_solution(d) # 7

        # candidate, fs, _ = local_search.vnd_first_improvement(d, candidate, fs, max_k)

        individual = Individual(candidate, fs)
        population.append(individual)

    # Order: best to worst
    population.sort(key = lambda i: i.fs)

    index_best = 0 # It is the first
    ind_star = Individual(population[index_best].candidate[:], population[index_best].fs)    

    for g in range(1, generation_max + 1):

        descendents = [] # 12

        # For each individual
        for i in range(mu):
            
            # Generate lambda / mu descendents
            for j in range(int(n_lambda / mu)):
                # --- Reproduction
                # Perfom copy
                child = population[i].candidate[:]

                # Perform Mutation
                ag.mutation_swap(child, mutation_rate)

                fs = tsp.full_eval(d, child)
                # child_one, fs, _ = local_search.vnd_first_improvement(d, child_one, fs, max_k)

                descendents.append(Individual(child[:], fs))
                
                if fs < ind_star.fs + local_search.EPS:
                    ind_star = Individual(child[:], fs)

            # ---
        # ---

        # -- Define survivors:        
        if strategy == 1: # mu + lambda
            # Merge: current population and descendents        
            population = population + descendents
        else: # mu, lambda
            population = descendents

        # Sort population
        population.sort(key = lambda i: i.fs)        
        
        # Remove individuals - shrink to mu
        del population[mu:len(population)]

        # # ---
        # index_best = 0 # It is the first, I hope :)
        # if population[index_best].fs < ind_star.fs + local_search.EPS:
        #     ind_star = Individual(population[index_best].candidate[:], population[index_best].fs)

        # Print generations
        print(f"{g}\t{ind_star.fs}\t{population[index_best].fs}")

        # ---

    # for individual in population:
    #     individual.print() 

    return ind_star.candidate, ind_star.fs, time.time() - t_init, chart_data