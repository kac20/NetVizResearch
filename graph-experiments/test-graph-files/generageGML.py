from collections import defaultdict
import math
import os
import pathlib
import random
import matplotlib.pyplot as plt
import copy
import networkx as nx

def generateGraphGivenEdges(edges):
    """
    Inputs: edges - a set of edges of the form {(node1, node2): edge weight}

    Effects: 
        Returns a graph g of each node mapped to its neighbor mapped to the
            corresponding edge weight between them. 
            Ex: {node: {nbr: edge_weight between node, nbr}}
        Note: although this will disregard nodes with no edges, for our
            purposes, we would want to eliminate those nodes anyways/ it's not
            necessary info

    """
    g = defaultdict(lambda: defaultdict(int))

    for ((node1, node2), edge_weight) in edges.items():
        g[node1][node2] = edge_weight
        g[node2][node1] = edge_weight
    
    return g


def createGraphGMLString(edges):
    """
    Returns a string representing the graph specified by inputted edges in GML file format
    """
    nodes_strings = set({})
    edges_strings =[]
    for edge in edges.keys():
        edges_strings.append(edges[edge])
        (node1, node2) = edge
        nodes_strings.add("\t\tid " + str(node1) + "\n\t\tlabel " + str(node1))
        nodes_strings.add("\t\tid " + str(node2) + "\n\t\tlabel " + str(node2))

    graph = "graph ["
    # add the node information to the graph
    for node in nodes_strings:
        graph += "\n\tnode [\n" + node + "\n\t]"
    # add the edge information to the graph
    for edge in edges_strings:
        graph += "\n\tedge [\n" + edge + "\n\t]"
    graph += "\n]"

    return graph


def generateGMLFile(inputFileName, percentToGenerate, getPercentOfGraphFunc, simplifyThreshold = None):
    """
    Inputs:
        • inputFilePath, the name of a .txt file located in the "test-graph-data" directory
                        representing a graph graph where each line is an edge of the 
                        format: node1 node2 edge_weight

        • percentToGenerate, a decimal for the percent of the graph to copy over 
        • getPercentOfGraphFunc, a function (removeRandomEdges) for taking a percent of the graph
        • simplifyThreshold, an optional integer for the graph simplification threshold (could represent cluster size, node degree)
    
    Effects:
        • creates a .gml file representing the graph specified by inputFilePath
            in the directory "test-graph-GML-files"

    """

    os.chdir(os.path.dirname(os.path.abspath(__file__))+"/test-graph-data")
    inputFile = open(inputFileName, 'r')

    #Store the nodes and edges of the graph
    edges = {}
    nodeDegrees = defaultdict(int)

    ## PARSE THE GRAPH FROM THE INPUT FILE
    for line in inputFile.readlines():
        #parse the line (each line represents an edge)
        (node1, node2, edge_weight) = line.strip().split()

        #update node degree
        nodeDegrees[node1] += 1
        nodeDegrees[node2] += 1
        

        #store the GML string representation of the edge (saves us from extracting it later)
        edge_string = "\t\tsource " + str(node1) + "\n\t\ttarget " + str(node2) + "\n\t\tlabel " + str(edge_weight)
        edges[(node1, node2)] = edge_string
        
    inputFile.close()

    ## REMOVE UNNECESSARY NODES
    # simplify graph by node degree
    # edges = removeDegreeThresholdNodes(edges, simplifyThreshold, nodeDegrees)

    # simplify graph by connected component size
    edges = removeClusters(edges, simplifyThreshold)


    ## TAKE A PERCENT OF THE GRAPH

    # Method 1: Remove a random selection of nodes
    # Method 2: Remove a random selection of edges
    # Method 3: Approximate what the degreeThreshold should be to get the desired graph %
    edges = getPercentOfGraphFunc(edges, percentToGenerate)

    ## CREATE THE GRAPH STRING
    graph = createGraphGMLString(edges)

    ## RUN GRAPH DIAGNOSTICS FOR TESTING PURPOSES (COMMENT OUT)
    runGraphDiagnostics(edges)
    
    ## WRITE THE GRAPH TO THE OUTPUTFILE
    os.chdir("../test-graph-GML-files")
    outputFilePath = (inputFileName[:-4] + "_" + str(int(percentToGenerate*100))+ "_threshold_"+str(simplifyThreshold) + ".gml")
    outputFile = open(outputFilePath, 'w')
    outputFile.write(graph)
    outputFile.close()


# ===== HELPER FUNCTIONS FOR REMOVING UNNECESSARY NODES ======
def removeDegreeThresholdNodes(edges, nodeDegreeThreshold, nodeDegrees):
    edges_copy = copy.deepcopy(edges)
    if nodeDegreeThreshold != None:
        for node, degree in nodeDegrees.items():
            if degree < nodeDegreeThreshold:
                # Remove node from the edges list
                for edge in edges.keys():
                    if node in edge and edge in edges_copy:
                        del edges_copy[edge]
    return edges_copy

def removeClusters(G, clusterSizeThreshold):
    for component in list(nx.connected_components(G)):
        if len(component)< clusterSizeThreshold:
            for node in component:
                G.remove_node(node)
    return G


# ===== HELPER FUNCTIONS FOR TAKING A PERCENT OF THE GRAPH  ====== 
def removeRandomNodes(edges, percent):
    """
    returns a modified edges dictionary to represent percent% of the graph
    """
    nodes = set({})
    for (node1, node2) in edges:
        nodes.add(node1)
        nodes.add(node2)
    
    node_count = math.floor(len(nodes)*percent)
    
def removeRandomEdges(edges, percent):
    """
    returns a modified edges dictionary to represent percent% of the graph
    """

    edge_count = math.floor(len(edges)*percent)
    selected_edges = random.sample(edges.keys(), edge_count)
    selected_edges_dict = {edge: edges[edge] for edge in selected_edges}
    return selected_edges_dict


# ===== TESTING HELPER FUNCTIONS ====== 
def runGraphDiagnostics(edges):
    g = generateGraphGivenEdges(edges)
    print("RUNNING GRAPH DIAGNOSTICS\n")
    min_degree=len(g[list(g.keys())[0]])
    for node, edges in g.items():
        degree = len(edges)
        if min_degree > degree:
            min_degree = degree

    print(min_degree)

 

# # Test reading a Graph
# os.chdir(os.path.dirname(os.path.abspath(__file__))+"/test-graph-data")
# os.chdir("../test-graph-data")
# G = nx.read_edgelist(path = "test.txt", nodetype = int, data = (("weight", float),))

# # Test removing connected components
# G =removeClusters(G, 4)
# nx.draw(G)
# plt.show()

 
# ====== GENERATING THE GRAPH GML FILES =======


