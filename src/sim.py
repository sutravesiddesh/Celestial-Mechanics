from vec3 import Vector3d
from ui import Simulation
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# Constants
G = 6.67e-11  # Gravitational constant in m^3 kg^-1 s^-2.
AU = 14959787070  # 1 Astronomical Unit in meters.

# Class representing a celestial body with position, velocity, mass, density, and color attributes.
class body:
    planet_mass = 5.98e24  # Mass of Earth in kg (used for comparison).

    def __init__(self, pos, vel, mass, density, color):
        # Initialize body with position, velocity, mass, density, and color.
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.density = density
        self.color = color
        self.prev_acceleration = Vector3d(0, 0, 0)  # Initialize previous acceleration as zero.

    def __repr__(self):
        # Return a string representation of the body instance.
        return (f"body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")

    # Calculate the gravitational force exerted on the body by another body.
    def force(self, other):
        r = other.pos - self.pos  # Distance vector between two bodies.
        distance = r.mag()  # Magnitude of the distance vector.
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Raise an error for zero distance.
        force_magnitude = G * self.mass * other.mass / distance**2  # Calculate force magnitude.
        force_vector = r.norm() * force_magnitude  # Calculate the force vector.
        return force_vector

    # Update the body's position and velocity based on the applied force and time step.
    def update(self, force: Vector3d, dt: float, bodies):
        if self.mass == body.planet_mass:
            return self  # If body is the planet, it remains stationary.

        acceleration = force / self.mass  # Calculate the acceleration.
        new_velocity = self.vel + acceleration * dt  # Calculate the new velocity.
        new_position = self.pos + new_velocity * dt  # Calculate the new position.
        
        return body(new_position, new_velocity, self.mass, self.density, self.color)

# Function to compute the total energy (kinetic + potential) of all bodies in the system.
def compute_energy(bodies: List[body]):
    kinetic_energy = 0.0  # Initialize kinetic energy.
    potential_energy = 0.0  # Initialize potential energy.

    # Calculate kinetic energy for each body.
    for body in bodies:
        kinetic_energy += 0.5 * body.mass * body.vel.mag() ** 2

    n = len(bodies)
    # Calculate potential energy between each pair of bodies.
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].pos - bodies[i].pos  # Distance vector between two bodies.
            distance = r.mag()  # Magnitude of the distance.
            if distance == 0:
                continue  # Skip if distance is zero.
            potential_energy += -G * bodies[i].mass * bodies[j].mass / distance  # Potential energy formula.

    total_energy = kinetic_energy + potential_energy  # Total energy of the system.
    return total_energy

# Function to update the state of all bodies over a time step dt.
def update(bodies: List[body], dt: float):
    updated_bodies = []  # List to store updated body states.

    for i in range(len(bodies)):
        body = bodies[i]
        total_force = Vector3d(0, 0, 0)  # Initialize total force on current body.

        # Calculate total force exerted on the current body by all other bodies.
        for j in range(len(bodies)):
            if i != j:  # Avoid self-interaction.
                total_force += body.force(bodies[j])

        # Update body based on calculated force and add to updated list.
        updated_body = body.update(total_force, dt, bodies)
        updated_bodies.append(updated_body)

    return updated_bodies

# Main function to set up and run the simulation.
def main():
    # Initialize the planet (Earth).
    planet_pos = Vector3d(0, 0, 0)  # Position at the origin.
    planet_vel = Vector3d(0, 0, 0)  # Stationary velocity.
    planet_mass = 5.98e24  # Mass of Earth.
    planet_density = 1.0  # Arbitrary density.
    planet_color = (0, 0, 255)  # Blue color for planet.
    planet = body(planet_pos, planet_vel, planet_mass, planet_density, planet_color)

    # Initialize a satellite orbiting the planet.
    satellite_pos = Vector3d(3.5e8, 0, 0)  # Position 3.5e8 meters from the planet.
    satellite_vel_mag = (G * planet_mass / satellite_pos.x) ** 0.5  # Orbital speed.
    satellite_vel = Vector3d(0, satellite_vel_mag, 0)  # Initial velocity perpendicular to position.
    satellite_mass = 1.23e21  # Arbitrary satellite mass.
    satellite_density = 1.0  # Arbitrary density.
    satellite_color = (200, 200, 200)  # Gray color for satellite.
    satellite = body(satellite_pos, satellite_vel, satellite_mass, satellite_density, satellite_color)

    print("Planet:", planet)
    print("\nSatellite:", satellite)

    # Calculate and print the gravitational force between planet and satellite.
    force_on_satellite = planet.force(satellite)
    print("\nGravitational force exerted by Earth on Satellite:", force_on_satellite)

    bodies = [planet, satellite]  # List of celestial bodies in the simulation.
    dt = 60 * 60  # Time step of 1 hour.

    # Update and print satellite's position and velocity after 1 hour.
    satellite_updated = satellite.update(force_on_satellite, dt, bodies)
    print("\nUpdated Satellite position and velocity after 1 hour:", satellite_updated)

    # Simulation setup using the Simulation class from ui module.
    simulation = Simulation(
        frame_rate=30,  # Frame rate for the simulation.
        width=800,  # Width of the simulation window.
        height=800,  # Height of the simulation window.
        caption="My Simulation",  # Window caption.
        dt=10000,  # Simulation time step.
        trail_length=500,  # Length of trail left by the bodies.
    )
    simulation.setup()  # Initialize the simulation.
    simulation.center = (0, 0)  # Center of the simulation view.
    simulation.zoom = 1e-6  # Zoom factor.

    # Run the simulation with the initial state and update function.
    simulation.loop(initial_state=bodies, update=update)

# Execute the main function to start the simulation.
main()
