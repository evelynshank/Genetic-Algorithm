# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 13:41:49 2019

@author: Evelyn
"""
# Goal: From some point on the groud, launch an object 150m. With all other variables held constant, 
# we will be evolving multiple combinations of velocity and theta which we can launch the
# projectile in order to find a set that shoots the projectile as close to 150m as possible.

# Importing libraries we need
import numpy as np
import copy
from timeit import default_timer

# Creates a class of individuals. These will be the individual combinations of velocity and
# theta that launch the projectile a certain distance.
class indiv:

    # Defining the function that creates the initial population
    def __init__(self, gen):
        self.gen = gen
        self.v = np.random.uniform(low=0, high= 100)
        self.theta = np.random.uniform(low= 0, high= 90)
        
    # Defining the function that mutates the individual you give it. This function randomly selects
    # one attribute of the individual, either its velocity or theta, and increases or decreases that 
    # value by a maximum of 15. 
    def Mut(self):
        binary = np.random.randint(low = 0, high = 2)
        
        if binary == 1:
            self.v = np.random.uniform(low = self.v-15 , high = self.v+15)
            while self.v < 0:
                self.v = np.random.uniform(low = self.v-15 , high = self.v+15)
                
        else:
            self.theta = np.random.uniform(low = self.theta-15, high = self.theta+15)
            while self.theta < 0 or self.theta > 90:
                self.theta = np.random.uniform(low = self.theta-15, high = self.theta+15)
        
    # Defining the function that will only slightly mutate the individual you give it. Same concept
    # as the preceeding function, but it can only alter the theta or velocity by 5. Used on individuals
    # with high fitness scores in order to fine tune them. 
    def fineMut(self):
        binary = np.random.randint(low = 0, high = 2)
        
        if binary == 1:
            self.v = np.random.uniform(low = self.v-5 , high = self.v+5)
            while self.v < 0:
                self.v = np.random.uniform(low = self.v-5 , high = self.v+5)
                
        else:
            self.theta = np.random.uniform(low = self.theta-15, high = self.theta+5)
            while self.theta < 0 or self.theta > 90:
                self.theta = np.random.uniform(low = self.theta-15, high = self.theta+5)
         
    # Defining a function that calculates fitness score (get as close to 150m as possible).
    def rangeFit(self):
        '''return np.sqrt((1/(150-(((self.v**2)/9.8)*np.sin(2*self.theta)))**2) + (1/((45-(self.theta))**2)))'''
        return 1/(150-((self.v**2/9.8)*np.sin(2*self.theta)))**2
        '''return np.sqrt((1/(150-(((self.v**2)/9.8)*np.sin(2*self.theta)))**2) + (1/(self.v**2)) + (1/(((2*self.v)/9.8)*np.sin(2*self.theta))))'''

# Initializing all lists used in the loop
Pop = []
sortedPop = []
newPop = []
bestPop = []
tourney = []
sortedTourney = []
sortedNewPop = []
finalPop = []
genTicker = 0

# Start the timer that tracks how long it takes to get an answer
start = default_timer()

# Creating the initial population
for x in range(100):
    Pop.append(indiv(0))
    
# Sorting the individuals according to fitness score high-low in the very first generation
if genTicker == 0:
    for x in Pop:
    
        i = 0
        
        while i <= len(sortedPop)-1 and x.rangeFit() < sortedPop[i].rangeFit():
            
            i = i+1
    
        sortedPop.insert(i, x)
        
    
# Checks the best fitness score out of all the individuals. If it is close enough to the desired
# solution, the loop stops and the individual is printed as the final answer. If not, it runs
# through the generational loop until a suitable individual is found. Or, if the algorithm takes more
# than 100 generations to solve, it terminates.
check = sortedPop[0].rangeFit()

while check <= 300 and genTicker <= 100:
    '''''''''''''''''''''''''''''''Start the Loop'''''''''''''''''''''''''''''''

    # First Cut: Selecting the individuals with the top ten fitness scores, putting them into 
    # the next generation (defined as the currently empty list, newPop).
    newPop.extend(sortedPop[0:10])
    
    
    # Second Cut: Selecting individuals with top ten fitness scores, mutating using fineMut function, 
    # appending to new generation.
    bestPop.extend(sortedPop[0:10])
    
    for x in bestPop:
        copiedData = copy.deepcopy(x)
        copiedData.fineMut()
        newPop.append(copiedData)
    '''For Testing'''
    '''for x in newPop:
        print(x.rangeFit())'''
        
        
    # Third Cut: Selecting 60 individuals at random and mutating them using Mut. Appending to the 
    # tourney list, which will be used in the next step to determine which of these individuals will
    # make it into the final population.
    for x in range(60):
        lotteryNum = np.random.randint(low = 0, high = 100)
        newCopy = copy.deepcopy(sortedPop[lotteryNum])
        newCopy.Mut()
        tourney.append(newCopy)
 
    # Out of the 60 new mutations, appending the 40 with the highest fitness scores to the new 
    # generation.
    for x in tourney:
    
        i = 0
        while i <= len(sortedTourney)-1 and x.rangeFit() < sortedTourney[i].rangeFit():
            i = i+1
    
        sortedTourney.insert(i, x)
        
    newPop.extend(sortedTourney[0:40])
    
    # Emptying out the tourney arrays so they can be used in the next cut
    tourney[:] = []
    sortedTourney[:] = []
    
    
    # Fourth Cut: Selecting 60 parents and mutating them using the cross-over method. Appending
    # to the tourney list.
    for x in range(30):
        
        lotteryNum = np.random.randint(low = 0, high = 100)
        parentOne = copy.deepcopy(sortedPop[lotteryNum])
        
        lotteryNumTwo = np.random.randint(low = 0, high = 100)
        
        while lotteryNumTwo == lotteryNum:
            lotteryNumTwo = np.random.randint(low = 0, high = 100) 
            
        parentTwo = copy.deepcopy(sortedPop[lotteryNumTwo])
        
        binary = np.random.randint(low = 0, high = 2)
        
        if binary == 1:
            geneOne = parentOne.v
            tempGeneOne = parentOne.v
            geneTwo = parentTwo.v
            
            parentOne.v = geneTwo
            parentTwo.v = tempGeneOne
            
        else:
            geneOne = parentOne.theta
            tempGeneOne = parentOne.theta
            geneTwo = parentTwo.theta
            
            parentOne.theta = geneTwo
            parentTwo.theta = tempGeneOne
            
        tourney.append(parentOne)
        tourney.append(parentTwo)
        
    # Out of the 60 new mutations, appending the 40 with the highest fitness scores to the new 
    # generation.
    for x in tourney:
    
        i = 0
        while i <= len(sortedTourney)-1 and x.rangeFit() < sortedTourney[i].rangeFit():
            i = i+1
    
        sortedTourney.insert(i, x)
        
    newPop.extend(sortedTourney[0:40])
    
    
    # Final Cut: Sorting the 100 individuals in the new generation by fitness score from high-low and 
    # cutting the bottom 10.
    for x in newPop:
    
        i = 0
        while i <= len(sortedNewPop)-1 and x.rangeFit() < sortedNewPop[i].rangeFit():
            i = i+1
    
        sortedTourney.insert(i, x)
        
    finalPop.extend(sortedTourney[0:90])
    
    # Adding 10 new random individuals to the final population for diversity
    for x in range(10):
        finalPop.append(indiv(0))
        
    
    # Update the generation number that keeps track of which generation the current population
    # is a part of.
    genTicker = genTicker + 1
    
    
    # Cleaning out all of the lists except for the final population for re-use in subsequent gens
    Pop = []
    sortedPop = []
    newPop= []
    bestPop= []
    tourney= []
    sortedTourney = []
    sortedNewPop = []
    
    
    # Sorting the final population by fitness score from high-low, putting back into the sortedPop
    # list so that the generational loop can run again
    for x in finalPop:
    
        i = 0
        
        while i <= len(sortedPop)-1 and x.rangeFit() < sortedPop[i].rangeFit():
            
            i = i+1
    
        sortedPop.insert(i, x)
    
    
    check = sortedPop[0].rangeFit()
    
    print(check)
    
    '''for x in sortedPop:
        vel = x.v
        print(vel)'''

'''''''''''''''''''''''''''''''''Finish the Loop'''''''''''''''''''''''''''''''''''''''
# Determining and printing the final results

finalV = sortedPop[0].v
finalTheta = sortedPop[0].theta
finalScore = sortedPop[0].rangeFit()
runTime = default_timer() - start

# If the loop was successful, print the results
if genTicker <= 100:
    print("   ")
    print("Here's your answer!")
    print("")
    print("Velocity = ",finalV)
    print("Theta = ",finalTheta)
    print("Final Fitness Score = ",finalScore)
    print("")
    print("Run time = ", runTime, "seconds.")
    
# If the loop took too long, say so!
if genTicker > 100:
    print("Sorry, it looks like our algorithm got stuck :(")
    print("Please try again")