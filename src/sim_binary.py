from vec3 import Vector3d 
from ui import Simulation
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# Constants
G = 6.67e-11  # Gravitational constant
AU = 14959787070  # Astronomical unit in meters (scaled value)
energy_values = []  # List to store energy values over time

class body:
    """Class representing a celestial body with position, velocity, mass, density, and color."""
    
    def __init__(self, pos, vel, mass, density, color):
        """Initialize a body with position, velocity, mass, density, and color."""
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.density = density
        self.color = color
    
    def __repr__(self):
        """Return a string representation of the body."""
        return (f"body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")
    
    def force(self, other):
        """Calculate the gravitational force exerted on this body by another body."""
        r = other.pos - self.pos  # Vector from this body to the other body
        distance = r.mag()  # Magnitude of the distance vector
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Prevent division by zero
        force_magnitude = G * self.mass * other.mass / distance**2  # Gravitational force magnitude
        force_vector = r.norm() * force_magnitude  # Force vector in the direction of r
        return force_vector
    
    def update(self, force: Vector3d, dt: float):
        """Update the body's position and velocity based on the force applied and time step."""
        acceleration = force / self.mass  # Calculate acceleration from force
        new_velocity = self.vel + acceleration * dt  # Update velocity
        new_position = self.pos + new_velocity * dt  # Update position

        return body(new_position, new_velocity, self.mass, self.density, self.color)


def compute_energy(bodies: List[body]):
    """Compute the total kinetic and potential energy of a list of bodies."""
    kinetic_energy = 0.0
    potential_energy = 0.0
    
    # Calculate kinetic energy for each body
    for body in bodies:
        kinetic_energy += 0.5 * body.mass * body.vel.mag() ** 2

    n = len(bodies)  # Number of bodies
    # Calculate potential energy between pairs of bodies
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].pos - bodies[i].pos  # Vector between bodies
            distance = r.mag()  # Magnitude of the vector
            if distance == 0:
                continue  # Skip if bodies overlap
            potential_energy += -G * bodies[i].mass * bodies[j].mass / distance  # Gravitational potential energy
    
    total_energy = kinetic_energy + potential_energy  # Total energy is the sum of kinetic and potential energy
    return total_energy


def update(bodies: List[body], dt: float):
    """Update the positions and velocities of all bodies in the list."""
    updated_bodies = []
    
    for i in range(len(bodies)):
        body = bodies[i]  # Current body
        
        total_force = Vector3d(0, 0, 0)  # Initialize total force vector
        for j in range(len(bodies)):
            if i != j:  # Don't calculate force on itself
                total_force += body.force(bodies[j])  # Accumulate forces from all other bodies
        
        updated_body = body.update(total_force, dt)  # Update the current body
        updated_bodies.append(updated_body)  # Add the updated body to the list
    
    return updated_bodies

def simulation_update(bodies, dt):
    """Update the simulation state, computing energy and updating bodies."""
    global energy_values  # Use the global energy_values list
    energy = compute_energy(bodies)  # Compute current energy
    energy_values.append(energy)  # Append energy to the list
    return update(bodies, dt)  # Update bodies


def calc_velocity(m1, m2, r):
    """
    Calculate the velocity for two bodies in a binary star system.
    
    Args:
        m1: Mass of the first body.
        m2: Mass of the second body.
        r: Distance between the two bodies.
    
    Returns:
        The velocity required for a stable orbit.
    """
    v = (G * (m1 + m2) / r) ** 0.5  # Calculate orbital velocity
    return v


def main():
    # Parameters for the binary star system
    star1_mass = 1.9885e30  # Mass of star 1 in kg (same as Sun)
    star2_mass = 1.9885e30  # Mass of star 2 in kg (same as Sun)
    distance_between_stars = 1 * AU  # Separation distance of 1 AU

    # Initial positions of the two stars (opposite sides of their center of mass)
    star1_pos = Vector3d(-distance_between_stars / 2, 0, 0)
    star2_pos = Vector3d(distance_between_stars / 2, 0, 0)

    # Velocities calculated to ensure stable orbits around the common center of mass
    velocity_magnitude = calc_velocity(star1_mass, star2_mass, distance_between_stars)

    # Star 1 velocity is in the positive y direction, and Star 2 in the negative y direction
    star1_vel = Vector3d(0, velocity_magnitude * (star2_mass / (star1_mass + star2_mass)), 0)
    star2_vel = Vector3d(0, -velocity_magnitude * (star1_mass / (star1_mass + star2_mass)), 0)

    # Colors for the stars
    star1_color = (255, 255, 0)  # Yellow
    star2_color = (255, 0, 0)    # Red

    # Creating star objects
    star1 = body(star1_pos, star1_vel, star1_mass, 1.408, star1_color)
    star2 = body(star2_pos, star2_vel, star2_mass, 1.408, star2_color)

    # Print initial positions and velocities
    print("Star 1:", star1)
    print("Star 2:", star2)
            
    # Initial bodies list
    bodies = [star1, star2]
    dt = 60 * 60  # Time step of 1 hour

    # Simulation setup
    simulation = Simulation(
        frame_rate=30,  # Frames per second
        width=800,      # Window width in pixels
        height=800,     # Window height in pixels
        caption="Binary Star System",  # Window title
        dt=10000,  # Time step for simulation
        trail_length=500,  # Length of trail for the stars
    )
    simulation.setup()  # Prepare the simulation environment
    simulation.center = (0, 0)  # Center of the simulation
    simulation.zoom = 1e-6  # Zoom level for the simulation

    # Run simulation
    simulation.loop(initial_state=bodies, update=simulation_update)

    print("Energy values:", energy_values)  # Check if this list is populated

    # Plot the energy values over time
    plt.plot(energy_values)  # Plot energy values
    plt.xlabel("Time Step")  # X-axis label
    plt.ylabel("Total Energy")  # Y-axis label
    plt.title("Energy Stability over Time in Binary Star System")  # Title of the plot
    plt.show()  # Display the plot


main()  # Run the main function
