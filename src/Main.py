'''
Created on 05.06.2014

@author: fernando
'''
from src.Graph import Graph
from src.VirtualNetworkMapping import VirtualNetworkMapping
import random
from math import exp, log
import sys
import datetime

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

numberOfCalls = 0;
CALLS_THREASHOLD = 100000;
def mapInitialSolution(virtualEdge, currentSolution, alreadyMappedEdges, gPhysical, gVirtual):
    global numberOfCalls;
    global CALLS_THREASHOLD;
    
    # Select physical vertex candidates for the mapping of the current virtual edge 
    if virtualEdge[0] in currentSolution.vertex:
        candidatesPhysicalVertices0 = [currentSolution.vertex[virtualEdge[0]]];
    else:
        candidatesPhysicalVertices0 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[0]][0]);
    
    if virtualEdge[1] in currentSolution.vertex:
        candidatesPhysicalVertices1 = [currentSolution.vertex[virtualEdge[1]]];
    else:
        candidatesPhysicalVertices1 = gPhysical.getCapableVertices(gVirtual.vertex[virtualEdge[1]][0]);
    
    # iterates in these candidate, until a possible combination matches, or none does
    processedVertices = [];
    for possiblePhysicalVertex0 in candidatesPhysicalVertices0:
        for possiblePhysicalVertex1 in candidatesPhysicalVertices1:
            
            # enter only if this tuple of vertices hasn't been tried yet
            if (possiblePhysicalVertex0, possiblePhysicalVertex1) not in processedVertices:
                processedVertices.append((possiblePhysicalVertex1, possiblePhysicalVertex0));
                
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
                    # sort possible edges to continue, in order to prioritize adjacent edges
                    possibleEdgesToMap = list(gVirtual.setOfEdges - alreadyMappedEdges);
                    compareFunc = (lambda t : 0 if (t[0] == virtualEdge[0] or t[0] == virtualEdge[1] or t[1] == virtualEdge[0] or t[1] == virtualEdge[1]) else 1);
                    possibleEdgesToMap.sort(key = compareFunc);
                    for nextEdgeToMap in possibleEdgesToMap:
                        # select an edge from the possible to map
                        #nextEdgeToMap = possibleEdgesToMap.pop();
                        
                        alreadyMappedEdges.add(nextEdgeToMap);
                        
                        #print("\t["+str((possiblePhysicalVertex0, possiblePhysicalVertex1))+"]Try now with" + str(nextEdgeToMap) +" - "+str(globalDebug) + " - "+str(iii)+ " - " +str(len(possibleEdgesToMap)) + " - "+ str(possiblePhysicalPath));
                        numberOfCalls += 1;
                        success = mapInitialSolution(nextEdgeToMap, currentSolution, alreadyMappedEdges, gPhysical, gVirtual);
                        
                        if success:
                            break;
                        else:
                            # in the case it wasn't possible to make a feasible solution, try with another next virtual edge
                            alreadyMappedEdges.remove(nextEdgeToMap);
                            if numberOfCalls > CALLS_THREASHOLD:
                                break;

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
                        if numberOfCalls > CALLS_THREASHOLD:
                            return False;
                # end for "paths"
            # end if
        # end for "V1"
    # end for "v0"
    
    # If checked every combination and neither yield a feasible solution, then return False
    return False;


def inicializeSolution(gPhysical, gVirtual):
    global numberOfCalls;
    solutionMap = VirtualNetworkMapping();
    
    alreadyMappedEdges = set();
    success = False;
    for virtualEdge in gVirtual.setOfEdges:
        # try to find a valid mapping. Try with each vertex until find a valid solution
        print("trying with" + str(virtualEdge));
        
        numberOfCalls = 0;
        
        alreadyMappedEdges.add(virtualEdge);
        success = mapInitialSolution(virtualEdge, solutionMap, alreadyMappedEdges, gPhysical, gVirtual);
        alreadyMappedEdges.remove(virtualEdge);
        if success:
            break;
    
    if success:
        return solutionMap;
    else:
        return None;

def findNeighbor(originalSolution, originalGPhysical, gVirtual, numOfTries):
    
    count = 0;
    while count < numOfTries:
        solution = originalSolution.copy();
        gPhysical = originalGPhysical.copy();
        # choose a random vertex from the virtual graph
        chosenVertex = random.choice(list(gVirtual.vertex.keys()));
        
        backupMappedVertices = {
            chosenVertex: solution.vertex[chosenVertex]
        };
        
        # for each adjacent virtual edge of the chosen vertex, remove the physical path from the solution
        firstLoop = True;
        for neighborVertex in gVirtual.edge[chosenVertex].keys():
            virtualEdge = (chosenVertex, neighborVertex);
            edgeDemand = gVirtual.edge[chosenVertex][neighborVertex][0];
            
            backupMappedVertices[neighborVertex] = solution.vertex[neighborVertex];
            
            removePartOfSolution(
                solution,
                gPhysical,
                virtualEdge,
                edgeDemand,
                (solution.vertex[chosenVertex] if firstLoop else None),
                None,
                solution.edge[virtualEdge]
            );
            firstLoop = False;
        
        # iterate over every possible physical vertex to allocate this virtual
        candidateVertices = gPhysical.getCapableVertices(gVirtual.vertex[chosenVertex][0], backupMappedVertices[chosenVertex]);
        for possibleVertex in candidateVertices:
            
            success = True;
            # for each adjacent virtual edge of the chosen vertex, try to establish a physical path
            for neighborVertex in gVirtual.edge[chosenVertex].keys():
                virtualEdge = (chosenVertex, neighborVertex);
                edgeDemand = gVirtual.edge[chosenVertex][neighborVertex][0];
                
                candidatePaths = gPhysical.getCapablePaths(possibleVertex, backupMappedVertices[neighborVertex], edgeDemand);
                if len(candidatePaths) > 0:
                    # get random feasible path between the two vertices
                    newPath = random.choice(candidatePaths);
                    
                    addPartOfSolution(
                        solution,
                        gPhysical,
                        virtualEdge,
                        edgeDemand,
                        possibleVertex,
                        backupMappedVertices[neighborVertex],
                        newPath
                    );
                else:
                    # couldn't find a path for every adjacent vertex
                    success = False;
                    break;
            #end for
            
            if success:
                break;
        #end for
        if success:
            return (solution, gPhysical);
        count += 1;
    #end while
    return None;

def initialTemperature(solution, gPhysical, gVirtual, numOfIterations):
    numOfTriesNeighborhood = (len(gVirtual.setOfEdges) / 2);
    
    maxVariation = 0;
    for i in range(1,numOfIterations):
        
        neighbor = findNeighbor(solution, gPhysical, gVirtual, numOfTriesNeighborhood);
        if neighbor != None:
            newSolution = neighbor[0];
            
            variation = abs(newSolution.totalUsedBand(gVirtual) - solution.totalUsedBand(gVirtual));
            if variation > maxVariation:
                maxVariation = variation;
    #end for
    
    return -maxVariation / (log(0.8));

def simmulatedAnnealing(solution, gPhysical, gVirtual, iterMaxOutter, iterMaxInner, iterMinSuccess, alphaCooler):
    min=solution.totalUsedBand(gVirtual);
    numOfTriesNeighborhood = (len(gVirtual.setOfEdges) / 2);
    temperature = initialTemperature(solution, gPhysical, gVirtual, int(iterMaxOutter));
    
    j = 1;
    while j <= iterMaxOutter:
        successCount = 0;
        for i in range(1,iterMaxInner):
            
            neighbor = findNeighbor(solution, gPhysical, gVirtual, numOfTriesNeighborhood);
            if neighbor != None:
                newSolution = neighbor[0];
                newGraph = neighbor[1];
            
                variation = newSolution.totalUsedBand(gVirtual) - solution.totalUsedBand(gVirtual);
                if variation < 0:
                    successCount += 1;
                if variation <= 0 or exp(-variation / temperature) > random.random():
                    solution = newSolution;
                    gPhysical = newGraph;
                    if newSolution.totalUsedBand(gVirtual) < min:
                        min = newSolution.totalUsedBand(gVirtual);
        #end inner for
        
        temperature *= alphaCooler;
        print('Temperature=',temperature);
        print('Current Solution=', solution.totalUsedBand(gVirtual));
        print('Minimum=',min);
        j += 1;
        if successCount < iterMinSuccess:
            break;
    
    return solution;

def algorithmParameters():
    default = [
       'solution.txt',  # solution output
       'rand1',         # problem instance folder (inside data folder)
       1000,            # outer loop iteration limit
       300,             # inner loop iteration limit
       10,              # without improve iteration limit
       0.99             # alpha cooler
    ];
    i=0;
    firstLoop = True;
    for arg in sys.argv:
        if not firstLoop:
            default[i] = arg;
            i += 1;
        else:
            firstLoop = False;
    
    return default;
    

if __name__ == '__main__':
    
    (outputFilename, instance, outerIter, innerIter, minSuccessIter, alpha) = algorithmParameters()

    virtual = Graph('../data/'+instance+'/vir.gtt');
    physical = Graph('../data/'+instance+'/sub.gtt');
    
    # DEBUG:
    '''solution = VirtualNetworkMapping();
    vertices = {'7': '19', '1': '34', '5': '26', '2': '30', '9': '42', '4': '21', '8': '47', '6': '2', '3': '20', '0': '14'};
    edges = {('5', '1'): ['34', '6', '20', '49', '26'], ('0', '8'): ['14', '47'], ('3', '6'): ['20', '6', '25', '31', '13', '2'], ('6', '3'): ['20', '6', '25', '31', '13', '2'], ('2', '4'): ['30', '10', '21'], ('7', '6'): ['2', '46', '43', '10', '19'], ('2', '5'): ['30', '46', '8', '26'], ('4', '2'): ['30', '10', '21'], ('6', '1'): ['34', '24', '2'], ('8', '0'): ['14', '47'], ('1', '5'): ['34', '6', '20', '49', '26'], ('1', '9'): ['34', '6', '20', '0', '15', '42'], ('9', '1'): ['34', '6', '20', '0', '15', '42'], ('6', '7'): ['2', '46', '43', '10', '19'], ('5', '2'): ['30', '46', '8', '26'], ('8', '5'): ['26', '23', '40', '47'], ('5', '8'): ['26', '23', '40', '47'], ('1', '6'): ['34', '24', '2']};
    for k,path in edges.items():
        addPartOfSolution(solution, physical, k, virtual.edge[k[0]][k[1]][0], vertices[k[0]], vertices[k[1]], path);
    
    if solution != None:
        print(solution.vertex);
        print(solution.edge);'''
    
    print('Output File Name: ',outputFilename);
    print('Instance Name: ',instance);
    print();
    print('Initializing ...');
    solution = inicializeSolution(physical, virtual);
    
    if solution == None:
        print('Could not find a feasible solution');
    else:
        print('Starting Optimization ({}) ...'.format(datetime.datetime.now()));    
        print('Outer Iterations: ',outerIter);
        print('Inner Iterations: ',innerIter);
        print('Minimum Successful Iterations: ',minSuccessIter);
        print('Alpha Cooler: ',alpha);
        print("Initial Value: "+str(solution.totalUsedBand(virtual)));
        
        solution = simmulatedAnnealing(solution, physical, virtual, outerIter, innerIter, minSuccessIter, alpha);
        
        print('Optimization Ended ({}) ...'.format(datetime.datetime.now()));
        print("Final Value: "+str(solution.totalUsedBand(virtual)));
        
        out = open(outputFilename, 'w');
        out.write(str(solution.vertex));
        out.write(str(solution.edge));
    