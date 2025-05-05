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
