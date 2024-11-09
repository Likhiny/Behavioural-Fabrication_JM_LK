import Rhino
import Rhino.Geometry as rg
import clr
clr.AddReference("ABxM.Core")
import ABxM.Core as abm

from System.Collections.Generic import List


class CartPartnerCohesion(abm.Behavior.BehaviorBase):
    def __init__(self, weight):
        self.Weight = weight
    
    def Execute(self, agent):
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        if cartesianAgent.CustomData['name'][1] == 'B':
            for neighbor in cartesianAgent.AgentSystem.Agents:
                if neighbor.CustomData['name'][0] == cartesianAgent.CustomData['name'][0]:
                    #Rhino.RhinoApp.WriteLine(neighbor.CustomData['name']+cartesianAgent.CustomData['name'])
                    moveToDistance = cartesianAgent.Position - neighbor.Position
                    moveToDistance.Unitize()
                    moveToDistance = (neighbor.Position + neighbor.CustomData['distance'] * moveToDistance) - cartesianAgent.Position
                    cartesianAgent.Moves.Add(moveToDistance)
                    cartesianAgent.Weights.Add(self.Weight)
                
                else: pass
        
        else: return
                

behavior = CartPartnerCohesion(iWeight)
oBehavior = behavior
