'''
Created on 05.06.2014

@author: fernando
'''
from src.Graph import Graph
from src.VirtualNetworkMapping import VirtualNetworkMapping

def addPartOfSolution(solution, physicalGraph, virtualEdge, edgeDemand, physicalVertex0, physicalVertex1, physicalPath):
    solution.addPartOfSolution(
        virtualEdge,
        physicalVertex0,
        physicalVertex1,
        physicalPath
    );
    physicalGraph.allocateResources(
        physicalVertex0,
        physicalVertex1,
        physicalPath,
        edgeDemand
    );

def removePartOfSolution(solution, physicalGraph, virtualEdge, edgeDemand, physicalVertex0, physicalVertex1, physicalPath):
    solution.removePartOfSolution(
        virtualEdge,
        physicalVertex0,
        physicalVertex1
    );
    physicalGraph.freeResources(
        physicalVertex0,
        physicalVertex1,
        physicalPath,
        edgeDemand
    );


def mapInitialSolution(virtualEdge, currentSolution, alreadyMappedEdges, gPhysical, gVirtual):
    
    # Select physical vertex candidates for the mapping of the current virtual edge 
    if virtualEdge[0] in currentSolution.vertex:
        candidatesPhysicalVertices0 = [currentSolution.vertex[virtualEdge[0]]];
    else:
        candidatesPhysicalVertices0 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[0]][0]);
    
    if virtualEdge[1] in currentSolution.vertex:
        candidatesPhysicalVertices1 = [currentSolution.vertex[virtualEdge[1]]];
    else:
        candidatesPhysicalVertices1 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[1]][0]);
    
    # iterates in these candidate, until a possible combination matches, or no one does
    for possiblePhysicalVertex0 in candidatesPhysicalVertices0:
        for possiblePhysicalVertex1 in candidatesPhysicalVertices1:
            
            # look for possible paths between these two vertices
            cadidatesPhysicalPath = gPhysical.getCapablePaths(possiblePhysicalVertex0,
                                                              possiblePhysicalVertex1,
                                                              gVirtual.edge[virtualEdge[0]][virtualEdge[1]][0]);
            for possiblePhysicalPath in cadidatesPhysicalPath:
                
                # keep whether the chosen vertex has already been allocated,
                # if yes, it mustn't free it after
                newVertex0 = not gPhysical.vertex[possiblePhysicalVertex0][1];
                newVertex1 = not gPhysical.vertex[possiblePhysicalVertex1][1];
                
                # change current solution
                assert(gPhysical.vertex[possiblePhysicalVertex0][0] >= gVirtual.vertex[virtualEdge[0]][0]);
                assert(gPhysical.vertex[possiblePhysicalVertex1][0] >= gVirtual.vertex[virtualEdge[1]][0]);
                addPartOfSolution(
                    currentSolution,
                    gPhysical,
                    virtualEdge,
                    gVirtual.edge[virtualEdge[0]][virtualEdge[1]][0],
                    possiblePhysicalVertex0,
                    possiblePhysicalVertex1,
                    possiblePhysicalPath
                );
                
                success = True;
                possibleEdgesToMap = gVirtual.setOfEdges - alreadyMappedEdges;
                while len(possibleEdgesToMap) > 0:
                    # select an edge from the possible to map
                    nextEdgeToMap = possibleEdgesToMap.pop();
                    
                    alreadyMappedEdges.add(nextEdgeToMap);
                    
                    success = mapInitialSolution(nextEdgeToMap, currentSolution, alreadyMappedEdges, gPhysical, gVirtual);
                    
                    if success:
                        break;
                    else:
                        # in the case it wasn't possible to make a feasible solution, try with another next virtual edge
                        alreadyMappedEdges.remove(nextEdgeToMap);
                #end while
                
                # if found a solution, then it's enough, return True
                # else, try to find with a different path or physical vertices
                if success:
                    return True;
                else:
                # if solution wasn't found, then undo the changes in the current solution made above
                # and try with other paths or vertices
                    removePartOfSolution(
                        currentSolution,
                        gPhysical,
                        virtualEdge,
                        gVirtual.edge[virtualEdge[0]][virtualEdge[1]][0], # demand of the virtual edge
                        (None if newVertex0 else possiblePhysicalVertex0), # remove only if it was added inside this call of this function
                        (None if newVertex1 else possiblePhysicalVertex1), # remove only if it was added inside this call of this function
                        possiblePhysicalPath
                    );
            # end for "paths"
        # end for "V1"
    # end for "v0"
    
    # If checked every combination and neither yield a feasible solution, then return False
    return False;


def inicializeSolution(gPhysical, gVirtual):
    solutionMap = VirtualNetworkMapping();
    
    alreadyMappedEdges = set();
    success = False;
    for virtualEdge in gVirtual.setOfEdges:
        # try to find a valid mapping. Try with each vertex until find a valid solution
        print("trying with" + str(virtualEdge));
        
        alreadyMappedEdges.add(virtualEdge);
        success = mapInitialSolution(virtualEdge, solutionMap, alreadyMappedEdges, gPhysical, gVirtual);
        alreadyMappedEdges.remove(virtualEdge);
        if success:
            break;
    
    if success:
        return solutionMap;
    else:
        return None;


if __name__ == '__main__':
    virtual = Graph('../data/rand1/vir.gtt');
    physical = Graph('../data/rand1/sub.gtt');
    
    solution = inicializeSolution(physical, virtual);
    
    print(solution);
    if solution != None:
        print(solution.vertex);
        print(solution.edge);