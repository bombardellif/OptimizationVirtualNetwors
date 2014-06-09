'''
Created on 05.06.2014

@author: fernando
'''
from copy import deepcopy

class VirtualNetworkMapping(object):
    '''
    classdocs
    '''
    
    def copy(self):
        new = VirtualNetworkMapping();
        new.vertex = deepcopy(self.vertex);
        new.edge = deepcopy(self.edge);
        return new;

    def __init__(self):
        '''
        Constructor
        '''
        self.vertex = {};
        self.edge = {};
        
    def addPartOfSolution(self, virtualEdge, physicalVertex0, physicalVertex1, physicalPath):
        self.vertex[virtualEdge[0]] = physicalVertex0;
        self.vertex[virtualEdge[1]] = physicalVertex1;
        
        self.edge[virtualEdge] = physicalPath;
        self.edge[virtualEdge[::-1]] = physicalPath;
    
    def removePartOfSolution(self, virtualEdge, physicalVertex0, physicalVertex1):
        if physicalVertex0 != None:
            del self.vertex[virtualEdge[0]];
        if physicalVertex1 != None:
            del self.vertex[virtualEdge[1]];
        
        del self.edge[virtualEdge];
        del self.edge[virtualEdge[::-1]];
    
    def totalUsedBand(self, graph):
        band = 0;
        for pathEdge, path in self.edge.items():
            band += (len(path)-1) * graph.edge[pathEdge[0]][pathEdge[1]][0];
        
        return band;
