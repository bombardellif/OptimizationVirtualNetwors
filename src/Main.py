'''
Created on 05.06.2014

@author: fernando
'''
from src.Graph import Graph
from src.VirtualNetworkMapping import VirtualNetworkMapping

def mapInitialSolution(virtualEdge, currentSolution, alreadyMappedEdges, gPhysical, gVirtual):
    
    # Select physical vertex candidates for the mapping of the current virtual edge 
    if virtualEdge[0] in currentSolution.vertex:
        candidatesPhysicalVertices0 = currentSolution.vertex[virtualEdge[0]];
    else:
        candidatesPhysicalVertices0 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[0]]);
    
    if virtualEdge[1] in currentSolution.vertex:
        candidatesPhysicalVertices1 = currentSolution.vertex[virtualEdge[1]];
    else:
        candidatesPhysicalVertices1 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[1]]);
    
    # iterates in these candidate, until a possible combination matches, or no one does
    for possiblePhysicalVertex0 in candidatesPhysicalVertices0:
        for possiblePhysicalVertex1 in candidatesPhysicalVertices1:
            
            # look for possible paths between these two vertices
            cadidatesPhysicalPath = gPhysical.getCapablePaths(possiblePhysicalVertex0,
                                                              possiblePhysicalVertex1,
                                                              gVirtual.edge[virtualEdge[0]][virtualEdge[1]]);
            for possiblePhysicalPath in cadidatesPhysicalPath:
                
                # change current solution
                currentSolution.vertex[virtualEdge[0]] = possiblePhysicalVertex0;
                currentSolution.vertex[virtualEdge[1]] = possiblePhysicalVertex1;
                currentSolution.edge[virtualEdge] = possiblePhysicalPath;
                
                success = True;
                possibleEdgesToMap = set();
                while len(possibleEdgesToMap) > 0:
                    #TODO
                    pass
                #end while
                
                if success:
                    return True;
            # end for "paths"
        # end for "V1"
    # end for "v0"
    
    # If checked every combination and neither yield a feasible solution, then return False
    return False;


def inicializeSolution(gPhysical, gVirtual):
    emptyMap = VirtualNetworkMapping();
    
    return mapInitialSolution((None, None), emptyMap, set(), gPhysical, gVirtual);


if __name__ == '__main__':
    virtual = Graph('../data/rand1/vir.gtt');
    Physical = Graph('../data/rand1/sub.gtt');
    
    print();
    print(virtual.getCapableVertices(80));
    
    print();
    print(virtual.getCapablePaths('5', '1', 4));