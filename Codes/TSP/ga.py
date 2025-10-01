import time
import random
import tsp
import local_search
import copy

class Individual:

    def __init__(self, candidate, fs):
        self.candidate = candidate
        self.fs = fs
        self.fitness = 0.0
        self.probability = 0.0

    def print(self):
        print(f"{self.fs}")

def genetic_algorithm(d, params):

    pop_size = 10
    mutation_rate = 0.05
    crossover_rate = 0.8
    generation_max = 10
    local_search_rate = 0.0
    
    # Fitness - linear ranking
    selective_pressure = 1.2

    # VND
    max_k = 2 

    t_init = time.time()
    chart_data = []

    population = []
    ind_star = Individual([], float("inf"))

    candidate, fs, _ = tsp.greedy_build(d)
    individual = Individual(candidate, fs)
    population.append(individual)

    # Partial greedy - alpha

    # Generate initial population - size: pop_size
    for _ in range(pop_size - len(population)):
        candidate, fs = random_solution(d)

        if random.random() <= local_search_rate:
            candidate, fs, _ = local_search.vnd_first_improvement(d, candidate, fs, max_k)

        individual = Individual(candidate, fs)
        population.append(individual)

    # Sort population using FS - this will be changed by fitness
    # population.sort(reverse = True, key = lambda i: i.fs)
    linear_ranking(population, selective_pressure)

    index_best = len(population) - 1 # It is the last 
    ind_star = Individual(population[index_best].candidate[:], population[index_best].fs)    

    for it in range(1, generation_max + 1):

        descendents = []

        # For each individual
        for _ in range(pop_size):
            if random.random() <= crossover_rate:
                # Select parents
                # pi = random.randint(0, pop_size - 1) # [a, b]
                # pj = pi

                # # Guarantee: pi != pj
                # while pj == pi:
                #     pj = random.randint(0, pop_size -1) # [a, b]

                [pi, pj] = roulette_wheel_selection(population, 2)

                # --- Reproduction
                # Perfom crossover
                child_one, child_two = crossover_ox(population[pi].candidate, population[pj].candidate)

                # Perform Mutation
                mutation_swap(child_one, mutation_rate)
                mutation_swap(child_two, mutation_rate)

                fs = tsp.full_eval(d, child_one)
                if random.random() <= local_search_rate:
                    child_one, fs, _ = local_search.vnd_first_improvement(d, child_one, fs, max_k)

                descendents.append(Individual(child_one, fs))

                fs = tsp.full_eval(d, child_two)
                if random.random() <= local_search_rate:
                    child_two, fs, _ = local_search.vnd_first_improvement(d, child_two, fs, max_k)       

                descendents.append(Individual(child_two, fs))

                # ---

        # -- Define survivors:
        
        # Merge: current population and descendents        
        merge = population + descendents

        # population = population + descendents
        # Sort merged population
        # population.sort(reverse = True, key = lambda i: i.fs)        
        # Remove individuals - shrink to pop_size
        # del population[pop_size:len(population)]

        # Fitness
        linear_ranking(merge, selective_pressure)
        # Selection
        survivors = roulette_wheel_selection(merge, pop_size)

        # Select individuals to the next generation
        population = []

        # Elitism
        last = len(merge) - 1
        population.append( copy.deepcopy(merge[last]) )

        for index in survivors:
            population.append( copy.deepcopy(merge[index]) )
            if (len(population) == pop_size):
                break

        linear_ranking(population, selective_pressure)

        # ---
        index_best = len(population) - 1 # It is the last individual
        if population[index_best].fs < ind_star.fs + local_search.EPS:
            ind_star = Individual(population[index_best].candidate[:], population[index_best].fs)

        # Print generations
        print(f"{it}\t{ind_star.fs}\t{population[index_best].fs}\n")

        # ---

    # for individual in population:
    #     individual.print() 

    return ind_star.candidate, ind_star.fs, time.time() - t_init, chart_data

def random_solution(d):

    individual = [*range(0, len(d))]
    random.shuffle(individual)

    fs = tsp.full_eval(d, individual)

    return individual, fs

def crossover_ox(parent_one, parent_two):

    # Two points
    cut = random.sample(range(2, len(parent_one) - 2), 2) 
    # Order - smaller and larger
    cut.sort()
    
    # print(f"Cut points: {cut}")

    # A = [6 3 8 | 2 4 1 | 5 7 9]
    # B = [1 2 7 | 4 6 5 | 8 9 3]

    # D1 = [ _ _ _ 2 4 1 _ _ _ ]
    # B3 + B1 + B2
    # Order = [ 8 9 3 1 2 7 4 6 5 ]

    # D2 = [ _ _ _ 4 6 5 _ _ _ ]
    # A3 + A1 + A2
    # Order = [ 5 7 9 6 3 8 2 4 1 ]

    # Create empty childreen
    # [ 0 0 0 0 0 0 0 0 0 ]
    child_one = [0] * len(parent_one)
    child_two = [0] * len(parent_two)

    # Copy sequence between cut[0] and cut [1] from parent one to child one
    c1, c2 = cut[0], cut[1] + 1
    child_one[c1:c2] = parent_one[c1:c2] 
    # The same for second child with parent two
    child_two[c1:c2] = parent_two[c1:c2] 

    # Starting from c2 until check all elements from parent two, insert on child one. 
    visit_order_p2 = parent_two[c2:len(parent_two)] + parent_two[0:c2]
    # Position to insert on child one - starting from c2
    position = c2
    for customer in visit_order_p2:
        # If customer does not exist in child one:
        if customer not in child_one:
            child_one[position] = customer
            position += 1

            if position == len(child_one):
                position = 0

    # The same process for the child two
    # This code will be rewrite as a function
    visit_order_p1 = parent_one[c2:len(parent_one)] + parent_one[0:c2]
    # Position to insert on child one - starting from c2
    position = c2
    # print(f"Starting from: {position}")
    # print(visit_order_p1)

    for customer in visit_order_p1:
        # If customer does not exist in child one:
        if customer not in child_two:
            # print(position)
            child_two[position] = customer
            position += 1

            if position == len(child_two):
                position = 0

    return child_one, child_two

def mutation_swap(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() <= mutation_rate:
            i = random.randint(0, len(individual) - 1) # [a, b]
            j = i

            # Guarantee: i != j
            while j == i:
                j = random.randint(0, len(individual) -1) # [a, b]

            # Swap i and j
            individual[i], individual[j] = individual[j], individual[i]

def linear_ranking(population, sp):

    nind = len(population)
    population.sort(reverse = True, key = lambda i: i.fs)

    # Calculate fitness    
    for i in range(1, nind + 1):
        population[i - 1].fitness = 2 - sp + 2 * (sp - 1) * \
            (( i - 1 ) / (nind - 1))

    min_value = population[0].fitness
    max_value = population[len(population) - 1].fitness

    # Normalize values - probabilities [0, 1]
    # Scaling: x' = [x - min()] / [ max() - min() ]
    for i in range(0, nind):
        population[i].probability = (population[i].fitness - min_value) / ( max_value - min_value )

def roulette_wheel_selection(population, nind_to_select):

    index_individuals = []

    ind = 0

    while ind < nind_to_select:
        prob = random.random()

        # Select distinct indexes
        for i in range(len(population)):
            if prob <= population[i].probability and i not in index_individuals:
                index_individuals.append(i)
                ind += 1
                break

    return index_individuals
