'''---------------------------------------------------------------------------
This program is written by Chashman 2021-MC-70 for a mid term project of CP-I.
This program find a suitable and fittest path for agent using Genetic Algorithm.
It contain different user defined functions. 
Project submitted to Dr Muhammad Ahsan Naeem 
On 2nd April,2023.
------------------------------------------------------------------------------'''
# Including required libraries 
from pyamaze import maze, agent
import matplotlib.pyplot as p
from random import *
from copy import *

# Function for generation of random population
def random_population():
    # Local pop list for storing one chromosome
    pop = []
    # Population generation code when rows are less than or equal to columns
    if rows <= columns:
        for i in range(pop_size):
            # Fixing first element of each chromosome
            pop.append(1)
            # Loop for generating remaining elements randomly
            for j in range(columns-2):
                pop.append(randint(1, rows))
            # Fixing last element of each chromosome
            pop.append(rows)
            # Appending in global list
            population.append(pop)
            # Empty local list for next chromosome
            pop = []
    else:
        for i in range(pop_size):
            # Fixing first element of each chromosome
            pop.append(1)
            for j in range(rows-2):
                pop.append(randint(1, columns))
            # Fixing last element of each chromosome
            pop.append(columns)
            # Appending values in global list
            population.append(pop)
            pop = []

# Function for printing population in a preentable way
def Print_Population():
    for i in population:
        print(i)

# Mutation function 
def Mutation():
    if rows <= columns:
        # Loop for mutation of each chromosome of any random element
        for i in population:
            i[randint(1, columns-2)] = randint(1, rows)
    else:
        # Loop for mutation of each chromosome of any random element
        for i in population:
            i[randint(1, rows-2)] = randint(1, columns)

# Crossover function
def Crossover():
    # Crossover of half chromosomes that's why range is  upto half of 
    # population size
    for i in range(0, pop_size//2, 2):
        # Generating deepcopy of parent chromosomes
        ancestor1 = deepcopy(population[i])
        ancestor2 = deepcopy(population[i+1])
        # Choosing random crosspoint and swapping parts for crossover
        if rows <= columns:
            for j in range(randint(1, columns-2), columns):
                ancestor1[j], ancestor2[j] = ancestor2[j], ancestor1[j]
        else:
            for j in range(randint(1, rows-2), rows):
                ancestor1[j], ancestor2[j] = ancestor2[j], ancestor1[j]
        # Storing offspring in parent chromosomes
        population[(pop_size//2)+i] = ancestor1
        population[(pop_size//2)+(i+1)] = ancestor2

# Path function
def Track():
    # Local path list
    path = []
    for i in population:
        if rows <= columns:
            for j in range(columns-1):
                # If difference of to consuctive number is +ve or equal to zero 
                # then this loop will execute 
                if i[j+1]-i[j] >= 0:
                    for k in range(i[j], i[j+1]+1):
                        # Appending path in form of tuples
                        path.append((k, j+1))
                if i[j+1]-i[j] < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        path.append((k, j+1))
            # Last tuple or step should be goal point
            path.append((rows, columns))
        else:
            for j in range(rows-1):
                if i[j+1]-i[j] >= 0:
                    for k in range(i[j], i[j+1]+1):
                        path.append((j+1, k))
                if i[j+1]-i[j] < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        path.append((j+1, k))
            path.append((rows, columns))

        # Appending values in global list
        track.append(path)
        path = []

# Obstacle count funtion
def Hinder():
    obstacle = 0
    for i in track:
        # Loop for checking obstacle
        for j in range(len(i)-1):
            # Moving downward so check if there is an obstacle in South or not
            if i[j+1][0]-i[j][0] > 0 and i[j+1][1] == i[j][1]:
                if finalMap[i[j]]["S"] == 0:
                    obstacle += 1
            # Moving upward so check if there is an obstacle in North or not
            if i[j+1][0]-i[j][0] < 0 and i[j+1][1] == i[j][1]:
                if finalMap[i[j]]["N"] == 0:
                    obstacle += 1
            # Moving rightward so check if there is an obstacle in East or not
            if i[j+1][1]-i[j][1] > 0 and i[j+1][0] == i[j][0]:
                if finalMap[i[j]]["E"] == 0:
                    obstacle += 1
            # Moving leftward so check if there is an obstacle in West or not
            if i[j+1][1]-i[j][1] < 0 and i[j+1][0] == i[j][0]:
                if finalMap[i[j]]["W"] == 0:
                    obstacle += 1
        # Appending values in global list
        hinder.append(obstacle)
        obstacle = 0
# Step count function
def StepCount():
    # Appending values in global list
    for i in track:
        steps.append(len(i))

# Turns count function
def Turns():
    turn = 0
    for i in population:
        for j in range(len(i)-1):
            # If next element is not equals previous it means there is a turn
            if i[j+1] != i[j]:
                # So turn variable +1
                turn += 1
        # Appending values in global list
        turns.append(turn)
        turn = 0

# Fitness funcion
def Fitness():
    # Invading required functions in fitness function
    Track()
    Hinder()
    StepCount()
    Turns()
    # Defining required variables
    weight_hinder = 3
    weight_turn = 2
    weight_step = 2
    # Loop for calculating fitness value of obstacle,turn and steps and then total 
    # fitness of each path obtained
    for i in range(pop_size):
        fit_obs = 1-((hinder[i]-min(hinder))/(max(hinder)-min(hinder)))
        fitness_obstacle.append(fit_obs)
        fit_turn = 1-((turns[i]-min(turns))/(max(turns)-min(turns)))
        fitness_turn.append(fit_turn)
        fit_step = 1-((steps[i]-min(steps))/(max(steps)-min(steps)))
        fitness_step.append(fit_step)
        # Total fitness 
        fitness = 100*(weight_hinder*fit_obs)*(((weight_turn*fit_turn) +
                                                (weight_step*fit_step))/(weight_step+weight_turn))
        # Appending values in global list
        Total_fitness.append(fitness)

# Sorting function
def Parenting():
    # Loop for scanning each element
    # Reaon for range one less than population size is we want to trigger each element
    for i in range(pop_size-1):
        for j in range(i+1, pop_size):
            if Total_fitness[j] > Total_fitness[i]:
                # Swapping chromosomes and fitness value according to greater fitness value
                Total_fitness[j], Total_fitness[i] = Total_fitness[i], Total_fitness[j]
                population[j], population[i] = population[i], population[j]

# Solution check function
def IsSolution():
    solution = []
    for i in range(pop_size):
        # Condition for solution 
        if hinder[i] == 0 and Total_fitness[i] >= 0:
            # Storing value of a that path which is Solution in a new local list
            solution = track[i]
            # Storing result in a dictionary
            for j in range(len(solution)-1):
                FinalResult.update({solution[j+1]: solution[j]})
            return 1
    return 0

# Code of block to plot graphs
'''x = [i for i in range(1, 501)]
p.xlabel("Population")
p.plot(x, hinder, color="b")
p.ylabel("Hinders")
p.title("Graph Between Population vs Hinders")
p.plot(x, steps, color="b")
p.ylabel("Steps")
p.title("Graph Between Population vs Steps")
p.plot(x, turns, color="b")
p.ylabel("Turns")
p.title("Graph Between Population vs Turns")
p.plot(x, Total_fitness, color="b")
p.ylabel("Fitness")
p.title("Graph Between Population vs Fitness")
p.show()
Global variables and Main function program'''

# Global variables
population = []
rows = 15
columns = 15
pop_size = 500
# Storing ouput maze in a variable m with rows and columns as input arguments
m = maze(rows, columns)
# Creating maze 
m.CreateMaze(pattern=None, loopPercent=100, theme="dark")
# Agent as a variable
a = agent(m, filled=True, footprints=True, shape="arrow", color="blue")
# Map as finalMap variable
finalMap = m.maze_map
# Main function 
random_population()
iteration = 0
# Loop for finding solution with a terminating condition  
while True:
    iteration += 1
    track = []
    hinder = []
    steps = []
    turns = []
    fitness_obstacle = []
    fitness_turn = []
    fitness_step = []
    Total_fitness = []
    FinalResult = {}

    Fitness()
    # Output of solution function is stored in variable "b"
    b = IsSolution()
    if b:
        # If solution found print this tatement 
        if iteration==1:
            print(f"Solution found after {iteration} iteration")
        else:
            print(f"Solution found after {iteration} iterations")
        # When solution is found display the result in separate window 
        # Using tracePath and run function of pyamaze
        m.tracePath({a: FinalResult},delay=150)
        m.run()
        # And then break the loop
        break
    Parenting()
    Crossover()
    Mutation()
# End of program 
# Thank you :)