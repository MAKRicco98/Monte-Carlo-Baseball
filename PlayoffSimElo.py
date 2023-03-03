
import numpy as np
import json
from collections import Counter
import matplotlib.pyplot as plt
import math
from copy import deepcopy

class PlayoffSimElo:

    def __init__(self, AL: dict, NL: dict) -> None:
        self.AL = AL
        self.NL = NL

        self.runningAL = deepcopy(self.AL)
        self.runningNL = deepcopy(self.NL)


        self.results = np.array([])


    def calculateProbability(self, homeTeamElo: int, awayTeamElo: int) -> float:
        '''
        - Calculating the win percentage of each team

        - homeTeamElo - Home team's Elo rating
        - awayTeamElo - Away team's Elo rating

        ** Home team is the higher seed
        '''
        # Home team gets a 24 pt pregame boost 
        homeTeamElo += 24

        homeTeamProb = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (awayTeamElo - homeTeamElo) / 400))
        awayTeamProb = 1 - homeTeamProb

        return homeTeamProb, awayTeamProb
    

    def adjustRating(self, currentRating: int, k: int, outcome: int, winProb: float) -> int:
        '''
        - k - K-factor
        - currentRating - Elo rating of team
        - outcome - 1 for win, 0 for loss
        - winProb - Probability of beating other team
        '''

        newRating = currentRating + (k * (outcome - winProb))
        return newRating
    

    def randWin(self, homeTeamProb: float, awayTeamProb: float) -> int:
        '''
        - Return True if home team wins and False if away team wins 
        '''
        return np.random.choice([True, False], p=[homeTeamProb, awayTeamProb])
    

    def simGame(self, higherSeed, lowerSeed, division):

        hSeedRank = higherSeed['rank']
        lSeedRank = lowerSeed['rank']

        # Will need to update the Elo for each team after each game
        # The winner of the wildcard will have their final elo returned and updated in the 'simPlayoff' dictionaries
        hSeedElo = higherSeed['Elo']
        lSeedElo = lowerSeed['Elo']
        
        if division == 'AL':
            homeTeamProb, awayTeamProb = self.calculateProbability(higherSeed['Elo'], lowerSeed['Elo'])         # Getting the probability of each team winning a game based on Elo
            homeTeamWins = self.randWin(homeTeamProb, awayTeamProb)                                             # Will return True if the home team wins the game

            if homeTeamWins:
                self.runningAL[hSeedRank]['Elo'] = self.adjustRating(currentRating=hSeedElo, k=4, outcome=1, winProb=homeTeamProb)      # After each game the elo rating will be updated
                self.runningAL[lSeedRank]['Elo'] = self.adjustRating(currentRating=lSeedElo, k=4, outcome=0, winProb=awayTeamProb)
                return homeTeamWins # True if home wins
            else:
                self.runningAL[hSeedRank]['Elo'] = self.adjustRating(currentRating=hSeedElo, k=4, outcome=0, winProb=homeTeamProb)      # After each game the elo rating will be updated
                self.runningAL[lSeedRank]['Elo'] = self.adjustRating(currentRating=lSeedElo, k=4, outcome=1, winProb=awayTeamProb)
                return homeTeamWins # False is away wins 

        elif division == 'NL':
            homeTeamProb, awayTeamProb = self.calculateProbability(higherSeed['Elo'], lowerSeed['Elo'])         # Getting the probability of each team winning a game based on Elo
            homeTeamWins = self.randWin(homeTeamProb, awayTeamProb)                                             # Will return True if the home team wins the game

            if homeTeamWins:
                self.runningNL[hSeedRank]['Elo'] = self.adjustRating(currentRating=hSeedElo, k=4, outcome=1, winProb=homeTeamProb)      # After each game the elo rating will be updated
                self.runningNL[lSeedRank]['Elo'] = self.adjustRating(currentRating=lSeedElo, k=4, outcome=0, winProb=awayTeamProb)
                return homeTeamWins # True if home wins
            else:
                self.runningNL[hSeedRank]['Elo'] = self.adjustRating(currentRating=hSeedElo, k=4, outcome=0, winProb=homeTeamProb)      # After each game the elo rating will be updated
                self.runningNL[lSeedRank]['Elo'] = self.adjustRating(currentRating=lSeedElo, k=4, outcome=1, winProb=awayTeamProb)
                return homeTeamWins # False is away wins 

        else:
            pass


    def wildcard(self, higherSeed, lowerSeed, division):
        '''
        - higherSeed will have homefiled advantage for all possible games (3 max for wildcard)
        '''
        hWins = 0
        lWins = 0

        # Best of 3 series
        # First team to 2 wins will stop
        while hWins < 2 or lWins < 2:
            homeTeamWins = self.simGame(higherSeed, lowerSeed, division)
            if homeTeamWins:
                hWins += 1
            else:
                lWins += 1


        higherSeedWinsSeries = True if hWins > lWins else False

        # first value is the losing team, second is the winning team, third is the winning team elo to be updated
        if higherSeedWinsSeries:
            return lowerSeed['rank'], higherSeed['rank']
        else:
            return higherSeed['rank'], lowerSeed['rank']
        

    def divisonal(self, higherSeed, lowerSeed, division):
        '''
        - The format for Divisional series is best of 5 and a 2-2-1 format
        - 2-2-1 -> The higher seed is the home team for the first two games and the last game if played; lower seed will be home team for games 3 and 4

        - hWins -> higherSeed wins
        - lWins -> lowerSeed wins
        '''

        hWins = 0
        lWins = 0

        while hWins < 3 or lWins < 3:
            for _ in range(2):
                homeTeamWins = self.simGame(higherSeed, lowerSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

            for _ in range(2):
                homeTeamWins = self.simGame(lowerSeed, higherSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

            for _ in range(1):
                homeTeamWins = self.simGame(higherSeed, lowerSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

        higherSeedWinsSeries = True if hWins > lWins else False

        # first value is the losing team, second is the winning team, third is the winning team elo to be updated
        if higherSeedWinsSeries:
            return lowerSeed['rank'], higherSeed['rank']
        else:
            return higherSeed['rank'], lowerSeed['rank']


    def championship(self, higherSeed, lowerSeed, division):

        hWins = 0
        lWins = 0

        while hWins < 5 or lWins < 5:
            for _ in range(2):
                homeTeamWins = self.simGame(higherSeed, lowerSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

            for _ in range(3):
                homeTeamWins = self.simGame(lowerSeed, higherSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

            for _ in range(2):
                homeTeamWins = self.simGame(higherSeed, lowerSeed, division)
                if homeTeamWins:
                    hWins += 1
                else:
                    lWins += 1

        higherSeedWinsSeries = True if hWins > lWins else False

        # first value is the losing team, second is the winning team, third is the winning team elo to be updated
        if higherSeedWinsSeries:
            return lowerSeed['rank'], higherSeed['rank']
        else:
            return higherSeed['rank'], lowerSeed['rank']


    def worldSeries(self, higherSeed, lowerSeed):
        hWins = 0
        lWins = 0

        hSeedElo = higherSeed['Elo']
        lSeedElo = lowerSeed['Elo']

        while hWins < 5 or lWins < 5:
            for _ in range(2):
                homeTeamProb, awayTeamProb = self.calculateProbability(higherSeed['Elo'], lowerSeed['Elo'])         # Getting the probability of each team winning a game based on Elo
                homeTeamWins = self.randWin(homeTeamProb, awayTeamProb)                                             # Will return True if the home team wins the game

                if homeTeamWins:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=1, winProb=homeTeamProb)      # After each game the elo rating will be updated
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=0, winProb=awayTeamProb)
                    hWins += 1
                else:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=0, winProb=homeTeamProb)
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=1, winProb=awayTeamProb)
                    lWins +=1

            for _ in range(3):
                homeTeamProb, awayTeamProb = self.calculateProbability(lowerSeed['Elo'], higherSeed['Elo'])         # Getting the probability of each team winning a game based on Elo
                homeTeamWins = self.randWin(homeTeamProb, awayTeamProb)                                             # Will return True if the home team wins the game

                if homeTeamWins:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=1, winProb=homeTeamProb)      # After each game the elo rating will be updated
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=0, winProb=awayTeamProb)
                    lWins += 1                                                                                      # Need to switch lWins and hWins here since lower seed has home field
                else:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=0, winProb=homeTeamProb)
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=1, winProb=awayTeamProb)
                    hWins +=1

            for _ in range(2):
                homeTeamProb, awayTeamProb = self.calculateProbability(higherSeed['Elo'], lowerSeed['Elo'])         # Getting the probability of each team winning a game based on Elo
                homeTeamWins = self.randWin(homeTeamProb, awayTeamProb)                                             # Will return True if the home team wins the game

                if homeTeamWins:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=1, winProb=homeTeamProb)      # After each game the elo rating will be updated
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=0, winProb=awayTeamProb)
                    hWins += 1
                else:
                    hSeedElo = self.adjustRating(currentRating=hSeedElo, k=4, outcome=0, winProb=homeTeamProb)
                    lSeedElo = self.adjustRating(currentRating=lSeedElo, k=4, outcome=1, winProb=awayTeamProb)
                    lWins +=1

        higherSeedWinsSeries = True if hWins > lWins else False

        # first value is the winning team, second is the winning team elo to be updated
        if higherSeedWinsSeries:
            return higherSeed['Team']
        else:
            return lowerSeed['Team']


    def simPlayoff(self):
        '''
        - Winners of 3/6 wildcard will play 2
        - Winners of 4/5 wildcard will play 1 

        - Winners of divisionals play each other in championship series

        - Winners of championship series play each other in world series
        '''
        
        # Simulating the 4 wilcard series
        loserRank, winnerAL3_6 = self.wildcard(self.runningAL[3], self.runningAL[6], division='AL')
        del self.runningAL[loserRank]

        loserRank, winnerAL4_5 = self.wildcard(self.runningAL[4], self.runningAL[5], division='AL')
        del self.runningAL[loserRank]

        loserRank, winnerNL3_6 = self.wildcard(self.runningNL[3], self.runningNL[6], division='NL')
        del self.runningNL[loserRank]

        loserRank, winnerNL4_5 = self.wildcard(self.runningNL[4], self.runningNL[5], division='NL')
        del self.runningNL[loserRank]


        # Simulating the 4 divisioal series
        loserRank, divWinnerAL1 = self.divisonal(self.runningAL[2], self.runningAL[winnerAL3_6], division='AL')
        del self.runningAL[loserRank]

        loserRank, divWinnerAL2 = self.divisonal(self.runningAL[1], self.runningAL[winnerAL4_5], division='AL')
        del self.runningAL[loserRank]

        loserRank, divWinnerNL1 = self.divisonal(self.runningNL[2], self.runningNL[winnerNL3_6], division='NL')
        del self.runningNL[loserRank]

        loserRank, divWinnerNL2 = self.divisonal(self.runningNL[1], self.runningNL[winnerNL4_5], division='NL')
        del self.runningNL[loserRank]


        # Simulating 2 championship series
        # Need to first see which team is the higher seed -> hiogher seed is home team first
        homeAL = min([divWinnerAL1, divWinnerAL2])
        awayAL = max([divWinnerAL1, divWinnerAL2])

        homeNL = min([divWinnerNL1, divWinnerNL2])
        awayNL = max([divWinnerNL1, divWinnerNL2])

        loserRank, ALChamp = self.championship(self.runningAL[homeAL], self.runningAL[awayAL], division='AL')
        del self.runningAL[loserRank]

        loserRank, NLChamp = self.championship(self.runningNL[homeNL], self.runningNL[awayNL], division='NL')
        del self.runningNL[loserRank]


        # Simulating World Series
        # Need to first see which team is the higher seed -> for the world series, the team with the 
        # better regualr season record is the home team
        if self.runningAL[ALChamp]['regWins'] > self.runningNL[NLChamp]['regWins']:
            champ= self.worldSeries(self.runningAL[ALChamp], self.runningNL[NLChamp])
        else:
            champ = self.worldSeries(self.runningNL[NLChamp], self.runningAL[ALChamp])

        # Clear running Elo for next trial
        self.runningAL = deepcopy(self.AL)
        self.runningNL = deepcopy(self.NL)

        return champ

        
    def runManySimulations(self, nTrials: int):
        for _ in range(nTrials):
            champ = self.simPlayoff()
            self.results = np.append(self.results, champ)

        counter = Counter(self.results)

        return counter





def main():

    AL = {
        1: {'Team': 'Astros', 'Elo': 1576, 'rank': 1, 'regWins': 106},
        2: {'Team': 'Yankees', 'Elo': 1576, 'rank': 2, 'regWins': 99},
        3: {'Team': 'Guardians', 'Elo': 1526, 'rank': 3, 'regWins': 92},
        4: {'Team': 'Blue Jays', 'Elo': 1550, 'rank': 4, 'regWins': 92},
        5: {'Team': 'Mariners', 'Elo': 1521, 'rank': 5, 'regWins': 90},
        6: {'Team': 'Rays', 'Elo': 1535, 'rank': 6, 'regWins': 86},
    }
    
    NL = {
        1: {'Team': 'Dodgers', 'Elo': 1619, 'rank': 1, 'regWins': 111},
        2: {'Team': 'Braves', 'Elo': 1585, 'rank': 2, 'regWins': 101},
        3: {'Team': 'Cardinals', 'Elo': 1526, 'rank': 3, 'regWins': 93},
        4: {'Team': 'Mets', 'Elo': 1549, 'rank': 4, 'regWins': 101},
        5: {'Team': 'Padres', 'Elo': 1524, 'rank': 5, 'regWins': 89},
        6: {'Team': 'Phillies', 'Elo': 1528, 'rank': 6, 'regWins': 87},
    }

    sim = PlayoffSimElo(AL, NL)
    cnts = sim.runManySimulations(100_000)
    plt.bar(cnts.keys(), cnts.values())
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Teams')
    plt.ylabel('# of World Series won')
    plt.show()
    # counts = sim.runManySimulations(1000)
    # print(counts)



if __name__ == '__main__':
    main()