## Function for calculating the probability that a team wins/loses/ties.
def DoublePoissonProbabilities(teamOa, teamDv, oppOa, oppDv, allowTies=True):
    '''
    Inputs
    teamOa: team 1's offensive strength
    teamDv: team 1's defensive vulnerability
    oppOa : team 2's offensive strength
    oppDv : team 2's defensive vulnerability
    Outputs: 
    (pWin, pLoss, pTie) - probability that team 1 wins, loses, or ties.
    '''
    from math import factorial, exp
    from scipy.stats import poisson
    scoreRange = range(0, 21)   # simulates under the assumption that each team scores less than or equal to 20 runs.
    pWin = 0
    pLoss = 0
    pTie = 0
    teamMu = teamOa * oppDv
    oppMu = oppOa * teamDv
    for teamScore in scoreRange:
        for oppScore in scoreRange:
            if teamScore > oppScore:
                pWin += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore < oppScore:
                pLoss += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore == oppScore:
                pTie += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
    if allowTies == True:
        return (pWin, pLoss, pTie)
    if allowTies == False:
        # Keep this tie-dropping formula. Replace with newPWin = pWin + (0.5)*(pTie) if XI games are predicted incorrectly.
        newPWin = pWin/(pWin + pLoss)
        newPLoss = pLoss/(pWin + pLoss)
        return (newPWin, newPLoss, 0)

def DPConfStrengthProbabilities(teamOa, teamDv, oppOa, oppDv, teamConfOa, teamConfDv, oppConfOa, oppConfDv, allowTies=True):
    '''
    Inputs:
    teamOa : team 1's offensive strength (average number of runs scored over season)
    teamDv : team 1's defensive vulnerability (average number of runs against over season)
    oppOa  : team 2's offensive strength (average number of runs scored over season)
    oppDv  : team 2's defensive vulnerability (average number of runs against over season)
    teamConfOa : offensive strength of team 1's conference (average number of runs scored by conference's teams in nonconf games)
    teamConfDv : def vulnerability of team 1's conference (average number of runs against by conference's teams in nonconf games)
    oppConfOa  : offensive strength of team 2's conference (average number of runs scored by conference's teams in nonconf games)
    oppConfDv  : def vulnerability of team 2's conference (average number of runs against by conference's teams in nonconf games)
    allowTies  : default=True (boolean)
    Assumption:
    Neither team will score more than 20 runs.
    Outputs: 
    (pWin, pLoss, pTie) - probability that team 1 wins, loses, or ties (against team 2)
    '''
    from math import factorial, exp
    from scipy.stats import poisson
    scoreRange = range(0, 21)   # simulates under the assumption that each team scores less than or equal to 20 runs.
    pWin = 0
    pLoss = 0
    pTie = 0
    teamMu = teamOa * oppDv * teamConfOa * oppConfDv
    oppMu = oppOa * teamDv * oppConfOa * teamConfDv
    for teamScore in scoreRange:
        for oppScore in scoreRange:
            if teamScore > oppScore:
                pWin += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore < oppScore:
                pLoss += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore == oppScore:
                pTie += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
    if allowTies == True:
        return (pWin, pLoss, pTie)
    if allowTies == False:
        # Keep this tie-dropping formula. Replace with newPWin = pWin + (0.5)*(pTie) if XI games are predicted incorrectly.
        newPWin = pWin/(pWin + pLoss)
        newPLoss = pLoss/(pWin + pLoss)
        return (newPWin, newPLoss, 0)

def DoublePoissonSimpleStrengths(teamMu, oppMu, allowTies=True):
    '''
    Use this function when the mu values are calculated outside the function and all we need is a set of probabilities.
    Inputs:
    teamMu - float value for the mean value of the team under study's Poisson process.
    oppMu - float value for the mean value of the team's opponent's Poisson process.
    allowTies - Boolean (default True) on whether or not to allow ties. If not, we use a method of relative probabilities.
    Outputs:
    (pWin, pLoss, pTie) - (probability that team under study wins, loses, ties)
    '''
    from math import factorial, exp
    from scipy.stats import poisson
    scoreRange = range(0, 21)   # simulates under the assumption that each team scores less than or equal to 20 runs.
    pWin = 0
    pLoss = 0
    pTie = 0
    for teamScore in scoreRange:
        for oppScore in scoreRange:
            if teamScore > oppScore:
                pWin += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore < oppScore:
                pLoss += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
            if teamScore == oppScore:
                pTie += (poisson.pmf(k=teamScore, mu=teamMu))*(poisson.pmf(k=oppScore, mu=oppMu))
    if allowTies == True:
        return (pWin, pLoss, pTie)
    if allowTies == False:
        # Keep this tie-dropping formula. Replace with newPWin = pWin + (0.5)*(pTie) if XI games are predicted incorrectly.
        newPWin = pWin/(pWin + pLoss)
        newPLoss = pLoss/(pWin + pLoss)
        return (newPWin, newPLoss, 0)
    
# Function to simulate a game
def SimulateDoublePoisson(pWin):
    '''
    Input:
    pWin : probability that a given team wins
    Output:
    1 if given team wins game, 0 if given team loses game
    '''
    import numpy as np
    randomFloat = np.random.uniform(low=0, high=1)
    if pWin <= randomFloat:
        return 0
    else:
        return 1

# Function to simulate a game and return a UID value
def SimDoublePoissonUID(pWin, teamUID, oppUID):
    '''
    Input:
    pWin : probability that team with TeamUID wins
    TeamUID, OppUID
    Output:
    (UID of winning team, UID of losing team)
    '''
    import numpy as np
    randomFloat = np.random.uniform(low=0, high=1)
    if pWin <= randomFloat:
        return (oppUID, teamUID)
    else:
        return (teamUID, oppUID)

# Function to simulate a four-team double elimination tournament
def SimulateFourTeamDE(probDF, team1, team2, team3, team4):
    '''
    Input:
    probDF: DF of win probabilities where (i, j) entry is the probability that team i beats team j
    team1 : UID of 1-seeded team
    team2 : UID of 2-seeded team
    team3 : UID of 3-seeded team
    team4 : UID of 4-seeded team
    Output:
    List of the following format [winner, runner-up, 1-2 team, 0-2 team]
    '''
    # Simulate two 0-0 games
    (game1Winner, game1Loser) = SimDoublePoissonUID(probDF.loc[team1, team4], team1, team4)
    (game2Winner, game2Loser) = SimDoublePoissonUID(probDF.loc[team2, team3], team2, team3)
    # Simulate 0-1 vs. 0-1 elimination game; game3Loser = 0-2 team
    (game3Winner, game3Loser) = SimDoublePoissonUID(probDF.loc[game1Loser, game2Loser], game1Loser, game2Loser)
    # Simulate 1-0 vs. 1-0 game
    (game4Winner, game4Loser) = SimDoublePoissonUID(probDF.loc[game1Winner, game2Winner], game1Winner, game2Winner)
    # Simulate 1-1 vs. 1-1 game
    (game5Winner, game5Loser) = SimDoublePoissonUID(probDF.loc[game3Winner, game4Loser], game3Winner, game4Loser)
    # Simulate 2-0 vs. 2-1 game
    (game6Winner, game6Loser) = SimDoublePoissonUID(probDF.loc[game4Winner, game5Winner], game4Winner, game5Winner)
    if game6Winner == game5Winner:
        # If-needed game
        (game7Winner, game7Loser) = SimDoublePoissonUID(probDF.loc[game6Winner, game6Loser], game6Winner, game6Loser)
        return [game7Winner, game7Loser, game5Loser, game3Loser]
    else:
        return [game6Winner, game6Loser, game5Loser, game3Loser]