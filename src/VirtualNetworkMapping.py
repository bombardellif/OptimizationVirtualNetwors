'''
Created on 05.06.2014

@author: fernando
'''

class VirtualNetworkMapping(object):
    '''
    classdocs
    '''

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
    
    def removePartOfSolution(self, virtualEdge, physicalVertex0, physicalVertex1):
        try:
            if physicalVertex0 != None:
                del self.vertex[virtualEdge[0]];
            if physicalVertex1 != None:
                del self.vertex[virtualEdge[1]];
        except:
            pass;
        
        del self.edge[virtualEdge];
        