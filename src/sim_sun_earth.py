from vec3 import Vector3d  # Importing Vector3d class for 3D vector operations
from ui import Simulation  # Importing Simulation class for UI handling
import numpy as np  # Importing NumPy for numerical operations
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting
from typing import List  # Importing List for type hinting

# Constants
G = 6.67e-11  # Gravitational constant
AU = 14959787070  # Astronomical unit in meters

energy_values = []  # List to store energy values during the simulation

class Body:
    """Class representing a celestial body in the simulation."""
    
    sun_mass = 1.9885e30  # Mass of the Sun in kilograms

    def __init__(self, pos: Vector3d, vel: Vector3d, mass: float, density: float, color: tuple):
        """
        Initializes a body with position, velocity, mass, density, and color.
        
        Args:
            pos: Position vector of the body.
            vel: Velocity vector of the body.
            mass: Mass of the body.
            density: Density of the body.
            color: Color representation of the body.
        """
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.density = density
        self.color = color
        self.prev_acceleration = Vector3d(0, 0, 0)  # Previous acceleration vector
    
    def __repr__(self):
        """Returns a string representation of the body object."""
        return (f"Body(pos={self.pos}, vel={self.vel}, mass={self.mass}, "
                f"density={self.density}, color={self.color})")
    
    def force(self, other: 'Body') -> Vector3d:
        """Computes the gravitational force exerted on this body by another body.
        
        Args:
            other: Another Body object.
        
        Returns:
            Force vector exerted by the other body.
        """
        r = other.pos - self.pos
        distance = r.mag()
        if distance == 0:
            raise ValueError("Distance cannot be zero")  # Check for zero distance
        force_magnitude = G * self.mass * other.mass / distance**2  # Gravitational force magnitude
        force_vector = r.norm() * force_magnitude  # Force vector
        return force_vector
    
    def update(self, force: Vector3d, dt: float, bodies: List['Body']) -> 'Body':
        """Updates the body's position and velocity based on the force applied.
        
        Args:
            force: Force vector applied to the body.
            dt: Time step for the update.
            bodies: List of all bodies in the simulation.
        
        Returns:
            Updated Body object.
        """
        if self.mass == Body.sun_mass:  
            return self  # Skip update for the Sun
        
        acceleration = force / self.mass  # Calculate acceleration
        new_velocity = self.vel + acceleration * dt  # Update velocity
        new_position = self.pos + new_velocity * dt  # Update position
        return Body(new_position, new_velocity, self.mass, self.density, self.color)  # Return new body state


def compute_energy(bodies: List[Body]) -> float:
    """Computes the total energy of a list of bodies (kinetic + potential energy).
    
    Args:
        bodies: List of Body objects.
    
    Returns:
        Total energy of the system.
    """
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


def update(bodies: List[Body], dt: float) -> List[Body]:
    """Updates the state of all bodies in the list based on forces.
    
    Args:
        bodies: List of Body objects.
        dt: Time step for the update.
    
    Returns:
        List of updated Body objects.
    """
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


def simulation_update(bodies: List[Body], dt: float) -> List[Body]:
    """Updates the simulation state and computes energy values.
    
    Args:
        bodies: List of Body objects.
        dt: Time step for the update.
    
    Returns:
        List of updated Body objects.
    """
    global energy_values  
    energy = compute_energy(bodies)  # Compute total energy
    energy_values.append(energy)  # Append energy to the list
    return update(bodies, dt)  # Update bodies


def main():
    """Main function to run the simulation."""
    # Sun
    sun_pos = Vector3d(0, 0, 0)  # Initial position of the Sun
    sun_vel = Vector3d(0, 0, 0)  # Initial velocity of the Sun
    sun_mass = 1.9885e30  # Mass of the Sun
    sun_density = 1.408  # Density of the Sun
    sun_color = (255, 255, 0)  # Color of the Sun
    sun = Body(sun_pos, sun_vel, sun_mass, sun_density, sun_color)  # Create Sun object

    # Earth
    earth_perihelion = 0.983 * AU  # Perihelion distance of Earth
    earth_aphelion = 1.017 * AU  # Aphelion distance of Earth
    semi_major_axis = (earth_perihelion + earth_aphelion) / 2  # Semi-major axis of Earth's orbit
    earth_pos = Vector3d(earth_perihelion, 0, 0)  # Initial position of Earth
    earth_mass = 5.9722e24  # Mass of Earth
    earth_density = 5.513  # Density of Earth
    earth_color = (0, 0, 255)  # Color of Earth
    earth_vel_mag = (G * sun_mass * (2 / earth_perihelion - 1 / semi_major_axis)) ** 0.5  # Orbital velocity of Earth
    earth_vel = Vector3d(0, earth_vel_mag, 0)  # Initial velocity of Earth
    earth = Body(earth_pos, earth_vel, earth_mass, earth_density, earth_color)  # Create Earth object

    print("Sun:", sun)  # Print Sun details
    print("\nEarth:", earth)  # Print Earth details
            
    force_on_earth = sun.force(earth)  # Calculate gravitational force on Earth
    print("\nGravitational force exerted by Sun on Earth:", force_on_earth)

    bodies = [sun, earth]  # List of bodies in the simulation
    dt = 60 * 60  # Time step in seconds

    earth_updated = earth.update(force_on_earth, dt, bodies)  # Update Earth's position and velocity
    print("\nUpdated Earth position and velocity after 1 hour:", earth_updated)

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

    # Set up dynamic plotting
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b-')  # Initialize line object for energy plot
    ax.set_xlim(0, 100)  # Set X-axis limit
    ax.set_ylim(min(energy_values) if energy_values else 0, max(energy_values) if energy_values else 1)  # Set Y-axis limit
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Total Energy")
    ax.set_title("Energy Stability over Time with Verlet Integration")

    # Run simulation with dynamic energy plotting
    for step in range(100):  # Run for a fixed number of iterations or until a condition is met
        bodies = simulation_update(bodies, dt)  # Update bodies
        
        # Update the energy plot
        if energy_values:  # Ensure there is data to plot
            line.set_xdata(range(len(energy_values)))
            line.set_ydata(energy_values)
            ax.set_ylim(min(energy_values), max(energy_values))  # Adjust Y limits based on data
            plt.pause(0.1)  # Pause to allow the plot to update

    plt.ioff()  # Disable interactive mode
    plt.show()  # Show final plot

# Execute the main function
main()
