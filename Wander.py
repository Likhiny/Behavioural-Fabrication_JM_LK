import Rhino
import Rhino.Geometry as rg
import clr
clr.AddReference("ABxM.Core")
import ABxM.Core as abm
import random
import math

from System.Collections.Generic import List


class CartWander(abm.Behavior.BehaviorBase):
    def __init__(self, weight, step):
        self.Weight = weight
        self.Step = step
    
    def Execute(self, agent):
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        if cartesianAgent.CustomData['name'][1] == 'A':
            randAngle= random.random() * math.pi
            wanderMove = self.Step * rg.Vector3d.XAxis
            wanderMove.Rotate(randAngle, rg.Vector3d.ZAxis)
            cartesianAgent.AddMove(wanderMove, 'Wander')
            cartesianAgent.Weights.Add(self.Weight)
        
        else: return
                

behavior = CartWander(iWeight, iStep)
oBehavior = behavior
