# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:35:34 2019

@author: Evelyn
"""
import numpy as np
from timeit import default_timer

# Creating an individual with these properties
class indiv:
    
    def __init__(self, v, theta, fitScore):
        self.v = v
        self.theta = theta
        self.fitScore = fitScore
        
Pop = [] 
sortedPop = []    
Thetas = []
Vels = []
velIndex = 0
comboTicker = 0

# Start a timer that tracks how long it takes to reach an answer
start = default_timer()

# Creating an array of all possible v's and theta's
Thetas = np.arange(1, 90)
Vels = np.arange(1, 100)

# Pick a theta value, cycle through all vels for that theta. For each combination, calculate that
# individual's fitness score ('fitness') and put that v, theta, and fitness score into an individual.
# Then, add that new individual to the population ('Pop').

for x in Thetas:
    for v in Vels:
         fitness = 1/(150-((v**2/9.8)*np.sin(2*x)))**2
         newIndiv = indiv(v, x, fitness)
         Pop.append(newIndiv)
         #comboTicker = comboTicker + 1
         #print(comboTicker)
         
         
# Arrange all values in Pop by fitness score, pick the best one and print it        
for x in Pop:
    
        i = 0
        
        while i <= len(sortedPop)-1 and x.fitScore < sortedPop[i].fitScore:
            
            i = i+1
    
        sortedPop.insert(i, x)


# Print the solution and the time it took to arrive there
        
bestV = sortedPop[0].v
bestTheta = sortedPop[0].theta
bestFit = sortedPop[0].fitScore
runTime = default_timer() - start
runMinutes = runTime / 60

print("Here's your solution!")
print()
print("Velocity = ", bestV)
print("Theta = ", bestTheta)
print("Fitness Score = ", bestFit)
print("Seconds run = ", runTime)
print("Minutes run = ", runMinutes)

print(theta_list)
print()