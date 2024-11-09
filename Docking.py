import Rhino
import Rhino.Geometry as rg
import clr
clr.AddReference("ABxM.Core")
import ABxM.Core as abm
import random
import math

from System.Collections.Generic import List


class CartAttract(abm.Behavior.BehaviorBase):
    def __init__(self, weight, radius, step):
        self.Weight = weight
        self.Radius = radius
        self.Step = step
    
    def Execute(self, agent):
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        if cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] == 'empty':
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            
            if(neighbors.Count == 0): return

            anchors = []
            for neighbor in neighbors:
                if neighbor.CustomData['name'][0] != cartesianAgent.CustomData['name'][0] and neighbor.CustomData['name'][1] == 'B' and neighbor.CustomData['docking'] == 'empty':
                        #Rhino.RhinoApp.WriteLine(neighbor.CustomData['name'])
                        anchors.append(neighbor)
                        
                else: pass

            if(len(anchors) > 0): 
                closestAnchor = min(anchors, key=lambda anchor: (cartesianAgent.Position - anchor.Position).Length)
                cartesianAgent.NewCustomData['docking'] = closestAnchor.CustomData['name']
                closestAnchor.NewCustomData['docking'] = cartesianAgent.CustomData['name']

        else: return
                

behavior = CartAttract(iWeight, iRadius, iStep)
oBehavior = behavior
