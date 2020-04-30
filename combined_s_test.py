#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:59:23 2020

@author: juliaschopp
"""

# Simulate test comp with 4 athletes
import pandas as pd
from itertools import permutations

from combined import *

# --- Competitor and results variables ---

competitors = ['Mori', 'Condie', 'Rakovec', 'Kaplina']
result_dict = {y:x for x,y in dict(enumerate(competitors)).items()}

speed_results = speed_results = {'Mori': 4,
 'Condie': 2,
 'Rakovec': 3,
 'Kaplina': 1}

boulder_results = {'Mori': 3,
 'Condie': 1,
 'Rakovec': 2,
 'Kaplina': 4}

lead_results = {'Mori': 1,
 'Condie': 2,
 'Rakovec': 3,
 'Kaplina': 4}

# --- Model leaderboards

empty_leaderboard = create_leaderboard(competitors) 

ranking_after_speed = update_discipline('Speed', speed_results, empty_leaderboard)

ranking_after_boulder = update_discipline('Boulder', boulder_results, ranking_after_speed)

ranking_after_lead = update_discipline('Lead', lead_results, ranking_after_boulder)


# --- Create scenarios and calculate probabilities

given = {'Kaplina': 4} 

athletes = ('Mori', 'Rakovec')

scenarios = get_all_possible_rankings(ranking_after_boulder)

(scenarios_ok, percentage, necessary_positions_mean, necessary_positions_max) = \
  still_possible(scenarios, "Condie", 3, given) 
  
(test_scenarios, test_percentage, test_necessary_positions_mean, max_position) = \
better_than_possible(scenarios, athletes)  

print("necessary_positions_mean: ", necessary_positions_mean)
print("test_percentage: ", test_percentage)

