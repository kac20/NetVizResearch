#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/basic/Graph_d.h>
#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>
 
#include <map>
#include <utility> 

using namespace ogdf;

// A class constructed with the GA of a ODGF layout Graph
// The Class contains methods to calculate the score of the nodes

class LayoutScore {
    public:
        std::map<int, std::pair<double, double>> nodeCoordinates;

        LayoutScore(Graph G, GraphAttributes GA); //Constructor

        void printCoordinates() {
            for(auto it = nodeCoordinates.cbegin(); it != nodeCoordinates.cend(); ++it)
                {
                    std::cout << it->first << " " << it->second.first << " " << it->second.second << "\n";
                }
        }


};

/**
 * LayoutScore Constructor
 * 
 * inputs: GA for a graph from an ODGF Layout
 * 
 * effects: defines a vector of all nodes' (x, y) positions
 * */
LayoutScore::LayoutScore(Graph G, GraphAttributes GA) {
    // construct nodeCoordinates which maps each node to its (x,y) coords
    for(node v = G.firstNode(); v!= nullptr; v=v->succ()) {
        std::pair <double, double> coords (GA.x(v), GA.y(v));
        nodeCoordinates.insert(std::pair<int, std::pair<double, double>> 
                    (GA.idNode(v)	, coords));
    }


}

int main () {
     // READ THE INPUT GRAPH
    Graph G;
    GraphAttributes GA(G);
    if (!GraphIO::read(GA, G, "./test-graph-files/test-graph-GML-files/test.gml", GraphIO::readGML)) {
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


    // Call the LayoutScore constructor
    LayoutScore layoutScore(G, GA);
    layoutScore.printCoordinates();

    //printing the coordinates
 
    return 0;
}