'''
Created on 05.06.2014

@author: fernando
'''
from _io import open

class Graph(object):
    '''
    classdocs
    '''

    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.vertex = {};
        self.edge = {};
        
        file = open(fileName, 'r');
            
        # iterates through the lines of the file
        for line in file:
            splittedLine = line.split(None);
            if len(splittedLine) >= 3:
                # Vertex
                if splittedLine[0] == 'V':
                    self.vertex[splittedLine[1]] = [int(splittedLine[2]), True];
                    self.edge[splittedLine[1]] = {};
                # Edge
                elif splittedLine[0] == 'E':
                    self.edge[splittedLine[1]][splittedLine[2]] = [int(splittedLine[3]), int(splittedLine[3])];
                    self.edge[splittedLine[2]][splittedLine[1]] = [int(splittedLine[3]), int(splittedLine[3])];
        
        print(self.vertex);
        print(self.edge);
        
    def getCapableVertices(self, minCapacity):
        return [k for k,v in self.vertex.items() if (v[0] >= minCapacity and v[1])];
    
    def getCapablePaths(self, v1, v2, demand):
        resultPaths = [[v1]];
        ## Local function to help
        def addVertexToAppropriatePaths(vFrom, vTo):
            nonlocal resultPaths; # bind with the outer scope
            for i in range(0,len(resultPaths)):
                try:
                    idx = resultPaths[i].index(vFrom);
                    # if vFrom is in the end of list, then append the new vertex in this path
                    if idx == len(resultPaths[i])-1:
                        resultPaths[i].append(vTo);
                    # if vFrom is in the middle, then "fork" of the path, creating a new one
                    else:
                        newPath = resultPaths[i][0:idx+1];
                        newPath.append(vTo);
                        if newPath not in resultPaths:
                            resultPaths.append(newPath);
                except:
                    #vFrom is not in this path, continue
                    pass
        ## End of local function 
        visitedEdges = set();
        visitedVertices = set();
        verticesToVisit = set(v1);
        
        # while there are possible adjacent vertices to visit, do:
        while len(verticesToVisit) > 0:
            # select any vertex possible
            currentVtx = verticesToVisit.pop();
            
            #if it is not the final goal, keep walking on the graph
            if currentVtx != v2:
                # select possible new adjacent vertices through edges not yet visited 
                for k,v in self.edge[currentVtx].items():
                    testEdge_ij = (currentVtx, k);
                    testEdge_ji = (k, currentVtx);
                    # if this edge has enough band available (and wasn't yet visited), add to the set of edges to visit
                    if v[1] >= demand and testEdge_ij not in visitedEdges:
                        # control whether it is a new vertex
                        if k not in visitedVertices:
                            verticesToVisit.add(k);
                            visitedVertices.add(k);
                        # don't visit this edge anymore
                        visitedEdges.add(testEdge_ij);
                        visitedEdges.add(testEdge_ji);
                        # add this edge to the right path
                        addVertexToAppropriatePaths(currentVtx, k);
                        
                #end for
        #end while
        
        # post processing: remove paths that don't get to the goal "v2"
        return [path for path in resultPaths if path[-1] == v2];