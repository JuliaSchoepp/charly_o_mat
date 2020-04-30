#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:51:22 2020

@author: juliaschopp
"""

# Simulate full round of finals
import pandas as pd
from itertools import permutations
import time
from combined import *

# --- Competitor and results variables ---

competitors = ['Mori', 'Condie', 'Rakovec', 'Kaplina', 'Krampel', 'Rogora',\
             'Charnoudie', 'Ito']
result_dict = {y:x for x,y in dict(enumerate(competitors)).items()}
    
speed_results = {'Mori': 8,
 'Condie': 2,
 'Rakovec': 6,
 'Kaplina': 1,
 'Krampel': 7,
 'Rogora': 5,
 'Charnoudie': 3,
 'Ito': 4}

boulder_results = {'Mori': 2,
 'Condie': 6,
 'Rakovec': 3,
 'Kaplina': 8,
 'Krampel': 7,
 'Rogora': 4,
 'Charnoudie': 5,
 'Ito': 1}

lead_results = {'Mori': 3,
 'Condie': 7,
 'Rakovec': 2,
 'Kaplina': 8,
 'Krampel': 1,
 'Rogora': 4,
 'Charnoudie': 2,
 'Ito': 6} 

# --- Model leaderboards

empty_leaderboard = create_leaderboard(competitors) 

ranking_after_speed = update_discipline('Speed', speed_results, empty_leaderboard)

ranking_after_boulder = update_discipline('Boulder', boulder_results, ranking_after_speed)

ranking_after_lead = update_discipline('Lead', lead_results, ranking_after_boulder)


# --- Create scenarios and calculate probabilities

given = {} 

athletes = ('Mori', 'Rakovec')

m1 = time.perf_counter()

scenarios = get_all_possible_rankings(ranking_after_boulder)

m2 = time.perf_counter()

(scenarios_ok, percentage, necessary_positions_mean, necessary_positions_max) = \
  still_possible(scenarios, "Condie", 1) 

m3 = time.perf_counter()
  
(test_scenarios, test_percentage, test_necessary_positions_mean, max_position) = \
better_than_possible(scenarios, athletes)  

m4 = time.perf_counter()

print("A random scenario: ", scenarios[7])
print("Necessary_positions_mean for Condie to win: ", necessary_positions_mean)
print("Probability that Mori places in front of Rakovec: ", test_percentage)
print("Time to calc scenarios: ", int((m2-m1)//60), "min", int((m2-m1)%60), "s")
print("Time to calc still_possible: ", int((m3-m2)/60), "min", int((m3-m2)%60), "s")
print("Time to calculate better_than: ", int((m4-m3)/60), "min", int((m4-m3)%60), "s")
print("Total runtime: ", int((m4-m1)//60), "min", int((m4-m1)%60), "s")
