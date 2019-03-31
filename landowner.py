#!/usr/bin/env python3

import re
import math

import networkx as nx

from pyjarowinkler.distance import get_jaro_distance
from config import HONORIFICS, TITLES, LOCATIONS, NORMALS

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

class Landowner:
    
    def __init__(self, name):       
        self.name_str = name
        corrected_name = re.sub(r"\s+", " ", " ".join(name.split(",", 1)[::-1]).strip())        
        self.labels = self.__generate_name_permutations(corrected_name)
        self.__transform_and_append(name, self.labels)

        nameparts = self.__apply_normalization_patterns(corrected_name)
        nameparts = self.__collapse_locations(nameparts)
        nameparts = self.__collapse_titles_honorifics(nameparts)
        nameparts = nameparts.split()
        
        if len(nameparts) > 1:
            self.surname = nameparts[-1]
            self.forename = nameparts[0]
        elif len(nameparts) > 0:
            self.surname = nameparts[0]
            self.forename = ""
        else:
            self.surname = self.forename = ""

        self.nameparts = nameparts

        self.location = ""
        for pattern in LOCATIONS:
            location = re.search(pattern, name)
            if location != None:
                self.location = location.group(0)[3:]
        
    def similarity( self, landowner ):
        sim = record_similarity(self.nameparts, landowner.nameparts)
        return sim

    def __generate_name_permutations(self, name):
        permutations = []
        
        # self.__transform_and_append(name, permutations)
        
        self.__transform_and_append(
            name, 
            permutations, 
            transf = lambda x: re.sub(r"\s+", " ", " ".join(x.split(",", 1)[::-1]).strip())
        )

        for perm in permutations:
            self.__transform_and_append(
                perm, 
                permutations, 
                transf = self.__apply_normalization_patterns
            )   

        for perm in permutations:
            self.__transform_and_append(
                perm, 
                permutations, 
                transf = self.__collapse_titles_honorifics
            )

        for perm in permutations:
            # collapse locations "Sir John of Kinsale" to "John"
            self.__transform_and_append(
                perm,
                permutations,
                transf = self.__collapse_locations
            )

        # Filter permutations that are comprised only of titles or locations
        permutations = [ permutation for permutation in permutations if not self.__matches_pattern_set(permutation, HONORIFICS) ]
        permutations = [ permutation for permutation in permutations if not self.__matches_pattern_set(permutation, TITLES) ]
        permutations = [ permutation for permutation in permutations if not self.__matches_pattern_set(permutation, LOCATIONS) ]

        return permutations

    def __transform_and_append(self, label, permutations, transf = lambda x: x):
        transformation = transf(label)
        if transformation not in permutations and len(transformation) > 0:
            permutations.append(transformation)

    def __apply_normalization_patterns( self, name ):
        
        for pattern, sub in NORMALS:            
            newname = re.sub(pattern, sub, name)
            #if name != newname:
            #   self.__info("Normalizing '{}' : '{}'".format(name, newname))
            name = newname

        return name

    def __collapse_locations( self, name ):
        for pattern in LOCATIONS:           
            name = re.sub("\s+", " ", re.sub(pattern, "", name)).strip()

        return name

    def __collapse_titles_honorifics( self, name ):
        nameparts = name.split(" ")
        nameparts = [ part for part in nameparts if not self.__matches_pattern_set(part, HONORIFICS) ]
        nameparts = [ part for part in nameparts if not self.__matches_pattern_set(part, TITLES) ]
        return " ".join(nameparts)

    def __matches_pattern_set( self, term, pattern_set ):
        for pattern in pattern_set:
            if re.match(pattern, term, re.IGNORECASE):
                return True
        return False

    def __debug(self, msg):
        logging.debug("{:>4}: {}".format(self.identifier, msg))

    def __info(self, msg):
        logging.info("{:>4}: {}".format(self.identifier, msg))

    def __warn(self, msg):
        logging.warn("{:>4}: {}".format(self.identifier, msg))

    def __error(self, msg):
        logging.error("{:>4}: {}".format(self.identifier, msg))
