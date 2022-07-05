from collections import defaultdict
import math
import os
import matplotlib.pyplot as plt
import networkx as nx
import random

def generateGMLFileImproved(inputFileName, percentOfGraph, clusterSizeThreshold, showTestingInfo = False):
    os.chdir(os.path.dirname(os.path.abspath(__file__))+"/test-graph-data")
    
    #Read the graph
    G = nx.read_edgelist(path = inputFileName, nodetype = int, data = (("weight", float),))

    #Take a percent of the graph
    G = takePercentOfGraph(G, percentOfGraph)

    #Remove clusters below the threshold
    G = removeSmallClusters(G, clusterSizeThreshold)

    if showTestingInfo:
        runGraphDiagnostics(G)

     #Write the graph to output file
    os.chdir("../test-graph-GML-files")
    outputFilePath = (inputFileName[:-4] + str(int(percentOfGraph*100))  +"_cluster_" + str(clusterSizeThreshold)+".gml")
    nx.write_gml(G, outputFilePath, stringizer=None)

    #Write the patient id's of the largest cluster to a file
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])

    os.chdir("../patientIDFiles")
    patientIDFilePath = (inputFileName[:-4] + str(int(percentOfGraph*100))  +"_" + str(clusterSizeThreshold)+"patientIDs.txt")
    writeNodesToFile(G0, patientIDFilePath)

    
def writeNodesToFile(G, outputFileName):
    outputFile = open(outputFileName, "w")
    for node in G.nodes:
         outputFile.write(str(node))
         outputFile.write("\n")
    outputFile.close()


def removeSmallClusters(G, clusterSizeThreshold):
    for component in list(nx.connected_components(G)):
        if len(component)< clusterSizeThreshold:
            for node in component:
                G.remove_node(node)
    return G


def takePercentOfGraph(G, percent):
    node_count = math.floor(len(G.nodes())*percent)
    nodes =  random.sample(G.nodes(), node_count)
    subgraph = G.subgraph(nodes)

    return nx.Graph(subgraph)

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
# generateGMLFileImproved("mips.txt", percentOfGraph = 1, clusterSizeThreshold = 4, showTestingInfo = False)
# generateGMLFileImproved("hippie.txt", percentOfGraph = .2, clusterSizeThreshold = 10, showTestingInfo = False)
# generateGMLFileImproved("mips.txt", percentOfGraph = 1, clusterSizeThreshold = 2, showTestingInfo = False)

generateGMLFileImproved("test.txt", percentOfGraph = 1, clusterSizeThreshold = 0, showTestingInfo = False)