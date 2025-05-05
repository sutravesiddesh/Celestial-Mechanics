Below is a snippet of code that should allow you to run a simulation using the
`src.ui` module
```python
from src.ui import Simulation

bodies = [ ... ]

def update(...):
    ...

simulation = Simulation(
    frame_rate=30,
    width=800,
    height=800,
    caption="My Simulation",
    dt=1000,
    trail_length=500,
)
simulation.setup()
simulation.center = (0, 0)
simulation.zoom = 1e-6
simulation.loop(initial_state=bodies, update=update)
```

## key bindings
There are a few key bindings that can be used to interact with the simulation
while it's running:
- pressing the "close" button of the window with the mouse or the _ESC_ key will
  close the simulation
- pressing _SPACE_ will pause / unpause the simulation
- pressing _K_ and _J_ will cycle through the bodies in the simulation, locking
  the view to one of them
- pressing _F_ will remove the focus
- using the mousewheel allows to change the zoom level
- dragging the mouse by clicking any button of the mouse will allow to move the
  _camera_ around
