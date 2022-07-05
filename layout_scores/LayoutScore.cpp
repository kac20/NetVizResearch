#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/basic/Graph_d.h>
#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>
#include <iostream>
#include <fstream>
 
#include <map>
#include <utility> 

using namespace ogdf;


int main (int argc, const char *argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << "filename" << std::endl;
        return 255;
    }

    // INPUT FILE INFO
    string filename = std::string(argv[1]);
    string inputFilePath = "./test-graph-data/";
    inputFilePath.append(filename);
    inputFilePath.append(".gml");

    // READ THE INPUT GRAPH
    Graph G;
    GraphAttributes GA(G);
    if (!GraphIO::read(GA, G, inputFilePath, GraphIO::readGML)) {
        std::cerr << "Could not load graph file" << std::endl;
        return 1;
    }

 
    // SET UP LAYOUT ALGORITHM CONFIGURATION
     for (node v : G.nodes)
        GA.width(v) = GA.height(v) = 5.0;
 
    FMMMLayout fmmm;
 
    fmmm.useHighLevelOptions(true);
    fmmm.unitEdgeLength(15.0);
    fmmm.newInitialPlacement(true);
    fmmm.qualityVersusSpeed(FMMMOptions::QualityVsSpeed::GorgeousAndEfficient);
 
    fmmm.call(GA);

    //GRAPH LAYOUT OUTPUT THE IMAGE
    string imagefilename = "FMMM-";
    imagefilename.append(filename);
    imagefilename.append(".svg");

    GraphIO::write(GA, imagefilename, GraphIO::drawSVG);


    //GRAPH LAYOUT OUTPUT THE NODE COORDINATES
    string nodeCoordinatesPath = "layoutCoords_";
    nodeCoordinatesPath.append(filename);
    nodeCoordinatesPath.append(".txt");
    
    std::ofstream nodeCoordinatesFile;
    nodeCoordinatesFile.open(nodeCoordinatesPath);

    for(node v = G.firstNode(); v != nullptr; v = v->succ()) {
        nodeCoordinatesFile << v;
        nodeCoordinatesFile << " ";
        nodeCoordinatesFile << GA.x(v);
        nodeCoordinatesFile << ' ';
        nodeCoordinatesFile << GA.y(v);
        nodeCoordinatesFile << "\n";
    }

    nodeCoordinatesFile.close();

 
    return 0;
}