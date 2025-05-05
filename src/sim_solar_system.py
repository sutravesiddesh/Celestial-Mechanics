from vec3 import Vector3d
from ui import Simulation
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# Constants for gravitational calculations
G = 6.67e-11  # Gravitational constant
AU = 14959787070  # Astronomical Unit in meters

# To store the energy values over time
energy_values = []

class body:
    # Class variable for Sun's mass
    sun_mass = 1.9885e30  

    def __init__(self, pos, vel, mass, density, color):
        # Initialize the attributes of the celestial body
        self.pos = pos         # Position as a Vector3d
        self.vel = vel         # Velocity as a Vector3d
        self.mass = mass       # Mass of the body
        self.density = density  # Density of the body
        self.color = color      # Color of the body
        self.prev_acceleration = Vector3d(0, 0, 0)  # Previous acceleration (not used in current logic)
    
    def __repr__(self):
        # String representation for debugging
        return (f"body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")
    
    def force(self, other):
        # Calculate gravitational force exerted by another body
        r = other.pos - self.pos  # Vector from this body to the other
        distance = r.mag()  # Magnitude of the distance vector
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Prevent division by zero
        # Gravitational force magnitude and direction
        force_magnitude = G * self.mass * other.mass / distance**2
        force_vector = r.norm() * force_magnitude  # Normalize the distance vector and scale by force magnitude
        return force_vector
    
    def update(self, force: Vector3d, dt: float, bodies):
        # Update the body's position and velocity based on the applied force
        if self.mass == body.sun_mass:  
            return self  # Do not update the Sun's position
        
        acceleration = force / self.mass  # Calculate acceleration
        new_velocity = self.vel + acceleration * dt  # Update velocity
        new_position = self.pos + new_velocity * dt  # Update position
        
        # Create and return a new body instance with updated properties
        return body(new_position, new_velocity, self.mass, self.density, self.color)

def compute_energy(bodies: List[body]):
    # Compute the total energy of the system (kinetic + potential)
    kinetic_energy = 0.0
    potential_energy = 0.0
    
    for body in bodies:
        kinetic_energy += 0.5 * body.mass * body.vel.mag() ** 2  # Kinetic energy calculation

    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].pos - bodies[i].pos  # Distance vector between two bodies
            distance = r.mag()  # Magnitude of the distance
            if distance == 0:
                continue  # Avoid division by zero
            potential_energy += -G * bodies[i].mass * bodies[j].mass / distance  # Gravitational potential energy
    
    total_energy = kinetic_energy + potential_energy  # Total energy
    return total_energy

def update(bodies: List[body], dt: float):
    # Update all bodies in the simulation
    updated_bodies = []
    
    for i in range(len(bodies)):
        body = bodies[i]
        
        total_force = Vector3d(0, 0, 0)  # Reset total force for the current body
        for j in range(len(bodies)):
            if i != j:  # Skip self-interaction
                total_force += body.force(bodies[j])  # Sum forces from all other bodies
        
        updated_body = body.update(total_force, dt, bodies)  # Update body with total force
        updated_bodies.append(updated_body)  # Append updated body to the list
    
    return updated_bodies

def simulation_update(bodies, dt):
    global energy_values  # Access the global energy values list
    energy = compute_energy(bodies)  # Compute energy at current state
    energy_values.append(energy)  # Store energy value
    return update(bodies, dt)  # Update the simulation state

def main():
    # Initialize Sun's properties
    sun_pos = Vector3d(0, 0, 0)  # Sun position
    sun_vel = Vector3d(0, 0, 0)  # Sun velocity
    sun_mass = 1.9885e30  # Sun mass in kg
    sun_density = 1.408  # Sun density
    sun_color = (255, 255, 0)  # Sun color (yellow)
    sun = body(sun_pos, sun_vel, sun_mass, sun_density, sun_color)

    # Data for planets
    planets_data = [
        {"name": "Mercury", "perihelion": 0.307 * AU, "aphelion": 0.467 * AU, "mass": 3.3011e23, "density": 5.427, "colour": (169, 169, 169)},
        {"name": "Venus", "perihelion": 0.718 * AU, "aphelion": 0.728 * AU, "mass": 4.8675e24, "density": 5.243, "colour": (255, 228, 196)},
        {"name": "Earth", "perihelion": 0.983 * AU, "aphelion": 1.017 * AU, "mass": 5.9722e24, "density": 5.513, "colour": (0, 0, 255)},
        {"name": "Mars", "perihelion": 1.381 * AU, "aphelion": 1.666 * AU, "mass": 6.4171e23, "density": 3.934, "colour": (255, 0, 0)},
        {"name": "Jupiter", "perihelion": 4.951 * AU, "aphelion": 5.457 * AU, "mass": 1.8982e27, "density": 1.326, "colour": (165, 42, 42)},
        {"name": "Saturn", "perihelion": 9.041 * AU, "aphelion": 10.12 * AU, "mass": 5.6834e26, "density": 0.687, "colour": (210, 180, 140)},
        {"name": "Uranus", "perihelion": 18.29 * AU, "aphelion": 20.1 * AU, "mass": 8.6810e25, "density": 1.270, "colour": (0, 255, 255)},
        {"name": "Neptune", "perihelion": 29.81 * AU, "aphelion": 30.33 * AU, "mass": 1.0241e26, "density": 1.638, "colour": (0, 0, 139)},
    ]

    bodies = [sun]  # Initialize the bodies list with the Sun

    for planet in planets_data:
        # For each planet, calculate its semi-major axis and initial velocity
        semi_major_axis = (planet["perihelion"] + planet["aphelion"]) / 2
        velocity_magnitude = (G * sun_mass * (2 / planet["perihelion"] - 1 / semi_major_axis)) ** 0.5
        initial_position = Vector3d(planet["perihelion"], 0, 0)  # Starting position
        initial_velocity = Vector3d(0, velocity_magnitude, 0)  # Starting velocity (tangential)
        
        # Create a new planet body and append to the bodies list
        new_planet = body(initial_position, initial_velocity, planet["mass"], planet["density"], planet["colour"])  
        bodies.append(new_planet)

    # Setup the simulation
    simulation = Simulation(
        frame_rate=30,
        width=800,
        height=800,
        caption="My Simulation",
        dt=3000,
        trail_length=500,
    )
    simulation.setup()  # Initialize the simulation
    simulation.center = (0, 0)  # Center the view
    simulation.zoom = 1e-6  # Set zoom level
    
    # Start the simulation loop with the bodies and update function
    simulation.loop(initial_state=bodies, update=simulation_update)

    # Print energy values for debugging
    print("Energy values:", energy_values)  

    # Plot the energy values over time
    plt.plot(energy_values)
    plt.xlabel("Time Step")
    plt.ylabel("Total Energy")
    plt.title("Energy Stability over Time with Verlet Integration")
    plt.show()

# Run the main function to start the simulation
main()