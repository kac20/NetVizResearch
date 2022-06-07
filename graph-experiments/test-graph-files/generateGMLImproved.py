from collections import defaultdict
import math
import os
import matplotlib.pyplot as plt
import networkx as nx

def generateGMLFileImproved(inputFileName, clusterSizeThreshold, showTestingInfo = False):
    os.chdir(os.path.dirname(os.path.abspath(__file__))+"/test-graph-data")
    
    #Read the graph
    G = nx.read_edgelist(path = inputFileName, nodetype = int, data = (("weight", float),))

    #Remove clusters below the threshold
    G =removeSmallClusters(G, clusterSizeThreshold)

    if showTestingInfo:
        runGraphDiagnostics(G)

     #Write the graph to output file
    os.chdir("../test-graph-GML-files")
    outputFilePath = (inputFileName[:-4] + "_cluserSize:" + str(clusterSizeThreshold))
    nx.write_gml(G, outputFilePath, stringizer=None)
   
    

def removeSmallClusters(G, clusterSizeThreshold):
    for component in list(nx.connected_components(G)):
        if len(component)< clusterSizeThreshold:
            for node in component:
                G.remove_node(node)
    return G

def runGraphDiagnostics(G):
    #Plot degree histogram
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.show()

    #Plot component size histogram
    componentSizes = [len(component) for component in list(nx.connected_components(G))]
    plt.hist(componentSizes)
    plt.show()

    #Visualize graph
    nx.draw(G)
    plt.show()



# GENERATING THE GRAPH
generateGMLFileImproved("mips.txt", clusterSizeThreshold = 20, showTestingInfo = False)