import Rhino
import Rhino.Geometry as rg
import clr
clr.AddReference("ABxM.Core")
import ABxM.Core as abm
import random
import math

from System.Collections.Generic import List


class CartAttract(abm.Behavior.BehaviorBase):
    def __init__(self, weight, radius, distance):
        self.Weight = weight
        self.Radius = radius
        self.Distance = distance
    
    def Execute(self, agent):
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        if cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] == 'empty':
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            
            if(neighbors.Count == 0): return

            anchors = []
            for neighbor in neighbors:
                if neighbor.CustomData['name'][0] != cartesianAgent.CustomData['name'][0]\
                 and neighbor.CustomData['name'][1] == 'B' and neighbor.CustomData['docking'] == 'empty':
                        #Rhino.RhinoApp.WriteLine(neighbor.CustomData['name'])
                        anchors.append(neighbor)
                        
                else: pass

            if(len(anchors) > 0): 
                closestAnchor = min(anchors, key=lambda anchor: (cartesianAgent.Position - anchor.Position).Length)
                # find partner of anchor
                memberDirection = rg.Vector3d(0.0, 0.0, 0.0)
                memberDocking = "empty"
                for agent in system.Agents:
                    if agent.CustomData['name'][0] == closestAnchor.CustomData['name'][0]\
                        and agent.CustomData['name'][1] != closestAnchor.CustomData['name'][1]:
                        memberDirection = agent.Position - closestAnchor.Position
                        memberDirection.Unitize()
                        memberDocking = agent.CustomData['docking'][0]
    
                    else:
                        pass
                anchorPosition = closestAnchor.Position + closestAnchor.CustomData['e'] * memberDirection
                # check distance of agent to anchor
                anchorVector = cartesianAgent.Position - anchorPosition
                anchorDistance = anchorVector.Length
                if anchorDistance < self.Distance and cartesianAgent.CustomData['name'][0] != memberDocking:
                    Rhino.RhinoApp.WriteLine(cartesianAgent.CustomData['name'] + memberDocking)
                    cartesianAgent.NewCustomData['docking'] = closestAnchor.CustomData['name']
                    closestAnchor.NewCustomData['docking'] = cartesianAgent.CustomData['name']
                else: pass
        
        # undock if falsly connected (only undocks one side...WIP)
        elif cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] != 'empty':
            # find partner of docked agent
            for agent in system.Agents:
                if agent.CustomData['name'][0] == cartesianAgent.CustomData['docking'][0] and agent.CustomData['name'][1] == 'A'\
                 and agent.CustomData['docking'][0] == cartesianAgent.CustomData['name'][0]\
                  and int(agent.CustomData['name'][0]) < int(cartesianAgent.CustomData['name'][0]):
                  agent.NewCustomData['docking'] = "empty"
                else: pass
        
        else: return
                

behavior = CartAttract(iWeight, iRadius, iDistance)
oBehavior = behavior
