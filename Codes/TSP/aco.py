"""
Ant Colony Optimization for the Travelling Salesman Problem - TSP
"""

import random
import time
import local_search
import tsp

class Ant:

    def __init__(self, cities, graph):
        self.cities = cities
        # self.delta_gamma = [[0 for i in range(cities)] for j in range(cities)]
        self.graph = graph
        self.start = random.randint(0, cities - 1) # First node
        self.route = []
        self.route.append(self.start)
        self.fs = float("inf")

class Graph:

    def __init__(self, d, cities):
        self.cities = cities

        # Matrix[n, n] <- 0
        self.eta = [[ 0 for i in range(cities) ] for j in range(cities)]
        
        for i in range(cities):
            for j in range(cities):
                if i != j:
                    self.eta[i][j] = 1 / d[i][j]

        # Scary version
        #  self.eta = [[0 if i == j else 1 / d[i][j] for j in range(self.cities)] for i in range(self.cities)]

class Solution:

    def __init__(self, customers, fs):
        self.customers = customers
        self.fs = fs

def ACO(d, params):

    t_init = time.time()
    chart_data = []

    n_ants = len(d) # m    

    # Ant probability - pk_ij
    alpha = 5.0
    beta = 10.0
    
    start_gamma = 0.5 # Gamma_0
    Q = 10 # a constant related to the quantity of trail laid by ants
        
    rho = 0.001 # trail persistence

    cycles = 100 # generations, iterations, ...

    f_star = Solution([], float("inf"))
    cities = len(d)

    # Local search - VND
    max_k = 4

    # Gamma
    pheromone = [[start_gamma for i in range(cities)] for j in range(cities)]

    # Problem info - graph
    # Heuristic information
    graph = Graph(d, cities)

    # Delta Gamma - update pheromone
    delta_pheromone = [[0 for i in range(cities)] for j in range(cities)]

    # #
    # colony = []

    # # Create m ants
    # for i in range(n_ants):
    #     ant = Ant(cities, graph)
    #     colony.append(ant)

    # Cycles
    # Stop criteria - IterMax?
    for it in range(1, cycles + 1):

        # Create ants
        for k in range(n_ants):

            # Create an ant
            ant = Ant(cities, graph)

            # Create routes
            create_route(cities, ant, pheromone, alpha, beta)          

            # Evaluate 3 c)
            ant.fs = tsp.full_eval(d, ant.route) # Lk

            # Local search
            # ant.route, ant.fs, _ = local_search.random_descent(d, ant.route, ant.fs, 1000)   

            # Check if the ant is better than F*
            # 3 (d)
            if ant.fs < f_star.fs + local_search.EPS:
                f_star = Solution(ant.route[:], ant.fs)

            # Delta Gamma - Ant K
            # 3 (e)
            delta_pheromone_ant = [[0 for i in range(cities)] for j in range(cities)]

            # Update pheromone left by ant k
            for i in range(cities - 1):
                ci = ant.route[i]
                cj = ant.route[i + 1]
                
                delta_pheromone_ant[ci][cj] = d[ci][cj] * ( Q / ant.fs )

            # Update delta pheromone
            # 3 (f)
            for i in range(cities):
                for j in range(cities):
                    delta_pheromone[i][j] += delta_pheromone_ant[i][j]

        # Update pheromone trail
        # 5
        for i in range(cities):
            for j in range(cities):
                pheromone[i][j] = ( 1 - rho ) * pheromone[i][j] + delta_pheromone[i][j]

        # Stop criteria -> 7 - 9

        print(f"{it}\t{f_star.fs}")

    return f_star.customers, f_star.fs, time.time() - t_init, chart_data

def create_route(cities, ant : Ant, pheromone, alpha, beta):

    cities_to_visit = [*range(0, cities)]
    # Remove first node - start
    current = ant.start
    cities_to_visit.remove(current)

    # [5]
    while cities_to_visit:
        j = select_next_city(ant, current, cities_to_visit, pheromone, alpha, beta)
        # j = 8
        # [5 -> 8]
        ant.route.append(j)
        cities_to_visit.remove(j)
        # 8
        current = j

def select_next_city(ant : Ant, current_city, cities_to_visit, pheromone, alpha, beta):

    denominator = 0.0

    for l in cities_to_visit:
        denominator += ( pheromone[current_city][l] ** alpha ) * ( ant.graph.eta[current_city][l] ** beta )

    probabilities = [ 0 for i in range(ant.graph.cities) ]

    # i = current_city
    for j in cities_to_visit:
        probabilities[j] = ((pheromone[current_city][j] ** alpha) * (ant.graph.eta[current_city][j] ** beta)) / denominator

    # 0.3
    rand = random.random()

    selected = -1
    for i in range(len(probabilities)):
        # i[0] = 0.05
        rand -= probabilities[i]
        # 0.3 - 0.05 = 0.25
        if rand <= 0:
            selected = i
            break
    
    return selected