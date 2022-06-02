from collections import defaultdict
import math
import os
import pathlib

def generateGraphGivenEdges(nodes,edges):
    """
    Inputs: nodes - a set of the unique nodes in a graph
            edges - a set of edges
    """

def generateGMLFile(inputFileName, percentToGenerate):
    """
    Inputs:
        • inputFilePath, the name of a .txt file located in the "test-graph-data" directory
                        representing a graph graph where each line is an edge of the 
                        format: node1 node2 edge_weight

        • percentToGenerate, a decimal for the percent of the graph to copy over 
    
    Effects:
        • creates a .gml file representing the graph specified by inputFilePath
            in the directory "test-graph-GML-files"

    """

    os.chdir(os.path.dirname(os.path.abspath(__file__))+"/test-graph-data")

    inputFile = open(inputFileName, 'r')

    # store the nodes and edges of the graph
    nodes = set({})
    edges = {}

    # store the string .gml file representation of nodes and edges
    nodes_string = set({})
    edges_string = set({})
    
    #determine number of edges to read
    total_edges = sum(1 for line in open(inputFileName, 'r'))
    edges_to_read = math.floor(total_edges*percentToGenerate)

    ## PARSE THE GRAPH
    for line in inputFile.readlines():
        #parse the line (each line represents an edge)
        (node1, node2, edge_weight) = line.strip().split()

        #add both edge end points info
        nodes.add(node1)
        nodes.add(node2)
        edges[{node1,node2}] = edge_weight

        #add both edge end points (if not already added) in GML string format
        nodes_string.add("\t\tid " + str(node1) + "\n\t\tlabel " + str(node1))
        nodes_string.add("\t\tid " + str(node2) + "\n\t\tlabel " + str(node2))

        #add the edge in GML string format
        edges_string = "\t\tsource " + str(node1) + "\n\t\ttarget " + str(node2) + "\n\t\tlabel " + str(edge_weight)
        edges_string.add(edge)

        if edges_to_read <= 0:
            break
        else:
            edges_to_read = edges_to_read-1
    

    inputFile.close()

    ## CREATE THE GRAPH STRING
    graph = "graph ["
    # add the node information to the graph
    for node in nodes_string:
        graph += "\n\tnode [\n" + node + "\n\t]"
    # add the edge information to the graph
    for edge in edges_string:
        graph += "\n\tedge [\n" + edge + "\n\t]"
    graph += "\n]"

    
    ## WRITE THE GRAPH TO THE OUTPUTFILE
    os.chdir("../test-graph-GML-files")
    outputFilePath = (inputFileName[:-4] + "_" + str(int(percentToGenerate*100))+".gml")
    outputFile = open(outputFilePath, 'w')
    outputFile.write(graph)
    outputFile.close()


# ====== GENERATING THE GRAPH GML FILES =======
generateGMLFile("hippie.txt", .25)



        

