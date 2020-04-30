#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:19:32 2019

@author: juliaschopp
"""

import pandas as pd
from itertools import permutations


def create_leaderboard(competitors):
    """
    Input: a list of competitors (str)
    Output: An empty leaderboard (pd Data Frame) with all rankings set to 1.
    """
    leaderboard = pd.DataFrame()
    possible_placements = [(i+1) for i in list(range(len(competitors)))]
    disciplines = ['Speed', 'Boulder', 'Lead']
    leaderboard['Name'] = competitors
    for discipline in disciplines:
        leaderboard[discipline] = [1 for i in possible_placements]
    leaderboard['Score'] = leaderboard.Speed * leaderboard.Boulder * leaderboard.Lead
    leaderboard['Rank'] = leaderboard['Score'].rank(method='min')
    leaderboard = leaderboard.set_index('Rank')
    return leaderboard

def update_ranking(leaderboard):
    """
    Input: the current leaderboard (pd df)
    Output: the current leaderboard with scores and rankings updated (pd df)
    """
    leaderboard['Score'] = leaderboard.Speed * leaderboard.Boulder * leaderboard.Lead
    leaderboard['Rank'] = leaderboard['Score'].rank(method='min')
    leaderboard = leaderboard.set_index('Rank')
    leaderboard.sort_index(inplace=True)
    return leaderboard

def update_discipline(discipline, results, leaderboard):
    """
    Input: The discipline (str), the results of the discipline (dict of format
    name (str): ranking (int)),
    the leaderboard that is to be updated (pd Data Frame)
    Output: The new ranking (pd Data Frame)
    """
    leaderboard = leaderboard.copy()
    for (key, value) in results.items():
        leaderboard.loc[leaderboard.Name == key, discipline] = value
    new_ranking = update_ranking(leaderboard)
    return new_ranking

def get_all_possible_rankings(ranking_after_boulder, given={}):
    """
    Brute force aproach to calculating all possible outcomes after second 
    discipline. Forms the basis of following analysis and calculation of 
    probabilities
    ---
    Inputs: 
    ranking after boulder (pd df); 
    optional: a dict of assumed results in Lead {str: int}, default empty
    ---
    Output: 
    A list of pd Data Frames with all scenarios of final rankings
    with every possible permutation of Lead Results (taking into account the 
    results in given)
    """
    competitors = ranking_after_boulder.Name.tolist() # get a list with competitor names
    possible_placements = [(i+1) for i in list(range(len(competitors)))]
    scenarios = []
    competitors = list(set(competitors)-set(given.keys())) # remove athletes and positions in "given"
    possible_placements = list(set(possible_placements)-set(given.values()))
    for i in permutations(possible_placements): # create all possible permutations of ranks
        x = {n:p for (n,p) in zip(competitors,i)} # create a result table based on permutation
        x ={**x, **given} # add the results from the given dict to those created by permutation
        leaderboard = update_discipline('Lead', x, ranking_after_boulder) # update the leaderboard
        scenarios.append(leaderboard) # add leaderboard to the list of scenarios
    return scenarios

def still_possible(scenarios, athlete, position, given={}):
    """
    Tests if a certain position or better is still achievable for one athlete
    after boulder
    ---
    Input: 
    - scenarios: A list of all possible rankings
    - athlete: name of the competitor/athlete (str) to be tested
    - position: which is to be tested (int)
    - given (optional): A dict of assumed positions, e.g. because someone has
        disqualified or testing assumptions (default: empty)
   ---
    Output: 
    - scenarios_ok: list of all possible scenarios in which athlete places equal or
        better than the input rank (list of pd dfs)
    - percentage: percentage of scenarios for which this is the case
    - necessary_positoins_mean: Mean position in lead that was required 
        for athlete to achieve input rank
    - necessary_positions_max: Worst position in lead which still allowed the
        athlete to reach input position
    """
    scenarios_ok = []
    necessary_positions = [] 
    for i in scenarios:
        if (i.loc[i.Name == athlete].index <= position) \
            and sum([(i.loc[i.Name == k].Lead == v).all() for k,v in given.items()]) == len(given):
            #test if scenario fulfills: 1) athlete achieves pos 2) given positions apply
            scenarios_ok.append(i)
            necessary_positions.append(int(i.loc[i.Name == athlete, 'Lead']))   
    percentage = 100 * (len(scenarios_ok) / len(scenarios))
    if len(necessary_positions) > 0:
        necessary_positions_mean = round(sum(necessary_positions)/len(necessary_positions), 4)
        necessary_positions_max = max(necessary_positions)
    else:
       necessary_positions_mean = "not possible"
       necessary_positions_max = "not possible"
    return (scenarios_ok, percentage, necessary_positions_mean, necessary_positions_max)


def better_than_possible(scenarios, athletes):
    """
    Tests if it is still possible for one athlete to place in front of another
    ---
    Parameters
    ----------
    scenarios : list of all possible scenarios
    athletes : Tuple or list with the name of two athletes (str), with the pos 0
    the one to come up in front of pos 2
    
    Returns
    -------
    scenarios_ok : A list of scenarios for which the first athlete positions better
        or equal than the second.
    percentage : percentage of scenarios for which the condition holds
    necessary_positions_mean : mean of the position which athlete 1 has to achieve
        to end up in front of the second one
    necessary_positions_max : worst possible position that athl. 1 can end up in to
        land in front of athlete 2
    """
    scenarios_ok = []
    necessary_positions = []
    for i in scenarios:
        if i.loc[i.Name == athletes[0]].index <= i.loc[i.Name == athletes[1]].index:
            scenarios_ok.append(i)
            necessary_positions.append(int(i.loc[i.Name == athletes[0], 'Lead']))
    percentage = 100 * (len(scenarios_ok) / len(scenarios))        
    if len(necessary_positions) > 0:
        necessary_positions_mean = round(sum(necessary_positions)/len(necessary_positions), 4)
        necessary_positions_max = max(necessary_positions)
    else:
       necessary_positions_mean = "not possible"
       necessary_positions_max = "not possible"
    return (scenarios_ok, percentage, necessary_positions_mean, necessary_positions_max)
    
    









     