"""
Computational Design and Simulation
assignment 01 - ABMS
students: Jonas Mertens, Likhinya Kvs
"""

import Rhino.Geometry as rg  # Import Rhino's geometry library for vector and rotation operations
import clr
clr.AddReference("ABxM.Core")  # Add a reference to ABxM.Core library
import ABxM.Core as abm  # Import ABxM.Core as abm for agent behavior management
import random
import math

# Define a custom behavior for a wandering movement in a cartesian coordinate system
class CartWander(abm.Behavior.BehaviorBase):
    def __init__(self, weight, step):
        """Initialize CartWander behavior with specified weight and step size."""
        self.Weight = weight
        self.Step = step
    
    def Execute(self, agent):
        """Execute the wandering behavior based on agent attributes."""
        
        cartesianAgent = agent
        system = cartesianAgent.AgentSystem

        # Check if the agent's custom data meets specific criteria
        if cartesianAgent.CustomData['name'][1] == 'A':
            # Calculate a random rotation angle in radians
            randAngle = random.random() * math.pi
            
            # Define a movement vector along the X-axis and rotate it around Z-axis by randAngle
            wanderMove = self.Step * rg.Vector3d.XAxis
            wanderMove.Rotate(randAngle, rg.Vector3d.ZAxis)
            
            # Apply the movement to the agent with the specified weight
            cartesianAgent.AddMove(wanderMove, 'Wander')
            cartesianAgent.Weights.Add(self.Weight)
        
        else:
            return  # No action if criteria are not met

# Instantiate CartWander behavior with provided weight and step inputs
behavior = CartWander(iWeight, iStep)
oBehavior = behavior
