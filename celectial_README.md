# Celestial Mechanics

The goal of this session is to
- learn how to read JSON data and manipulate deep dictionaries
- write and use Python classes
- have some fun with $n$-body simulations of celestial objects

## Table of content
- [_Requirements_](#requirements-toc)
- [_Upload your work to the LMS_](#upload-your-work-to-the-lms-toc)
- [_Part 1. Manipulating JSON and dictionaries_](parts/analysing_json.md)
  - [_Introduction to the data_](parts/analysing_json.md#introduction-to-the-data-toc)
  - [_Q1.1_](parts/analysing_json.md#question-11-toc)
  - [_Q1.2_](parts/analysing_json.md#question-12-toc)
  - [_Q1.3_](parts/analysing_json.md#question-13-toc)
  - [_Q1.4_](parts/analysing_json.md#question-14-toc)
  - [_Q1.5_](parts/analysing_json.md#question-15-toc)
  - [_Q1.6_](parts/analysing_json.md#question-16-toc)
  - [_Q1.7_](parts/analysing_json.md#question-17-toc)
- [_Part 2. Celestial Mechanics simulation_](parts/simulation.md)
  - [_Q2.1_](parts/simulation.md#question-21-toc)
  - [_Q2.2_](parts/simulation.md#question-22-toc)
  - [_Q2.3_](parts/simulation.md#question-23-toc)
  - [_Q2.4_](parts/simulation.md#question-24-toc)
  - [_Q2.5_ (_optional_)](parts/simulation_energy.md#question-25-toc)
  - [_Q2.6_ (_optional_)](parts/simulation_energy.md#question-26-toc)
  - [_Q2.7_](parts/simulation_systems.md#question-27-toc)
  - [_Q2.8_ (_optional_)](parts/simulation_systems.md#question-28-toc)

![Languages](./assets/celestial_mechanics_medieval_artwork.jpg)

---

## Requirements [[toc](#table-of-content)]
you should have completed the following notebooks before starting this project:
- the [basics of the Python language](https://gitlab.isae-supaero.fr/mae/learn-python#the-basics-of-the-language)
- how to [read and write to text files and write functions](https://gitlab.isae-supaero.fr/mae/learn-python#reading-text-files-and-writing-functions)
- how to [read JSON and manipulate dictionaries](https://gitlab.isae-supaero.fr/mae/learn-python#manipulating-json-and-dictionaries)
- the basics of [object-oriented programming](https://gitlab.isae-supaero.fr/mae/learn-python#object-oriented-programming)

## Upload your work to the LMS [[toc](#table-of-content)]
- open a terminal
- go into the folder containing your project
- use the `zip` command to compress your project
```shell
zip -r project.zip . -x "venv/**" ".git/**"
```
- upload the ZIP archive to the [LMS](https://lms.isae.fr/mod/assign/view.php?id=116612&action=editsubmission)

---
---
> [go to questions](parts/analysing_json.md)

# Part 1. Manipulating JSON and dictionaries [[toc](../README.md#table-of-content)]

During this section, you will use an extracted dataset from the _NASA's Near Earth Object Web Service_ (NeoWs).
You will have to retrieve information about _Near-Earth Objects_ (NEOs) from a JSON file.

> :exclamation: **Important**
>
> your code for this question should go in a source file called `neos.py` and
> should run without issues by calling the following command in a terminal
> ```shell
> python neos.py
> ```
>
> so don't forget to create this new `neos.py` file :wink:

### Introduction to the data [[toc](../README.md#table-of-content)]

The JSON data is organized hierarchically. Below is a simplified example of what the JSON format for _NEO_ data might look like:

```json
{
    "element_count": 10, # Total number of NEOs in the response
    "near_earth_objects": {
        "2023-10-16": [ # Date in YYYY-MM-DD format
            {
                "links": {
                    "self": "URL to detailed NEO information"
                },
                "id": "12345", # Unique identifier for the NEO
                "name": "Apophis", # Name of the NEO
                "nasa_jpl_url": "URL to JPL's page for this NEO",
                "absolute_magnitude_h": 19.7, # Absolute magnitude
                "estimated_diameter": {
                    "kilometers": {
                        "estimated_diameter_min": 0.186,
                        "estimated_diameter_max": 0.416
                    }
                },
                "is_potentially_hazardous_asteroid": False, # Indicates if the NEO is hazardous
                "close_approach_data": [
                    {
                        "close_approach_date": "2023-10-16", # Date of closest approach
                        "miss_distance": {
                            "astronomical": "0.1 AU", # Miss distance in astronomical units
                            "kilometers": "15,000,000" # Miss distance in kilometers
                        },
                        "relative_velocity": "10.5 km/s" # Relative velocity in km/s
                    }
                ]
            },
            # More NEOs for the same date
        ],
        # More dates with NEOs
    }
}
```

In this example:
- `$.element_count` tells you the total number of _NEOs_ in the file.
- `$.near_earth_objects` contains _NEO_ data organized by date.
- each date inside `$.near_earth_objects` is a key in the format `YYYY-MM-DD`.
- for each _NEO_ on a given date, you have information about its ID, name, URL links, absolute magnitude, estimated diameter, hazard status, and close approach data.

### Question 1.1 [[toc](../README.md#table-of-content)]
#### Creating a NEO class
Define a Python class named `NearEarthObject` that represents a _Near-Earth Object_.
The class should have the following attributes:
- `name`: The name of the _NEO_.
- `diameter`: The diameter of the _NEO_ in meters.
- `is_potentially_hazardous`: A boolean value indicating whether the _NEO_ is potentially hazardous.

Your class should also have a constructor to initialize these attributes.

```python
# You can see how to use the NEO class here
neos = [
    NearEarthObject("(2022 UY)", 47.8674154419, False),
    NearEarthObject("(2022 WL)", 36.3111479288, False),
    NearEarthObject("(2022 WT11)", 85.9092601232, False),
    NearEarthObject("(2023 KD1)", 74.1378485408, False),
    NearEarthObject("(2023 KQ5)", 1066.694310755, False),
    NearEarthObject("(2023 LR1)", 1330.5768979725, False),
    NearEarthObject("(2023 MK1)", 381.979432159, True),
    NearEarthObject("337558 (2001 SG262)", 809.1703835499, True),
    NearEarthObject("(2007 EC)", 210.8822267643, False),
    NearEarthObject("(2017 HG)", 34.201092472, False),
    NearEarthObject("(2017 TM6)", 130.0289270043, False),
    NearEarthObject("(2017 TT6)", 85.9092601232, False),
    NearEarthObject("(2018 UC)", 39.2681081809, False),
    NearEarthObject("(2019 CE4)", 1432.3197447269, True),
    NearEarthObject("(2019 UZ3)", 23.6613750114, False),
    NearEarthObject("(2022 QQ3)", 205.1351006288, False),
    NearEarthObject("(2023 KH4)", 23.4444462214, False),
    NearEarthObject("523585 (1998 MW5)", 986.3702813054, False),
    NearEarthObject("(1998 HH49)", 322.1365318908, True),
    NearEarthObject("(2004 TP1)", 430.566244241, True),
]
```

### Question 1.2 [[toc](../README.md#table-of-content)]
#### Reading JSON data and storing _NEO_ data

Write a function to read the JSON file and return a list of `NearEarth` objects.
For the diameter, use `estimated_diameter_max`, of course, in meters.
> :bulb: **Note**
>
> This is a non-blocking question. If you don't succeed to read data from the JSON file, you can continue with the next question and use the given dataset from [Question 1.1](#question-11-toc).

### Question 1.3 [[toc](../README.md#table-of-content)]
#### Filtering _NEOs_

Write a function `filter_neos` to filter _NEOs_ based on specific criteria. This function takes the following parameters:
- `neos`: list of `NearEarthObject` objects
- `min_diameter`: Minimum diameter (in meters) that a _NEO_ must have to be considered.
- `is_potentially_hazardous`: A boolean value to filter _NEOs_ that are potentially hazardous or not.

The `filter_neos` method should return a new list of `NearEarthObject` objects that meet the specified criteria.
Call this function by giving the `neos` list generated from the previous questions (can be the list from either [Question 1.1](#question-11-toc) or [Question 1.2](#question-12-toc)).
Find the other parameters to print the number of `neos` that are potentially hazardous objects and have a diameter bigger than 400m.

> :bulb: **Note**
>
> To get the number of elements in a `list`, use the `len` function

### Question 1.4 [[toc](../README.md#table-of-content)]
#### Create an analyser

Write a Python class named `NeoAnalyzer` that is responsible for computing additional information about _NEOs_.
The class should have the following methods:
- `__init__(self, neos)`: Constructor that takes a list of `NearEarthObject` objects.
- `average_diameter(self)`: A method to calculate the average diameter of all _NEOs_ and return it.
- `count_potentially_hazardous(self)`: A method to count and return the number of _NEOs_ that are potentially hazardous.

### Question 1.5 [[toc](../README.md#table-of-content)]
#### Analyse the data

Create an instance of the `NeoAnalyzer` class, passing the neos list as a parameter.
Compute and display the average diameter and the count of potentially hazardous _NEOs_ using the `NeoAnalyzer` methods.

> :bulb: **Note**
>
> You have to give to the constructor the `neos` list generated from the previous questions.
> It can be the list generated from the [Question 1.1](#question-11-toc) or the [Question 1.2](#question-12-toc).

### Question 1.6 [[toc](../README.md#table-of-content)]
#### Implementing Comparison for Sorting NEOs

Go back to your `NearEarthObject` class and implement the `__lt__` method (less than) that compares `NearEarthObject` objects and allows you to sort them in ascending order by their `diameter`.

### Question 1.7 [[toc](../README.md#table-of-content)]
#### Sorting data for faster analyse

Create a list of `NearEarthObject` sorted by `diameter`, and print the diameter and the name of the smallest _NEO_.
> :pray: **Help**
>
> The `sorted` function returns a sorted list:
> ```python
> assert (sorted([4, 1, 3, 2]) == [1, 2, 3, 4])
> ```

---
---
> [go to next questions](simulation.md)

# Part 2. Celestial Mechanics simulation [[toc](../README.md#table-of-content)]

Reading data about celestial objects gathered by NASA is great, but what if we
were able to compute the trajectories of any celestial object ourselves and show
their movements in a little simulation?

This second part will be dedicated to this very question!

> :exclamation: **Important**
>
> your code for this part should go in a source file called `sim.py` and
> should run without issues when calling the following command in a terminal
> ```shell
> python sim.py
> ```
>
> so don't forget to create this new `sim.py` file :wink:

### Question 2.1 [[toc](../README.md#table-of-content)]
#### Defining celestial objects

The simplest and only object that needs to be manipulated in such a simulation
will be refered to as a _body_.

> :bulb: **Note**
>
> some of you might be familiar with the $3$-body problem, these are the bodies
> we talk about!

Here, a _body_ is anything that has a _position_ in 3D space, a _velocity_ in
3D space, a _mass_ and a _density_.
For the sake of rendering these bodies on screen, we will add a _color_ property
to them.

:file_folder: Create a file `sim.py`.

:pencil: Write a class called `Body` with the fields mentionned above:
- `pos` is a vector in 3D space
- `vel` is a vector in 3D space
- `mass` is a real number, the _mass_ expressed in $\text{kg}$
- `density` is a real number, the _density_ expressed in $\text{kg}.\text{m}^{-3}$
- `color` is a tuple of three integers between $0$ and $255$, e.g. _red_,
  _green_ and _blue_ would be `(255, 0, 0)`, `(0, 255, 0)` and `(0, 0, 255)`
  respectively

:pencil: Let's define a simple 2-body system with a planet and one moon:
- the planet will be a _blue_ body at the _center_ of the referential with
  _no speed_, a mass of $5.98 \times 10^{24}$ $\text{kg}$ and a density of
  $1.0$ $\text{kg}.\text{m}^{-3}$.
- the moon will be a _grey_ ($(200, 200, 200)$ should be ok) body with a
  mass of $1.23 \times 10^{21}$ $\text{kg}$ and a density of $1.0$
  $\text{kg}.\text{m}^{-3}$. It should be $3.5 \times 10^{8}$ $\text{m}$ away from
  the _planet_ and have an initial speed that puts it in a circular or
  elliptical orbit around the _planet_.

> :bulb: **Note**
>
> in order to put a body $A$ in a circular orbit around another body $B$ of
> mass $M$, respectively the satellite and the Earth in the image below, where
> the distance between $A$ and $B$ is $r$ and $B$ has no speed, then the initial
> velocity vector $v$ of $A$ should
> - be orthogonal to the vector between $A$ and $B$
> - have a magnitude of $\sqrt{\frac{GM}{r}}$
>
> <img src="../assets/circular_orbit.jpg" alt="circular orbit" width="200"/>
>
> > image from [_Name Some of the Functions of Earth Orbiting Satellites_](https://terry-yersblogknapp.blogspot.com/2022/05/name-some-of-functions-of-earth.html)
>
> slightly changing this initial speed will cause $A$ to enter an elliptical
> orbit around $B$.

> :bulb: **Note**
>
> the value of the gravitational constant $G$ is
> $6.67 \times 10^{-11}$ $\text{N}.\text{m}^{2}.\text{kg}^{-2}$

> :bulb: **Note**
>
> to represent 3D vectors, you can use the `Vector3D` class from the `src.vec3`
> module provided with the class material.

### Question 2.2 [[toc](../README.md#table-of-content)]
#### May the force be with you

Now that we have a few bodies, we can compute the force applied to each pair of them.

The force applied by a body $A$ of mass $m_{A}$ at position $\vec{p_A}$ to a body $B$
of mass $m_{B}$ at position $\vec{p_B}$ is expressed as

$$\vec{F_{A \rightarrow B}} = - G \frac{m_{A}m_{B}}{||\vec{r}||^2}\frac{\vec{r}}{||\vec{r}||}$$
where $\vec{r}$ is the vector from $A$ to $B$

<img src="../assets/attractive-forces.png" alt="gravitational attraction" width="500"/>

:pencil: Write a method `force` for the class `Body` that takes another `Body`
as parameter and returns the force between the two bodies as a 3D vector.

### Question 2.3 [[toc](../README.md#table-of-content)]
#### Your system is out of date

Now that we can compute the forces between all the bodies in our system, we can
update their velocities and positions using the second law of Newton which
states
$$\vec{F} = m\vec{a}$$
where $\vec{F}$ is the force applied to a body, $m$ is its mass and $\vec{a}$ its
acceleration.

As a starter, the simplest integration scheme will be used, i.e. the
_forward Euler method_.
$$\vec{v_{t+1}} = \vec{v_{t}} + \text{dt} \times \vec{a_{t}}$$
$$\vec{p_{t+1}} = \vec{p_{t}} + \text{dt} \times \vec{v_{t+1}}$$

:pencil: Write a method `update` for the class `Body` that takes a `force` as a
3D vector and time step `dt` and returns a new `Body` with it's velocity and
position updated.

### Question 2.4 [[toc](../README.md#table-of-content)]
#### Preparing the simulation

In order to simulation the system and see the bodies in action, we will be using
the `Simulation` class from the `src.ui` module.

> :bulb: **Note**
>
> see [this document](src/README.md) for more information about the `src.ui` module

:pencil: Define `bodies` as a list containing our two bodies from [_Question 2.1_](#question-21-toc).

:pencil: Define `update` as a function that takes a list of bodies and a time step `dt`
and returns a list with the same number of bodies, all of them with their
velocities and positions updated.

---
---
> [go to next questions](simulation_energy.md)


### Question 2.5 [[toc](../README.md#table-of-content)] (_optional_)
#### The stability of energy

Something that might not be apparent with the simulations alone is the so called
_stability_ of the integration scheme used.

:warning: Spoiler alert: the _forward Euler method_ is not very stable...

The energy of a system of $n$ bodies at instant $t$ can be defined as the sum of
the kinetic energies of all the bodies and the pair-wise gravitational potential
energies:
$$E_{\text{tot}}(t) = \sum\limits_{i = 1}^{n} E_{\text{kin}, i}(t) + \sum\limits_{1 \leq i \lt j \leq n} E_{\text{pot}, i, j}(t)$$
where
$$E_{\text{kin}, i}(t) = \frac{1}{2}m_i||\vec{v_i}(t)||^2$$
and
$$E_{\text{pot}, i, j}(t) = -G\frac{m_i m_j}{||\vec{p_i}(t) - \vec{p_j}(t)||}$$

:pencil: Write a function `compute_energy` that takes a list of _bodies_ and computes the
total energy of the system.

:question: Run a simulation, record the energy at each time step and plot it using
`matplotlib` at the end, what do you observe? Is that expected?

### Question 2.6 [[toc](../README.md#table-of-content)] (_optional_)
#### Making our system more stable

Another simple integration scheme is the _Verlet_ one.

Instead of simply updating the speed from the acceleration and the position from
the speed as in [_Question 2.3_](simulation.md#question-23-toc), the _Verlet_ method will
first update the position with the acceleration and then update the speed with
the average of the first acceleration and the new acceleration after the update
on the position:
$$\vec{p_{t+1}} = \vec{p_{t}} + \text{dt} \times \vec{v_{t}} + \frac{\text{dt}^2}{2} \times \vec{a_{t}}$$
$$\vec{v_{t+1}} = \vec{v_{t}} + \text{dt} \times \frac{\vec{a_{t}} + \vec{a_{t+1}}}{2}$$

:pencil: Modify the `update` method of the `Body` class and plot the total energy of the
system again.

> :bulb: **Hint**
>
> in order to simplify the code, you can add a new attribute to the `Body` class, to store the
> previous acceleration, reuse in the computation of the new velocity and then store the new value
> of the acceleration.

:question: What do you see now? Does it look any better? (it should)

> :bulb: **Note**
>
> you might need to pass the list of all the bodies to `update` now...

---
---
> [go to next questions](simulation_systems.md)

### Question 2.7 [[toc](../README.md#table-of-content)]
#### Let's build some systems

> :bulb: **Note**
>
> one _Astronomic Unit_ is roughly the distance between the Earth and the Sun
> and is equal to $149597870700$ $\text{m}$.
>
>
> The orbit of any body $B$ around another body $A$ is given by the _periapsis_
> and the _apoapsis_, i.e. the point where $B$ is the closest and the farthest
> from $A$ respectively.

##### Q2.7.1
The Moon's perigee and apogee are $362600$ $\text{km}$ and $405400$ $\text{km}$
respectively.
Knowing that the mass of the Moon is $7.342 \times 10^{22}$ $\text{kg}$, build a
simple system where the Moon orbits the Earth.

##### Q2.7.2
Below are the positions and masses of all the planets in the solar system.

| name    | aphelion (in AU) | perihelion (in AU) | mass (in $\text{kg}$)   | density (in $\text{g}.\text{cm}^{-3}$) |
| ------- | ---------------- | ------------------ | ----------------------- | -------------------------------------- |
| Sun     | 0.000            | 0.000              | $1.9885 \times 10^{30}$ | 1.408                                  |
| Mercury | 0.467            | 0.307              | $3.3011 \times 10^{23}$ | 5.427                                  |
| Venus   | 0.728            | 0.718              | $4.8675 \times 10^{24}$ | 5.243                                  |
| Earth   | 1.017            | 0.983              | $5.9722 \times 10^{24}$ | 5.513                                  |
| Mars    | 1.666            | 1.381              | $6.4171 \times 10^{23}$ | 3.934                                  |
| Jupyter | 5.457            | 4.951              | $1.8982 \times 10^{27}$ | 1.326                                  |
| Saturn  | 10.12            | 9.041              | $5.6834 \times 10^{26}$ | 0.687                                  |
| Uranus  | 20.10            | 18.29              | $8.6810 \times 10^{25}$ | 1.270                                  |
| Neptune | 30.33            | 29.81              | $1.0241 \times 10^{26}$ | 1.638                                  |

In the table above, only the distance at the _aphelion_ and the _perihelion_ are
given.
There is a formula to compute the speed at any point on the elliptical orbit
$$v^2 = GM(\frac{2}{r} - \frac{1}{a})$$
where $v$ is the speed, $r$ is the distance to the attractive body, $M$ is the
mass of the attractive body and $a$ is the
[_semi-major axis_](https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes)
of the elliptical orbit.

Build a system that simulates the solar system.

##### Q2.7.3
Can you design a 3-body system satisfying the following properties?
- $A$ is at the center
- $B$ orbits around $A$
- $C$ orbits around $B$

##### Q2.7.4
Can you design a _binary star_ system, i.e. a simple system where both bodies
orbit around the other?

### Question 2.8 [[toc](../README.md#table-of-content)] (_optional_)
#### Home sweet home

In this question, we would like to study the time it takes for bodies to return
to their initial position.
This duration is commonly refered to as a _year_.

> :exclamation: **Important**
>
> here, we need to have at least one of the bodies that don't move, otherwise
> none of the bodies will return to it's original position...
>
> to be more precise, we need the center of mass of the system to stay in the
> same vicinity as the original state.

:pencil: Write some Python code to (1) track the distance of all bodies at each time step
from their respective initial positions and (2) plot these distances against time.

:question: What can you observe? Do the bodies go back to where they started? Do some of
them align again in a reasonable amount of time?

:question: Compute the duration of a _year_ for a given body and compare it to the
theoretical value given by Kepler's laws of motion.

> :bulb: **Note**
>
> For the sake of simplicity, in the case of the solar system or any system
> where the orbits are nearly circles, we can approximate the orbits of the
> bodies by circles and then the following equality holds
> $$T^2 = \frac{4\pi^2}{GM}r^3$$

---
---
> this is the end of the class :clap: :clap:
>
> [return to TOC](../README.md#table-of-content)