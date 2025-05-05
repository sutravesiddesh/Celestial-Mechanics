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
