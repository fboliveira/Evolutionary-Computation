import tsp
import util
import random
import sys
from params import Params
import ga
import aco
import es

def main(args):
    args = ["main.py"]
    args.append("./datasets/att48.tsp")
    args.append("-algorithm")
    args.append("ACO")

    params = Params(args) 
    
    # read command line parameters
    d, coord = util.read_tsp(params.instance)
    if params.seed:
        random.seed(params.seed)  # change/remove to allow new random behavior (and solutions)
    if params.timelimit is None:
        params.timelimit = len(d)
        print("Unspecified run time limit set to (num cities)", params.timelimit, "\n")

    # build initial solution
    if params.constructive == "PARTGREEDY":
        s_ini, fs_ini, t = tsp.part_greedy_build(d, params.alpha)
    elif params.constructive == "GREEDY":
        s_ini, fs_ini, t = tsp.greedy_build(d)
    print("Initial solution of cost: ", round(fs_ini, 2))

    # run selected algorithm
    print("Running", params.algorithm)
    if params.algorithm == "GA": # FBO
        s, fs, t, data = ga.genetic_algorithm(d, params)
    elif params.algorithm == "ACO": # FBO
        s, fs, t, data = aco.ACO(d, params)
    elif params.algorithm == "ES": # FBO
        s, fs, t, data = es.ES(d, params)

    # write outputs (if allowed)
    if params.chart:
        util.plot_chart(data, f'output/{params.instance} {params.algorithm} {params.seed}.png', f'{params.algorithm} convergence chart', params.lb)
    if params.output:
        util.plot_sol(s, coord, f'output/{params.instance} {params.algorithm} {params.seed}.html', title=f'{params.instance} {params.algorithm} {params.seed} Cost `{round(fs, 2)}')

    # needed to iRace
    print(round(fs, 2), end="")


if __name__ == "__main__":
    main(sys.argv)