"""
Computational Design and Simulation
assignment 01 - ABMS
students: Jonas Mertens, Likhinya Kvs
"""

import Rhino.Geometry as rg  # Import Rhino's geometry library for vector manipulation
import clr
clr.AddReference("ABxM.Core")  # Reference ABxM.Core for agent behavior management
import ABxM.Core as abm
import math

# Define a custom behavior for attraction among agents
class CartAttract(abm.Behavior.BehaviorBase):
    def __init__(self, weight, radius, step):
        """Initialize CartAttract behavior with specified weight, radius, and step size."""
        self.Weight = weight
        self.Radius = radius
        self.Step = step
    
    def Execute(self, agent):
        """Execute the attraction behavior for agents based on proximity and conditions."""
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        # Check if agent has specific attributes for 'A' type and 'empty' docking status
        if cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] == 'empty':
            # Find nearby agents within the specified radius
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            if neighbors.Count == 0:
                return

            anchors = []
            # Identify eligible neighbors as anchors
            for neighbor in neighbors:
                if (neighbor.CustomData['name'][0] != cartesianAgent.CustomData['name'][0]
                    and neighbor.CustomData['name'][1] == 'B'
                    and neighbor.CustomData['docking'] == 'empty'):
                        anchors.append(neighbor)

            if anchors:
                # Select the closest anchor to the agent
                closestAnchor = min(anchors, key=lambda anchor: (cartesianAgent.Position - anchor.Position).Length)

                # Find the partner of the closest anchor and calculate direction to it
                memberDirection = rg.Vector3d(0.0, 0.0, 0.0)
                for agent in system.Agents:
                    if (agent.CustomData['name'][0] == closestAnchor.CustomData['name'][0]
                        and agent.CustomData['name'][1] != closestAnchor.CustomData['name'][1]):
                        memberDirection = agent.Position - closestAnchor.Position
                        memberDirection.Unitize()
                
                # Move agent towards the closest anchor, adjusting distance
                moveTowards = closestAnchor.Position + closestAnchor.CustomData['e'] * memberDirection - cartesianAgent.Position
                length = moveTowards.Length
                moveTowards.Unitize()
                moveTowards = self.Step * (0.1 + length) * moveTowards
                cartesianAgent.AddMove(moveTowards, 'Attraction')
                cartesianAgent.Weights.Add(self.Weight)

        # Handle case where 'A' type agent is already docked
        elif cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] != 'empty':
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            if neighbors.Count == 0:
                return

            # Search for specific neighbor based on docking information
            for neighbor in neighbors:
                if neighbor.CustomData['name'] == cartesianAgent.CustomData['docking']:
                    memberDirection = rg.Vector3d(0.0, 0.0, 0.0)
                    # Find partner of the docked neighbor and calculate direction
                    for agent in system.Agents:
                        if (agent.CustomData['name'][0] == neighbor.CustomData['name'][0]
                            and agent.CustomData['name'][1] != neighbor.CustomData['name'][1]):
                            memberDirection = agent.Position - neighbor.Position
                            memberDirection.Unitize()
                    
                    # Move agent towards docked partner
                    moveTowards = neighbor.Position + neighbor.CustomData['e'] * memberDirection - cartesianAgent.Position
                    length = moveTowards.Length
                    moveTowards.Unitize()
                    moveTowards = self.Step * (0.1 + length) * moveTowards
                    cartesianAgent.AddMove(moveTowards, 'Attraction')
                    cartesianAgent.Weights.Add(self.Weight)

        else:
            return  # No action if criteria are not met

# Instantiate CartAttract behavior with provided weight, radius, and step inputs
behavior = CartAttract(iWeight, iRadius, iStep)
oBehavior = behavior
