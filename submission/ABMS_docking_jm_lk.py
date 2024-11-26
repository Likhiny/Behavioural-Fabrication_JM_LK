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

# Define a custom behavior for docking among agents
class CartDocking(abm.Behavior.BehaviorBase):
    def __init__(self, weight, radius, distance):
        """Initialize CartDocking behavior with specified weight, radius, and docking distance."""
        self.Weight = weight
        self.Radius = radius
        self.Distance = distance
    
    def Execute(self, agent):
        """Execute the docking behavior for agents based on proximity and docking status."""
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        # If agent type is 'A' and currently undocked
        if cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] == 'empty':
            # Find nearby agents within the specified radius
            neighbors = system.FindNeighbors(cartesianAgent, self.Radius)
            if neighbors.Count == 0:
                return

            anchors = []
            # Identify eligible neighbors as potential docking anchors
            for neighbor in neighbors:
                if (neighbor.CustomData['name'][0] != cartesianAgent.CustomData['name'][0]
                    and neighbor.CustomData['name'][1] == 'B'
                    and neighbor.CustomData['docking'] == 'empty'):
                        anchors.append(neighbor)

            # If eligible anchors are found, select the closest one
            if anchors:
                closestAnchor = min(anchors, key=lambda anchor: (cartesianAgent.Position - anchor.Position).Length)
                
                # Find the partner of the closest anchor and calculate direction
                memberDirection = rg.Vector3d(0.0, 0.0, 0.0)
                memberDocking = "empty"
                for agent in system.Agents:
                    if (agent.CustomData['name'][0] == closestAnchor.CustomData['name'][0]
                        and agent.CustomData['name'][1] != closestAnchor.CustomData['name'][1]):
                        memberDirection = agent.Position - closestAnchor.Position
                        memberDirection.Unitize()
                        memberDocking = agent.CustomData['docking'][0]

                # Calculate anchor's intended position based on partner direction
                anchorPosition = closestAnchor.Position + closestAnchor.CustomData['e'] * memberDirection
                
                # Check if agent is within docking distance to anchor
                anchorVector = cartesianAgent.Position - anchorPosition
                anchorDistance = anchorVector.Length
                if anchorDistance < self.Distance and cartesianAgent.CustomData['name'][0] != memberDocking:
                    # Establish docking relationship if within range and valid
                    cartesianAgent.NewCustomData['docking'] = closestAnchor.CustomData['name']
                    closestAnchor.NewCustomData['docking'] = cartesianAgent.CustomData['name']

        # Undock if docking conditions are invalid
        elif cartesianAgent.CustomData['name'][1] == 'A' and cartesianAgent.CustomData['docking'] != 'empty':
            # Find partner of the docked agent
            for agent in system.Agents:
                if (agent.CustomData['name'][0] == cartesianAgent.CustomData['docking'][0]
                    and agent.CustomData['name'][1] == 'A'):
                    # Check if undocking criteria are met
                    if (agent.CustomData['docking'][0] == int(cartesianAgent.CustomData['name'][0]) 
                        and int(agent.CustomData['name'][0] < cartesianAgent.CustomData['name'][0])):
                        # Locate docking agent to undock
                        for anchor in system.Agents:
                            if anchor.CustomData['name'] == cartesianAgent.CustomData['docking']:
                                cartesianAgent.NewCustomData['docking'] = "empty"
                                anchor.NewCustomData['docking'] = "empty"

        else:
            return  # No action if criteria are not met

# Instantiate CartDocking behavior with provided weight, radius, and docking distance inputs
behavior = CartDocking(iWeight, iRadius, iDistance)
oBehavior = behavior
