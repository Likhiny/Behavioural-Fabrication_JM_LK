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

            if len(anchors) > 0:
                closestAnchor = min(anchors, key=lambda anchor: (cartesianAgent.Position - anchor.Position).Length)
                moveTowards = closestAnchor.Position - cartesianAgent.Position
                length = moveTowards.Length
                moveTowards.Unitize()
                moveTowards = (self.Step * (0.1 + length) * moveTowards)
                cartesianAgent.AddMove(moveTowards, 'Attraction')
                cartesianAgent.Weights.Add(self.Weight)

        elif cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] != 'empty':
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            
            if(neighbors.Count == 0): return

            for neighbor in neighbors:
                if neighbor.CustomData['name'] == cartesianAgent.CustomData['docking']:
                        #Rhino.RhinoApp.WriteLine(neighbor.CustomData['name'])
                        moveTowards = neighbor.Position - cartesianAgent.Position
                        length = moveTowards.Length
                        moveTowards.Unitize()
                        moveTowards = (self.Step * (0.1 + length) * moveTowards)
                        cartesianAgent.AddMove(moveTowards, 'Attraction')
                        cartesianAgent.Weights.Add(self.Weight)
                        
                else: pass

        else: return
                

behavior = CartAttract(iWeight, iRadius, iStep)
oBehavior = behavior