# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 16:00:33 2020

@author: focke
"""
from __future__ import print_function
from ortools.graph import pywrapgraph
import time
import os
import random as rng
import multiprocessing as mp
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import copy
ox.config(use_cache=True, log_console=True)
ox.__version__
import networkx as nx
from multiprocessing import Pool, cpu_count

start_time = time.process_time()

#download and build graph
G = ox.graph_from_place({'state':'NRW','country':'Germany'},custom_filter='["highway"~"motorway|trunk|primary|secondary"]')
ox.plot_graph(G)
#G = ox.graph.graph_from_point([50.77543745,6.083803247551902],dist=3000,network_type='drive')

#claculate and add traveltimes to edges
speed_dict = {'motorway' : 80, 'trunk' : 80, 'primary' : 70, 'secondary' : 50, 'motorway_link' : 50, 'trunk_link' : 50, 'primary_link' : 50, 'secondary_link' : 50}

ox.speed.add_edge_speeds(G, hwy_speeds=speed_dict, fallback=50, precision=1)
ox.speed.add_edge_travel_times(G, precision=1)

#build new graph without dead ends
G_proj = ox.project_graph(G)
G2 = ox.consolidate_intersections(G_proj, rebuild_graph=True, tolerance=1, dead_ends=False)
ox.plot_graph(G2)

G2 = nx.convert_node_labels_to_integers(G2)
node_info = G2.nodes

print("Time =", time.process_time() - start_time, "seconds")
#%%



start_time = time.process_time()
#number of entities
carrier_number = rng.randint(20,40)
transportable_number = rng.randint(20,40)

print(carrier_number, ' Carriers')
print(transportable_number, ' Transportables')

#functions to select random nodes
def create_random_node_points_2(number,Graph):
    node_list=[]
    for i in range(number):
        node_list.append(rng.randint(0,len(list(node_info))-1))
    return node_list


#create random carriers and transportables
carriers = create_random_node_points_2(carrier_number,G2)
transportables = create_random_node_points_2(transportable_number,G2)



#find paths from carriers to transportables
node_info = node_info
route_list = []
weight_list = []
weight_list_2 = []

connection_list = []
connection_number = []
end_list = []
start_end_list =[]

for i in range(len(carriers)):
    ways_to_transportables = []
    weights_to_transportables = []
    start_to_end = []
    end_numbers = []
    counter=0
    for j in range(len(transportables)):
        #if (ox.distance.euclidean_dist_vec(node_info[carriers[i]]['y'],node_info[carriers[i]]['x'],
        #                                   node_info[transportables[j]]['y'],node_info[transportables[j]]['x'])) <= 1e+05:#euclidian distance is unit of x,y coords
            #print(ox.distance.euclidean_dist_vec(node_info[carriers[i]]['y'],node_info[carriers[i]]['x'],
            #                               node_info[transportables[j]]['y'],node_info[transportables[j]]['x']))
            connection_list.append(j+1+carrier_number)
            end_numbers.append(j)
            start_to_end.append([i,j])
            way = ox.shortest_path(G2, carriers[i], transportables[j], weight='travel_time')
            ways_to_transportables.append(way)
            way_weight=0
            for k in range(len(way)-1):
                #print(G2[way[k]][way[k+1]])
                way_weight += (G2[way[k]][way[k+1]][0]['travel_time'])
                #print(G2[way[k]][way[k+1]])
            weight_list.append(way_weight)
            weights_to_transportables.append(way_weight)
            counter+=1
    
    end_list.append(end_numbers)
    connection_number.append(counter)
    route_list.append(ways_to_transportables)
    weight_list_2.append(weights_to_transportables)
    start_end_list.append(start_to_end)
    

print("Time =", time.process_time() - start_time, "seconds")

#%%

start_time = time.process_time()

def solver(n_carrier,n_transportables,weights,connections,n_connections):
  """Solving an Assignment Problem with MinCostFlow"""

  # Instantiate a SimpleMinCostFlow solver.
  min_cost_flow = pywrapgraph.SimpleMinCostFlow()

  # Define the directed graph for the flow.
  start_nodes = np.zeros(n_carrier)
  for i in range(n_carrier):
      start_nodes = np.concatenate((start_nodes , np.full(n_connections[i],i+1)))
  start_nodes = np.concatenate((start_nodes , np.linspace(n_carrier+1,n_carrier+n_transportables,n_transportables)))
  
  end_nodes = np.linspace(1,n_carrier,n_carrier)
  end_nodes = np.concatenate((end_nodes , connections))
  end_nodes = np.concatenate((end_nodes , np.full(n_transportables,n_carrier+n_transportables+1)))
      
  capacities =np.zeros(n_carrier+sum(n_connections)+n_transportables)+1

  costs = np.concatenate((np.zeros(n_carrier), weight_list, np.zeros(n_transportables)))

  start_nodes = start_nodes.astype(int)
  end_nodes = end_nodes.astype(int)
  capacities = capacities.astype(int)
  costs = costs.astype(int)
  
  start_nodes = start_nodes.tolist()
  end_nodes = end_nodes.tolist()
  capacities = capacities.tolist()
  costs = costs.tolist()

  source = 0
  sink = n_carrier+n_transportables+1
  tasks = n_transportables
  
  supplies =np.concatenate(([min(n_carrier,n_transportables)], np.zeros(n_carrier+n_transportables),[-min(n_carrier,n_transportables)]))
  supplies = supplies.astype(int)
  supplies = supplies.tolist()

  # Add each arc.
  for i in range(len(start_nodes)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],capacities[i], costs[i])
  # Add node supplies.

  for i in range(len(supplies)):
    min_cost_flow.SetNodeSupply(i, supplies[i])

  # Find the minimum cost flow between node 0 and node 10.
  output = []
  if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
    print('Total cost = ', min_cost_flow.OptimalCost())
    print()
    for arc in range(min_cost_flow.NumArcs()):

      # Can ignore arcs leading out of source or into sink.
      if min_cost_flow.Tail(arc)!=source and min_cost_flow.Head(arc)!=sink:

        # Arcs in the solution have a flow value of 1. Their start and end nodes
        # give an assignment of worker to task.

        if min_cost_flow.Flow(arc) > 0:
          print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                min_cost_flow.Tail(arc),
                min_cost_flow.Head(arc)-n_carrier,
                min_cost_flow.UnitCost(arc)))
          output.append([min_cost_flow.Tail(arc),min_cost_flow.Head(arc)-n_carrier])
  else:
    print('There was an issue with the min cost flow input.')
  
  return output



def greedy_algo(weights, ends, car_num, trans_num):
    overall_cost = 0
    output = []
    for i in range(min([car_num,trans_num])):
        picked_index = weights[i].index(min(weights[i]))
        picked_end =  ends[i][picked_index]
        overall_cost += weights[i][picked_index]
        output.append([i+1,picked_end+1])
        print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                i+1,
                picked_end+1,
                weights[i][picked_index]))
        for j in range(len(ends)):
            if picked_end in ends[j]:
                index=ends[j].index(picked_end)
                del ends[j][index]
                del weights[j][index]
    print()
    print('Total cost = ',overall_cost)
    return output



def greedy_algo_2(weights, connects, car_num, trans_num):
    overall_cost = 0
    output = []
    for i in range(min([car_num,trans_num])):
        zipped = zip(weights, connects)
        new_zipped = sorted(zipped)
        weights,connects = zip(*new_zipped)
        weights =list(weights)
        connects =list(connects)
        picked_index = weights[0].index(min(weights[0]))
        picked_connect =  connects[0][picked_index]
        overall_cost += weights[0][picked_index]
        output.append([picked_connect[0]+1,picked_connect[1]+1])
        print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                picked_connect[0]+1,
                picked_connect[1]+1,
                weights[0][picked_index]))
        for j in range(len(connects)):
            for k in range(len(connects[j])):
                if picked_connect[1] == connects[j][k][1]:
                    del connects[j][k]
                    del weights[j][k]
                    break
        del connects[0]
        del weights[0]
    print()
    print('Total cost = ',overall_cost)
    return output



def plot_assigned_routes(Graph,car,trans,opt,route_l,end_l,car_num):
    nc=[]
    ns=[]
    for node in Graph.nodes():
        if node in car:
            nc.append('r')
            ns.append(80)
        elif node in trans:
            nc.append('g')
            ns.append(80)
        else:
            nc.append('w')
            ns.append(0)
        
    routes_to_plot = []
    for element in opt:
        routes_to_plot.append(route_l[element[0]-1][end_l[element[0]-1].index(element[1]-1)])

    ox.plot.plot_graph_routes(G2,routes_to_plot,route_colors='w', show=True, close=False, node_color=nc, node_size=ns)






  
optimal_routes=solver(carrier_number,transportable_number,weight_list,connection_list,connection_number)
print()
print("Time =", time.process_time() - start_time, "seconds")
print()
#print(optimal_routes)
start_time = time.process_time()

#plotting routine
color_list=['r','b','g','y']
#color_list=['C00','C01','C02','C03','C04','C05']

plot_assigned_routes(G2, carriers, transportables, optimal_routes, route_list, end_list, carrier_number)

print()
print("Time =", time.process_time() - start_time, "seconds")
print()
start_time = time.process_time()


weight_list_2_copy = copy.deepcopy(weight_list_2)
end_list_copy = copy.deepcopy(end_list)

optimal_routes=greedy_algo(weight_list_2_copy,end_list_copy,carrier_number, transportable_number)
print()
print("Time =", time.process_time() - start_time, "seconds")
print()
start_time = time.process_time()

plot_assigned_routes(G2, carriers, transportables, optimal_routes, route_list, end_list, carrier_number)

print()
print("Time =", time.process_time() - start_time, "seconds")
print()
start_time = time.process_time()


weight_list_2_copy = copy.deepcopy(weight_list_2)
start_end_list_copy = copy.deepcopy(start_end_list)

optimal_routes=greedy_algo_2(weight_list_2_copy,start_end_list_copy,carrier_number, transportable_number)
print()
print("Time =", time.process_time() - start_time, "seconds")
print()
start_time = time.process_time()

plot_assigned_routes(G2, carriers, transportables, optimal_routes, route_list, end_list, carrier_number)

print()
print("Time =", time.process_time() - start_time, "seconds")


