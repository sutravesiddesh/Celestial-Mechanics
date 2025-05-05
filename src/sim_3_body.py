from vec3 import Vector3d
from ui import Simulation
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# Constants
G = 6.67e-11  # Gravitational constant
AU = 14959787070  # Astronomical unit in meters (scaled value)
energy_values = []  # List to track energy values over time

class body:
    """
    Represents a celestial body in the simulation, characterized by its position, velocity,
    mass, density, and color.
    """
    earth_mass = 5.972e24  # Mass of Earth for reference

    def __init__(self, pos, vel, mass, density, color):
        """
        Initializes a body with its position, velocity, mass, density, and color.
        """
        self.pos = pos  # Position of the body as a Vector3d
        self.vel = vel  # Velocity of the body as a Vector3d
        self.mass = mass  # Mass of the body
        self.density = density  # Density of the body
        self.color = color  # Color representation of the body
        self.prev_acceleration = Vector3d(0, 0, 0)  # Previous acceleration (unused)

    def __repr__(self):
        """
        String representation of the body object for debugging purposes.
        """
        return (f"body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")
    
    def force(self, other):
        """
        Calculates the gravitational force exerted on this body by another body.
        """
        r = other.pos - self.pos  # Vector from this body to the other body
        distance = r.mag()  # Magnitude of the distance vector
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Prevent division by zero
        force_magnitude = G * self.mass * other.mass / distance**2  # Gravitational force magnitude
        force_vector = r.norm() * force_magnitude  # Force vector direction and magnitude
        return force_vector
    
    def update(self, force: Vector3d, dt: float, bodies):
        """
        Updates the body's position and velocity based on the applied force and time step.
        """
        if self.mass == body.earth_mass:  
            return self  # Skip updating Earth

        acceleration = force / self.mass  # Calculate acceleration
        new_velocity = self.vel + acceleration * dt  # Update velocity
        new_position = self.pos + new_velocity * dt  # Update position

        return body(new_position, new_velocity, self.mass, self.density, self.color)


def compute_energy(bodies: List[body]):
    """
    Computes the total energy of the system, including kinetic and potential energy.
    """
    kinetic_energy = 0.0  # Initialize kinetic energy
    potential_energy = 0.0  # Initialize potential energy
    
    # Calculate kinetic energy for all bodies
    for body in bodies:
        kinetic_energy += 0.5 * body.mass * body.vel.mag() ** 2

    n = len(bodies)  # Number of bodies
    # Calculate potential energy between each pair of bodies
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].pos - bodies[i].pos  # Vector between two bodies
            distance = r.mag()  # Distance between bodies
            if distance == 0:
                continue  # Skip if bodies overlap
            potential_energy += -G * bodies[i].mass * bodies[j].mass / distance  # Gravitational potential energy
    
    total_energy = kinetic_energy + potential_energy  # Total energy of the system
    return total_energy


def update(bodies: List[body], dt: float):
    """
    Updates all bodies in the system based on gravitational forces and returns updated states.
    """
    updated_bodies = []  # List to store updated bodies
    
    # Update each body in the system
    for i in range(len(bodies)):
        body = bodies[i]
        
        total_force = Vector3d(0, 0, 0)  # Initialize total force
        for j in range(len(bodies)):
            if i != j:  # Skip self-interaction
                total_force += body.force(bodies[j])  # Accumulate forces from other bodies
        
        updated_body = body.update(total_force, dt, bodies)  # Update the body's state
        updated_bodies.append(updated_body)  # Store updated body
    
    return updated_bodies

def simulation_update(bodies, dt):
    """
    Updates the simulation state and records energy values over time.
    """
    global energy_values  # Access the global energy values list
    energy = compute_energy(bodies)  # Compute current energy of the system
    energy_values.append(energy)  # Append energy value to the list
    return update(bodies, dt)  # Update and return the new state of bodies


def calc_vel(mass, radius, orbital_radius):
    """
    Calculate the velocity required for a circular orbit given the mass of the central body,
    the distance from the central body, and the orbital radius.
    """
    return Vector3d(0, (G * mass / radius) ** 0.5, 0)  # Return velocity vector for circular orbit


def main():
    """
    Main function to set up and run the simulation.
    """
    # Sun initialization
    sun_pos = Vector3d(0, 0, 0)
    sun_vel = Vector3d(0, 0, 0)
    sun_mass = 1.9885e30  # Sun mass in kg
    sun_density = 1.408
    sun_color = (255, 255, 0)  # Yellow color for the Sun
    sun = body(sun_pos, sun_vel, sun_mass, sun_density, sun_color)

    # Earth initialization orbiting the Sun
    earth_distance_from_sun = 1.496 * pow(10, 11)  # 1 AU in meters
    vel_earth = calc_vel(sun_mass, earth_distance_from_sun, earth_distance_from_sun)  # Calculate Earth's orbital velocity
    earth_pos = Vector3d(earth_distance_from_sun, 0, 0)  # Initial position of Earth
    earth_mass = 5.9722e24  # Earth mass in kg
    earth_density = 5.513
    earth_color = (0, 0, 255)  # Blue color for Earth
    earth = body(earth_pos, vel_earth, earth_mass, earth_density, earth_color)

    # Moon initialization orbiting the Earth
    moon_distance_from_earth = 3.844 * pow(10, 8)  # Distance of Moon from Earth
    vel_moon_relative_to_earth = calc_vel(earth_mass, moon_distance_from_earth, moon_distance_from_earth)  # Calculate Moon's velocity around Earth

    # Calculate Moon's position and velocity relative to the Sun
    moon_pos_relative_to_sun = Vector3d(earth_distance_from_sun + moon_distance_from_earth, 0, 0)
    vel_moon_relative_to_sun = vel_earth + vel_moon_relative_to_earth  # Total velocity of Moon

    # Create Moon object
    moon_mass = 7.348 * pow(10, 22)  # Moon mass in kg
    moon_density = 3.934
    moon_color = (150, 150, 150)  # Grey color for Moon
    moon = body(moon_pos_relative_to_sun, vel_moon_relative_to_sun, moon_mass, moon_density, moon_color)

    # Print initial positions and velocities of celestial bodies
    print("Sun:", sun)
    print("Earth:", earth)
    print("Moon:", moon)
            
    # Initialize bodies list for simulation
    bodies = [sun, earth, moon]

    # Simulation setup
    simulation = Simulation(
        frame_rate=30,
        width=800,
        height=800,
        caption="3-Body Simulation",
        dt=10000,  # Time step for the simulation
        trail_length=500,
    )
    simulation.setup()  # Setup the simulation environment
    simulation.center = (0, 0)  # Center the view on the origin
    simulation.zoom = 1e-6  # Set initial zoom level

    # Run the simulation loop
    simulation.loop(initial_state=bodies, update=simulation_update)

    # Output energy values for analysis
    print("Energy values:", energy_values)

    # Plot the energy values over time
    plt.plot(energy_values)
    plt.xlabel("Time Step")
    plt.ylabel("Total Energy")
    plt.title("Energy Stability over Time with Verlet Integration")
    plt.show()

# Entry point for the program
main()
