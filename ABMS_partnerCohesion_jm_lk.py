"""
Computational Design and Simulation
assignment 01 - ABMS
students: Jonas Mertens, Likhinya Kvs
"""

import Rhino.Geometry as rg  # Import Rhino's geometry library for vector manipulation
import clr
clr.AddReference("ABxM.Core")  # Reference ABxM.Core for agent behavior management
import ABxM.Core as abm

# Define a custom behavior for partner cohesion among agents
class CartPartnerCohesion(abm.Behavior.BehaviorBase):
    def __init__(self, weight):
        """Initialize CartPartnerCohesion behavior with specified weight for cohesion."""
        self.Weight = weight
    
    def Execute(self, agent):
        """Execute the cohesion behavior based on partner matching criteria."""
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        # Check if agent's custom data meets criteria for partner cohesion behavior
        if cartesianAgent.CustomData['name'][1] == 'B':
            for neighbor in system.Agents:
                # Check if the neighbor has the same identifier for cohesion
                if neighbor.CustomData['name'][0] == cartesianAgent.CustomData['name'][0]:
                    # Calculate a vector for moving towards the neighbor at a specified distance
                    moveToDistance = cartesianAgent.Position - neighbor.Position
                    moveToDistance.Unitize()
                    desiredMove = (neighbor.Position + neighbor.CustomData['distance'] * moveToDistance) - cartesianAgent.Position
                    
                    # Apply the movement and associated weight to the agent
                    cartesianAgent.Moves.Add(desiredMove)
                    cartesianAgent.Weights.Add(self.Weight)
        
        else:
            return  # No action if criteria are not met

# Instantiate CartPartnerCohesion behavior with the provided weight input
behavior = CartPartnerCohesion(iWeight)
oBehavior = behavior
