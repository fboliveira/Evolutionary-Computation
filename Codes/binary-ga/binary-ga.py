import random

def decode(individual, nvar, precision, min, max):

    phenotype = []
    decode_values = []

    for i in range(0, nvar):
        value = 0

        for j in range(0, precision):
            value += pow(2, precision - j - 1) * individual[ i * precision + j ]
                
        phenotype.append(value)

        float_value = (value * (max - min) / (pow(2, precision) - 1)) + min

        decode_values.append(float_value)

    return decode_values

def create_individual(nvar, precision) -> list[int]:
    
    individual = []

    for _ in range(0, nvar):
        for _ in range(0, precision):
            individual.append(random.randint(0, 1))

    return individual

def calculate_objective_function(values) -> float:
    """ Sum of x^2 """
    sum = 0

    for x in values:
        sum += x ** 2

    return sum


if __name__ == '__main__':
    precision = 7
    min = -100
    max = 100
    nvar = 2
    pop_size = 5

    it_max = 10

    population = []
    costs = []

    for _ in range(0, pop_size):
        individual = create_individual(nvar, precision)
        values = decode(individual, nvar, precision, min, max)
        ofc = calculate_objective_function(values)

        population.append((individual, ofc))
        costs.append(ofc)

    print(population)
    population.sort(key=lambda ind: ind[1])
    print(f'Sorted: {population}')