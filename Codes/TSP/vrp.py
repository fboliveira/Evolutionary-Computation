
class Problem:

    def __init__(self, cap, dem, d) -> None:
        self.cap = cap
        self.dem = dem
        self.d = self.d

class Route:

    def __init__(self, problem):
        self.list = []
        self.cost = float("inf")
        self.demand = 0
        self.problem = problem

class Solution:

    def __init__(self, problem) -> None:
        self.routes = []
        self.problem = problem

    def routeToGiantTour(self):
        giantTour = []
        for route in self.routes:
            r = route[:]
            r.pop(0)
            r.pop(len(r) - 1)
            giantTour = giantTour + r

    def giantTourToRoutes(self, tour):
        self.routes = []
        for i in tour:            
            pass

def metaheuristic(cap, dem, d):

    problem = Problem(cap, dem, d)
    solution = Solution(problem)

    r = Route(problem)
    solution.routes.append(r)
    


def calculate(problem : Problem):
    
    k = 10

    if k <= problem.dem:
        pass
