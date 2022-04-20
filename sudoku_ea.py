# "Sudoku Solver" EVOLUTIONARY ALGORITHM  

import numpy
from random import choice, random
import random
random.seed() 

### EVOLUTIONARY ALGORITHM ###
def evolve(grid):
    init_pop = []
    population = []
    best_fit = 0
    gen = 0
    i = 0
    
    # Create the inital population
    for _ in range(POPULATION_SIZE):
        init_pop.append(grid)
    # Fill any empty spaces ('0') with random numbers
    for pop in init_pop:
        population.append(create_pop(pop))
    fitness_population = evaluate_pop(population)
    best_i, best_f = best_pop(population, fitness_population)
    
    # While the result is not equalt to the highest fitness score and 
    # the fitness score has not be repeated for more than 50 generations:
    while((best_fit < 243) & (i < 50)):
        best_i, best_f = best_pop(population, fitness_population)
        mating_pool = select_pop(population, fitness_population)
        fitness_population = evaluate_pop(mating_pool)
        offspring_population = crossover_pop(mating_pool)
        population = mutate_pop(offspring_population, grid)
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        gen += 1
        print("#%3d" % gen, "fit:%3d" % best_fit, "list, " + str(gen))
        # If the user would like the Sudoku board printed out uncomment the following:
        #for best in best_ind:
        #    print(best)
        if best_f == best_fit:
            i += 1
        else:
            i = 0

### POPULATION-LEVEL OPERATORS ###

def create_pop(population):
    return [create_ind(pop) for pop in population]

def evaluate_pop(population):
    return [ fitness_func(individual) for individual in population ]

# Returns a list of the best fitness puzzles
def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    sorted_population.reverse()
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

# Crosses over two parent puzzles
def crossover_pop(population): 
    new_population = []
    for _ in range(int(POPULATION_SIZE/2)):
        offspring = crossover(choice(population), choice(population))
        new_population.append(offspring[0])
        new_population.append(offspring[1])
    return new_population

def mutate_pop(population, grid):
    return [ mutate_ind(individual, grid) for individual in population ]

# Returns the best puzzle from the population
def best_pop(population, fitness_population):
    best = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    best.reverse()
    return best[0]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

INDIVIDUAL_SIZE = 9

# Starts with an alphabet that has the digits already in the row removed
# Then populates the row removing each digit placed in.
def create_ind(pop):
    list = []
    alphabet = '123456789'
    for n in pop:
        if n != '0':
            alphabet = alphabet.replace(n, '')
    for n in pop:
        if n == '0':
            c = choice(alphabet)
            list.append(c)
            alphabet = alphabet.replace(c, '')
        else:
            list.append(n)
    return list

# counts each unique number in every row, column and 3x3 square
def fitness_func(individual):
    x = 0
    y = 0
    
    # Counting for row 
    for i in range(9):
        f = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for n in range(9):
            if individual[i][n] in f:
                f.remove(individual[i][n])
                x +=1
                
    # Counting for column
    for i in range(9):
        f = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for n in range(9):
            if individual[n][i] in f:
                f.remove(individual[n][i])
                x +=1
                
    # Counting for 3x3 square
    for i in range(0, 9, 3):
        f = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for j in range(0, 9, 3):
            if individual[i][j] in f : x += 1
            if individual[i][j+1] in f: x += 1
            if individual[i][j+2] in f: x += 1
            
            if individual[i+1][j] in f: x += 1
            if individual[i+1][j+1] in f: x += 1
            if individual[i+1][j+2] in f: x += 1
            
            if individual[i+2][j] in f: x += 1
            if individual[i+2][j+1] in f: x += 1
            if individual[i+2][j+2] in f: x += 1
    return x

# chooses a random row from each parent to be crossed over.
def crossover(parent1, parent2):
    child1 = numpy.zeros((9, 9), dtype=int)
    child2 = numpy.zeros((9, 9), dtype=int)
    child3 = []
    child4 = []
    
    # Make a copy of the parent genes.
    child1 = parent1
    child2 = parent2
    
    c1 = []
    c2 = []
    
    crossover_point = random.randint(0, 8)
    c1, c2 = crossover_rows(child1[crossover_point], child2[crossover_point])
    for i in range(len(child1)):
        if i == crossover_point:
            child3.append(c1)
        else:
            child3.append(child1[i])
            
    for i in range(len(child2)):
        if i == crossover_point:
            child4.append(c2)
        else:
            child4.append(child2[i])
    
    return child3, child4

# Crosses over the two rows
def crossover_rows(row1, row2):
    child_row1 = row2
    child_row2 = row1
    return child_row1, child_row2 

# Randomly swaps two numbers in a row, if the number selected was from the original puzzle then it chooses a different position
def mutate_ind(individual, grid):
    i = 0
    new_list = []
    for ch in individual:
        r1 = 0
        r2 = 0 
        list = []
        r1 = random.randint(0,8)
        r2 = random.randint(0,8)
        
        while (grid[i][r1] != '0'):
            r1 = random.randint(0,8)
        while (grid[i][r2] != '0'):
            r2 = random.randint(0,8)
        
        if (random.random() < MUTATION_RATE):
            for n in range(9):
                if n == r1: 
                    list.append(ch[r2])
                elif n == r2: 
                    list.append(ch[r1])
                else: 
                    list.append(ch[n])
            new_list.append(list)
            
        else:
            new_list.append(ch)
        i += 1
    return individual

### PARAMERS VALUES ###

POPULATION_SIZE = 1000
TRUNCATION_RATE = 0.5
MUTATION_RATE = 1.0 / INDIVIDUAL_SIZE

# hard coded sudoku puzzle
grid1  = [
    ['3', '0', '0', '0', '0', '5', '0', '4', '7'], 
    ['0', '0', '6', '0', '4', '2', '0', '0', '1'], 
    ['0', '0', '0', '0', '0', '7', '8', '9', '0'],
    ['0', '5', '0', '0', '1', '6', '0', '0', '2'],
    ['0', '0', '3', '0', '0', '0', '0', '0', '4'],
    ['8', '1', '0', '0', '0', '0', '7', '0', '0'],
    ['0', '0', '2', '0', '0', '0', '4', '0', '0'],
    ['5', '6', '0', '8', '7', '0', '1', '0', '0'],
    ['0', '0', '0', '3', '0', '0', '6', '0', '0']
    ]

grid2 = [
    ['0', '0', '2', '0', '0', '0', '6', '3', '4'],
    ['1', '0', '6', '0', '0', '0', '5', '8' ,'0'],
    ['0', '0', '7', '3', '0', '0', '2', '9', '0'],
    ['0', '8', '5', '0', '0', '1', '0', '0', '6'],
    ['0', '0', '0', '7', '5', '0', '0', '2', '3'],
    ['0', '0', '3', '0', '0', '0', '0', '5', '0'],  
    ['3', '1', '4', '0', '0', '2', '0', '0', '0'], 
    ['0', '0', '9', '0', '8', '0', '4', '0', '0'], 
    ['7', '2', '0', '0', '4', '0', '0', '0', '9']
    ]

grid3 = [
    ['0', '0', '4', '0', '1', '0', '0', '6', '0'], 
    ['9', '0', '0', '0', '0', '0', '0', '3', '0'], 
    ['0', '5', '0', '7', '9', '6', '0', '0', '0'], 
    ['0', '0', '2', '5', '0', '4', '9', '0', '0'], 
    ['0', '8', '3', '0', '6', '0', '0', '0', '0'], 
    ['0', '0', '0', '0', '0', '0', '6', '0', '7'],
    ['0', '0', '0', '9', '0', '3', '0', '7', '0'], 
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'], 
    ['0', '0', '6', '0', '0', '0', '0', '1', '0'],
    ]

### EVOLVE! ###

evolve(grid2)