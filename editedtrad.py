# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:35:34 2019

@author: Evelyn
"""
import numpy as np
from timeit import default_timer
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Creating an individual with these properties
class indiv:

	def __init__(self, v, theta, fitScore):
		self.v = v
		self.theta = theta
		self.fitScore = fitScore


#I'm gonna adjuts Evelyn's code to run over a series of different increments and then output the run times for those increments in a list

#initialize the increments
theta_increment = .8
vel_increment = .8


#create lists to hold the increments and corresponding run times
theta_list = []
vel_list = []
runTimes = []

#put in the first increments to their respective lists
#theta_list.append(theta_increment)
#vel_list.append(vel_increment)

g = 0
while g < 10:
	Pop = []
	sortedPop = []  
	Thetas = []
	Vels = []
	velIndex = 0
	comboTicker = 0
	# Start a timer that tracks how long it takes to reach an answer
	start = default_timer()

	# Creating an array of all possible v's and theta's
	Thetas = np.arange(1, 90, theta_increment)
	Vels = np.arange(1, 100, vel_increment)
	# Pick a theta value, cycle through all vels for that theta. For each combination, calculate that
	# individual's fitness score ('fitness') and put that v, theta, and fitness score into an individual.
	# Then, add that new individual to the population ('Pop').

	for x in Thetas:
		for v in Vels:
			fitness = 1/(150-((v**2/9.8)*np.sin(2*x)))**2
			newIndiv = indiv(v, x, fitness)
			Pop.append(newIndiv)
			comboTicker = comboTicker + 1
	#	print(comboTicker)]  
		 
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

	#add to the list of run times
	runTimes.append(runTime)

	#throw in the new increments to the increment lists
	theta_list.append(theta_increment)
	vel_list.append(vel_increment)

	#increment the theta increment for each run through the main loop
	theta_increment += .05
	vel_increment += .05

	g += 1

"""
print("Here's your solution!")
print()
print("Velocity = ", bestV)
print("Theta = ", bestTheta)
print("Fitness Score = ", bestFit)
print("Seconds run = ", runTime)
print("Minutes run = ", runMinutes)
"""

print(runTimes)

#let's plot the data
plt.figure(figsize = (8, 8))
plt.plot(theta_list, runTimes, 'ro')
plt.show()

print(theta_list)
print(runTimes)

'''for x in range(theta_list)
    sns.regplot(theta_list[x], runTimes[x])
plt.show()'''

'''for x in theta_list:
    print(theta_list[x])
    
for x in vel_list:
    print(vel_list[x])'''
    