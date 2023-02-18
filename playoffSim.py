# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 04:12:26 2023

@author: Stephen
"""

import numpy as np
from matplotlib import pyplot as plt

class Baseball():
    
    
    def __init__(self, nationalLeague, americanLeague):
        self.nl = nationalLeague
        self.al = americanLeague
           
    
    def simulateMatchup(self, teamA, teamB):
        '''Function that takes two teams and weights as parameters.
        The stronger team should be teamA, the weaker as teamB.
        Returns the values of the loser'''
        
        random = np.random.uniform(0,1)             # Get random num between 0 and 1

        winRatio = teamA[1]/(teamA[1] + teamB[1])   # Get ratio of stronger team vs weaker team
        if random > winRatio:                       # If random num is greater than winRatio
            loser = [teamA[0], teamA[1]]            # Loser is stronger team
        else:                                       # If random num is lower than winRatio
            loser = [teamB[0], teamB[1]]            # Loser is weaker team
      
        return loser                                # Return loser
    
    
    def simulatePlayoffs(self):
        '''Function that simulates 2022 playoff scenario'''
        
        self.wildCard()                     # Simulate wild card round
        self.divisionSeries()               # Simulate divisional series round
        self.championshipSeries()           # Simulate league championship round
        champ = self.worldSeries()          # Simulate world series
                
        return champ
    
    
#   def runSimulation(self, trials = 1000000):
#        '''Function that runs the playoff scenario a default 1,000,000 times.
#        Track the world series winners and plot results'''
        
#        champions = []
#        nlCopy = self.nl
#        alCopy = self.al
        
#        for i in range(trials):
#            champions.append(self.simulatePlayoffs())
            
        #fig, axs = plt.subplots()
        #axs[0].bar()
            
            
#        return champions
       
        
        
        
        
        
        
    
    
    def wildCard(self):
        '''Function that eliminates wild card round losers'''
        
        nl = {}
        al = {}
        
        # American League 3/6 matchup
        am1 = self.simulateMatchup(self.al[3], self.al[6])                  # Simulate matchup and return loser values
        value1 = list(self.al.keys())[list(self.al.values()).index(am1)]    # Get key from loser values
        del self.al[value1]                                                 # Remove loser from playoffs
        
        # American League 4/5 matchup
        am2 = self.simulateMatchup(self.al[4], self.al[5])
        value2 = list(self.al.keys())[list(self.al.values()).index(am2)]
        del self.al[value2]
        
        # National League 3/6 matchup
        am3 = self.simulateMatchup(self.nl[3], self.nl[6])
        value3 = list(self.nl.keys())[list(self.nl.values()).index(am3)]
        del self.nl[value3]
        
        # National League 4/5 matchup
        am4 = self.simulateMatchup(self.nl[4], self.nl[5])
        value4 = list(self.nl.keys())[list(self.nl.values()).index(am4)]
        del self.nl[value4]
        
        return
        
        
    def divisionSeries(self):
        '''Function that returns the divional round winners'''
        
        # American League 1 vs 4/5 matchup
        if 4 in self.al:                                                    # If 4th ranked team is still alive
            am1 = self.simulateMatchup(self.al[1], self.al[4])              # Simulate 1 v 4 matchup
        else:                                                               # If 5th ranked team is still alive
            am1 = self.simulateMatchup(self.al[1], self.al[5])              # Simulate 1 v 5 matchup
        value1 = list(self.al.keys())[list(self.al.values()).index(am1)]    # Get key of loser
        del self.al[value1]                                                 # Remove loser from playoffs
        
        # American League 2 vs 3/6 matchup
        if 3 in self.al:
            am2 = self.simulateMatchup(self.al[2], self.al[3])
        else:
            am2 = self.simulateMatchup(self.al[2], self.al[6])
        value2 = list(self.al.keys())[list(self.al.values()).index(am2)]
        del self.al[value2]
        
        # National League 1 vs 4/5 matchup
        if 4 in self.nl:
            am3 = self.simulateMatchup(self.nl[1], self.nl[4])
        else:
            am3 = self.simulateMatchup(self.nl[1], self.nl[5])
        value3 = list(self.nl.keys())[list(self.nl.values()).index(am3)]
        del self.nl[value3]
        
        # National League 2 vs 3/6 matchup
        if 3 in self.nl:
            am4 = self.simulateMatchup(self.nl[2], self.nl[3])
        else:
            am4 = self.simulateMatchup(self.nl[2], self.nl[6])
        value4 = list(self.nl.keys())[list(self.nl.values()).index(am4)]
        del self.nl[value4]
        
        return
    
    
    def championshipSeries(self):
        '''Function that returns the league championship winners'''
        
        # American League matchup
        alTeams = list(self.al.keys())                                              # Get list of keys of playoff teams left
        if alTeams[0] > alTeams[1]:                                                 # Find the higher ranked team
            am1 = self.simulateMatchup(self.al[alTeams[0]], self.al[alTeams[1]])    # Simulate matchup with higher ranked team input first
        else:
            am1 = self.simulateMatchup(self.al[alTeams[1]], self.al[alTeams[0]])
            value1 = list(self.al.keys())[list(self.al.values()).index(am1)]        # Get key of loser
            del self.al[value1]                                                     # Remove loser from playoffs
            
        # National League matchup
        nlTeams = list(self.nl.keys())
        if nlTeams[0] > nlTeams[1]:
            am2 = self.simulateMatchup(self.nl[nlTeams[0]], self.nl[nlTeams[1]])
        else:
            am2 = self.simulateMatchup(self.nl[nlTeams[1]], self.nl[nlTeams[0]])
            value2 = list(self.nl.keys())[list(self.nl.values()).index(am2)]
            del self.nl[value2]
        
        return
        
    
    def worldSeries(self):     
        '''Function that returns the world series champion'''
        
        alTeam = list(self.al.keys())       # Get AL team key
        nlTeam = list(self.nl.keys())       # Get NL team key
        
        if nlTeam[0] > alTeam[0]:                                                   # If NL team is stronger
            am = self.simulateMatchup(self.nl[nlTeam[0]], self.al[alTeam[0]])       # Simulate match with NL team input first
        else:                                                                       # Else input AL team first
            am = self.simulateMatchup(self.al[alTeam[0]], self.nl[nlTeam[0]])       # Get world series winner
        
        if am in self.nl.values():                                                  # If winner is in NL
            value = list(self.nl.keys())[list(self.nl.values()).index(am)]          # Get ranking from value
        else:                                                                       # Else get AL winner
            value = list(self.al.keys())[list(self.al.values()).index(am)]
            
        winner = []
        winner.append(value)
        winner.append(am[0])
        winner.append(am[1])
            
        return winner
    
def runSimulation(nl, al, trials = 2):
    '''Function that runs the playoff scenario a default 1,000,000 times.
    Track the world series winners and plot results'''
     
    champions = []
        
    for i in range(trials):
        b = Baseball(nl, al)
        champions.append(b.simulatePlayoffs())
            
    #fig, axs = plt.subplots()
    #axs[0].bar()
                      
    return champions
    
    
    
nationalLeague = {1: ['Dodgers', 0.91], 2: ['Braves', 0.82],
                  3: ['Cardinals', 0.75], 4: ['Mets', 0.71], 
                  5: ['Padres', 0.66], 6: ['Phillies', 0.73]} 

americanLeague = {1: ['Astros', 0.88], 2: ['Yankees', 0.87],
                  3: ['Guardians', 0.75], 4: ['Blue Jays', 0.72],
                  5: ['Mariners', 0.69], 6: ['Mariners', 0.66]} 
                  
                  
b = Baseball(nationalLeague, americanLeague)
c = Baseball(nationalLeague, americanLeague)
#b.wildCard()
#b.al
#b.nl
#b.divisionSeries()
#b.al
#b.nl
#b.championshipSeries()
#b.al
#b.nl
#b.worldSeries()
b.simulatePlayoffs()
c.simulatePlayoffs()
runSimulation(nationalLeague, americanLeague)



#winner = b.simulateOneGame(teamA, teamB)
#print("The {} are victorious".format(winner))
season = b.simulateSeason()
print(season)
