#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>
 

 
using namespace ogdf;
 
int main()
{
    // READ THE INPUT GRAPH
    Graph G;
    GraphAttributes GA(G);
    if (!GraphIO::read(GA, G, "./test-graph-files/test-graph-GML-files/mips.gml", GraphIO::readGML)) {
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

    // OUTPUT RESULTS
    // GraphIO::write(GA, "FMMM-mips_10.gml", GraphIO::writeGML);
    GraphIO::write(GA, "FMMM-mips.svg", GraphIO::drawSVG);
 
    return 0;
}