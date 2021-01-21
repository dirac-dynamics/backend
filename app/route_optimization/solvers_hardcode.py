# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:17:09 2021

@author: focke
"""
from __future__ import print_function

from .utils_osmnx import * 
from .solver_multi import simp_min_cost_flow
from .solver_single import simp_min_cost_flow, greedy_algo

from ortools.graph import pywrapgraph
import time
import os
import random as rng
#import multiprocessing as mp
import numpy as np
#print('test')
import osmnx as ox
import matplotlib.pyplot as plt
import copy
import networkx as nx

import json

ox.config(use_cache=True, log_console=True)

'''
#%%
def multisolver_osmnx(solv_dic):
    
    dic = solv_dic['dic']
    inter_dic = solv_dic['inter_dic']
    target_dic = solv_dic['target_dic']
    G = solv_dic['G']

    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Classical network flow solver:')
    print()

    
    optimal_routes_solv, cost_solver = simp_min_cost_flow(carrier_number,
                                        transportable_number,
                                        dic['weight_list'],
                                        dic['connection_list'],
                                        dic['connection_number'],
                                        np.array(transportables),
                                        np.array(targets),
                                        inter_dic,
                                        target_dic)
                                        

    #print(optimal_routes_solv)    
    
    plot_route_list = np.concatenate((dic['plot_route'], inter_dic['plot_route']))
    plot_connection_list = np.concatenate((dic['plot_start_end'], inter_dic['plot_start_end'])).tolist()
    
    mp.plot_assigned_routes(G, carriers, transportables, targets, optimal_routes_solv, plot_route_list, plot_connection_list, target_dic['route_list'])
    
    all_routes_coord, all_routes_node = get_coord_routes(G,get_route_start_end_node(optimal_routes_solv,carriers,targets,transportables),dic['route_list'],target_dic['route_list'],inter_dic['route_list'],carriers)

    all_routes_time, all_routes_length = get_routes_time_length(G,all_routes_node)

    return all_routes_coord, all_routes_time, all_routes_length
'''


#%%
def singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number):
    """
    dic = solv_dic['dic']
    G = solv_dic['G']

    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    """
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Classical network flow solver:')
    print()

    optimal_routes_solv, cost_solver = simp_min_cost_flow(carrier_number,
                                        transportable_number,
                                        weight_list,
                                        connection_list_single,
                                        connection_number)
    
    #coord_routes_solv = output_routes(G,optimal_routes_solv,dic)
    
    #print(optimal_routes_solv)
    #print(all_time)
    #print(all_length)
    
    coords = []
    times = []
    lengths = []
    
    for element in optimal_routes_solv:
        coords.append(all_coord_routes[(element[0]-1)*carrier_number+element[1]-1])
        times.append(all_time[(element[0]-1)*carrier_number+element[1]-1])
        lengths.append(all_length[(element[0]-1)*carrier_number+element[1]-1])
    
    #coord_routes_solv= optimal_routes_solv

    #sp.plot_assigned_routes(G, carriers, transportables, optimal_routes_solv, dic['route_list'], dic['end_list'], dic['carrier_number'])
    
    return coords, times, lengths


#%%
def greedy_singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list_2, start_end_list):
    """
    dic = solv_dic['dic']
    G = solv_dic['G']
    
    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    """
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Greedy 2 solver:')
    print()
    
    weight_list_2_copy = copy.deepcopy(weight_list_2)
    start_end_list_copy = copy.deepcopy(start_end_list)
    
    optimal_routes_greed, cost_greedy= greedy_algo(weight_list_2_copy,start_end_list_copy,carrier_number, transportable_number)
    
    #coord_routes_greed =  output_routes(G,optimal_routes_greed,dic)
    coords = []
    times = []
    lengths = []
    
    for element in optimal_routes_greed:
        coords.append(all_coord_routes[(element[0]-1)*carrier_number+element[1]-1])
        times.append(all_time[(element[0]-1)*carrier_number+element[1]-1])
        lengths.append(all_length[(element[0]-1)*carrier_number+element[1]-1])
    
    #sp.plot_assigned_routes(G, carriers, transportables, optimal_routes_greed, dic['route_list'], dic['end_list'], dic['carrier_number'])

    return coords, times, lengths

'''
#%%

carrier_list = []
transportable_list = []
target_list = []

for i in range(rng.randint(10,10)):
    carrier_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))
    
for i in range(rng.randint(10,10)):    
    transportable_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))
    target_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))
#%%
carrier_list=[(48.129752769107945, 11.633920245074599), (48.17047873070159, 11.603082230724248), (48.14381540814869, 11.667907089457689), (48.157319901798516, 11.49443898952296), (48.15825620312655, 11.652080661995884), (48.15763862974767, 11.477973326658901), (48.11493098637105, 11.548067508716473), (48.18731512075317, 11.496868530419107), (48.190834582828706, 11.655388050444897), (48.160687246423705, 11.629874578282955)]
transportable_list=[(48.17977205349469, 11.675124253602606), (48.14795941900202, 11.628119831786826), (48.14166350755995, 11.65906539320436), (48.15999276074108, 11.540107109989), (48.13618853750969, 11.520402166764363), (48.16625648132125, 11.647085718140074), (48.15553867079467, 11.662042471944243), (48.14230829028947, 11.605450008848473), (48.1459378773055, 11.494065399447209), (48.1897695827536, 11.641544613253666)]
target_list = [(48.19028348830723, 11.615346030613956), (48.124016664796514, 11.627555666747382), (48.154021979313974, 11.662788957888983), (48.09726570006666, 11.530032723460545), (48.151663807186914, 11.593862358444369), (48.13017213933091, 11.624845373953026), (48.11941156323218, 11.508588449581357), (48.17663960770297, 11.570890592909363), (48.14359633138411, 11.491297184077672), (48.100630421828214, 11.652155523658816)]

#%%
carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number, weight_list_2, start_end_list = stp.setup_osmnx('munich_2', 48.143743 + 0.05, 48.143743 - 0.05, 11.575942 + 0.10, 11.575942 - 0.10, carrier_list, transportable_list, target_list, dead_ends=True)
output = [carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number, weight_list_2, start_end_list]
#output = stp.setup_osmnx('munich_2', 48.143743 + 0.05, 48.143743 - 0.05, 11.575942 + 0.10, 11.575942 - 0.10, carrier_list, transportable_list, target_list, dead_ends=True)
with open('setup_data.json', 'w') as outfile:
    json.dump(output, outfile)
#with open('deed.txt', 'a') as f:
#  f.write(str(setup_dic))
#%%
#print(str(setup_dic))

#print(carrier_list)
#print(transportable_list)
#print(target_list)
#%%
#print(multisolver_osmnx(setup_dic))
print(singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number))
print(greedy_singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list_2, start_end_list))

#%%
#print(setup_dic['dic']['weight_list'])
'''