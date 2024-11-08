import Rhino.Geometry as rg
import clr
clr.AddReference("ABxM.Core")
import ABxM.Core as abm


class CohesionBehavior(abm.Behavior.BehaviorBase):
    def __init__(self, weight):
        self.Weight = weight
    
    def Execute(self, agent):
        boid = agent
        desired_velocity = rg.Vector3d(0,0,0)
        nodeNeighbors = 0 # will be a list

        for i, agent in enumerate(boid.AgentSystem.Agents):
            # find left member in supernode
            vector = agent.Position - boid.Position
            directedVector = boid.CustomData['direction'] * vector * boid.CustomData['direction']
            cross_product = directedVector.X * vector.Y - directedVector.Y * vector.X 
            if cross_product > 0 and boid.CustomData['direction'] * agent.CustomData['direction'] == 0.0:
                nodeNeighbors = i
            else:
                pass

        neighborAgent = boid.AgentSystem.Agents[nodeNeighbors]

        vector = neighborAgent.Position - boid.Position
        directedVector = neighborAgent.CustomData['direction'] * vector * neighborAgent.CustomData['direction']
        desired_velocity += (directedVector.Length - neighborAgent.CustomData['length']/2) * directedVector

        desired_velocity.Unitize()
        desired_velocity *= boid.AgentSystem.MaxSpeed
            
        steering = desired_velocity - boid.Velocity
        
        boid.AddForce(steering * self.Weight)

behavior = CohesionBehavior(iWeight)
oBehavior = behavior
