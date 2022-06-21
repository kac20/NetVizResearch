#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>
 
using namespace ogdf;
 
int main()
{
     // READ THE INPUT GRAPH
    Graph G;
    GraphAttributes GA(G);
    if (!GraphIO::read(GA, G, "./test-graph-files/test-graph-GML-files/mips100_cluser_4.gml", GraphIO::readGML)) {
        std::cerr << "Could not load graph file" << std::endl;
        return 1;
    }


    // GET ALL NODES IN THE COMPONENT

    ogdf::Graph::allNodes(CONTAINER)
   
 
    return 0;
}