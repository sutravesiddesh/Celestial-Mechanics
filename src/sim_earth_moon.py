from vec3 import Vector3d  # Importing Vector3d class for 3D vector operations
from ui import Simulation  # Importing Simulation class for UI handling
import numpy as np  # Importing NumPy for numerical operations
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting
from typing import List  # Importing List for type hinting

# Constants
G = 6.67e-11  # Gravitational constant
AU = 14959787070  # Astronomical unit in meters

energy_values = []  # List to store energy values during the simulation

class body:
    # Class representing a celestial body

    earth_mass = 5.972e24  # Mass of Earth in kilograms

    def __init__(self, pos, vel, mass, density, color):
        # Initializes a body with position, velocity, mass, density, and color
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.density = density
        self.color = color
        self.prev_acceleration = Vector3d(0, 0, 0)  # Previous acceleration vector
    
    def __repr__(self):
        # Returns a string representation of the body object
        return (f"body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")
    
    def force(self, other):
        # Computes the gravitational force exerted on this body by another body
        r = other.pos - self.pos
        distance = r.mag()
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Check for zero distance
        force_magnitude = G * self.mass * other.mass / distance**2  # Gravitational force magnitude
        force_vector = r.norm() * force_magnitude  # Force vector
        return force_vector
    
    def update(self, force: Vector3d, dt: float, bodies):
        # Updates the body's position and velocity based on the force applied
        if self.mass == body.earth_mass:  
            return self  # Skip update for Earth
        
        acceleration = force / self.mass  # Calculate acceleration

        new_velocity = self.vel + acceleration * dt  # Update velocity
        new_position = self.pos + new_velocity * dt  # Update position
        return body(new_position, new_velocity, self.mass, self.density, self.color)  # Return new body state


def compute_energy(bodies: List[body]):
    # Computes the total energy of a list of bodies (kinetic + potential energy)
    kinetic_energy = 0.0
    potential_energy = 0.0
    
    for body in bodies:
        kinetic_energy += 0.5 * body.mass * body.vel.mag() ** 2  # Kinetic energy calculation

    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].pos - bodies[i].pos  
            distance = r.mag()
            if distance == 0:
                continue  # Skip if distance is zero
            potential_energy += -G * bodies[i].mass * bodies[j].mass / distance  # Potential energy calculation
    
    total_energy = kinetic_energy + potential_energy  # Total energy
    return total_energy


def update(bodies: List[body], dt: float):
    # Updates the state of all bodies in the list based on forces
    updated_bodies = []
    
    for i in range(len(bodies)):
        body = bodies[i]
        
        total_force = Vector3d(0, 0, 0)  # Initialize total force
        for j in range(len(bodies)):
            if i != j:  
                total_force += body.force(bodies[j])  # Sum forces from other bodies
        
        updated_body = body.update(total_force, dt, bodies)  # Update body state
        updated_bodies.append(updated_body)  # Append updated body to the list
    
    return updated_bodies  # Return updated bodies


def simulation_update(bodies, dt):
    # Updates the simulation state and computes energy values
    global energy_values  
    energy = compute_energy(bodies)  # Compute total energy
    energy_values.append(energy)  # Append energy to the list
    return update(bodies, dt)  # Update bodies


def main():
    # Main function to run the simulation
    # Sun
    earth_pos = Vector3d(0, 0, 0)  # Initial position of Earth
    earth_vel = Vector3d(0, 0, 0)  # Initial velocity of Earth
    earth_mass = 5.972e24  # Mass of Earth
    earth_density = 1.0  # Density of Earth
    earth_color = (0, 0, 255)  # Color of Earth
    earth = body(earth_pos, earth_vel, earth_mass, earth_density, earth_color)  # Create Earth object

    # Moon
    moon_perigee = 362600 * 1e3  # Perigee distance of Moon
    moon_apogee = 405400 * 1e3  # Apogee distance of Moon
    semi_major_axis = (moon_perigee + moon_apogee) / 2  # Semi-major axis of Moon's orbit
    moon_pos = Vector3d(moon_perigee, 0, 0)  # Initial position of Moon
    moon_mass = 7.342e22  # Mass of Moon
    moon_vel_mag = (G * earth_mass * (2 / moon_perigee - 1 / semi_major_axis)) ** 0.5  # Orbital velocity of Moon
    moon_vel = Vector3d(0, moon_vel_mag, 0)  # Initial velocity of Moon
    moon_density = 1.0  # Density of Moon
    moon_color = (200, 200, 200)  # Color of Moon
    moon = body(moon_pos, moon_vel, moon_mass, moon_density, moon_color)  # Create Moon object

    print("Earth:", earth)  # Print Earth details
    print("\nMoon:", moon)  # Print Moon details
            
    force_on_moon = earth.force(moon)  # Calculate gravitational force on Moon
    print("\nGravitational force exerted by Earth on Moon:", force_on_moon)

    bodies = [earth, moon]  # List of bodies in the simulation
    dt = 60 * 60  # Time step in seconds

    moon_updated = moon.update(force_on_moon, dt, bodies)  # Update Moon's position and velocity
    print("\nUpdated Moon position and velocity after 1 hour:", moon_updated)

    # Simulation setup
    simulation = Simulation(
        frame_rate=30,
        width=800,
        height=800,
        caption="My Simulation",
        dt=10000,
        trail_length=500,
    )  # Create simulation object
    simulation.setup()  # Setup the simulation
    simulation.center = (0, 0)  # Center the simulation view
    simulation.zoom = 1e-6  # Set zoom level

    # Run simulation
    simulation.loop(initial_state=bodies, update=simulation_update)  # Start simulation loop

    print("Energy values:", energy_values)  # Print energy values list


    # Plot the energy values over time
    plt.plot(energy_values)  # Plot energy values
    plt.xlabel("Time Step")  # X-axis label
    plt.ylabel("Total Energy")  # Y-axis label
    plt.title("Energy Stability over Time with Verlet Integration")  # Plot title
    plt.show()  # Show the plot

main()  # Execute the main function
