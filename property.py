#!/usr/bin/env python3

import re
import math

import networkx as nx

from pyjarowinkler.distance import get_jaro_distance

def __optimal_matching(nameparts1, nameparts2):
    graph = nx.Graph()
    graph.add_nodes_from(["1_{}".format(i) for i in nameparts1], bipartite=0)
    graph.add_nodes_from(["2_{}".format(i) for i in nameparts2], bipartite=1)

    for i in nameparts1:
        edges = [ ("1_{}".format(i), "2_{}".format(j), get_jaro_distance(i, j)) for j in nameparts2 ]
        edges = [ edge for edge in edges if edge[2] > 0 ]
        graph.add_weighted_edges_from(edges)

    pairings = nx.max_weight_matching(graph)
    result = []
    matched = []

    for pairing in pairings:
        match = { p.split("_")[0]: p.split("_")[1] for p in pairing }
        v1 = match["1"]
        v2 = match["2"]
        weight = graph[pairing[0]][pairing[1]]["weight"]
        result.append( (v1, v2, weight) )
        matched.append(v1)
        matched.append(v2)

    result += [ (namepart, None, 0) for namepart in nameparts1 if namepart not in matched]
    result += [ (namepart, None, 0) for namepart in nameparts2 if namepart not in matched]

    return result

def record_similarity( record1, record2, m=2 ):
    similarities = __optimal_matching(record1, record2)
    total_sim = sum( s[2]**m for s in similarities )
    total_sim = (total_sim/max(1, len(similarities)))**(1/m)

    return total_sim

class Property:
    
    def __init__(self, name):       
        self.name_str = name

        nameparts = self.name_str.split()
        self.nameparts = nameparts
        
    def similarity( self, landowner ):
        sim = record_similarity(self.nameparts, landowner.nameparts)
        return sim
