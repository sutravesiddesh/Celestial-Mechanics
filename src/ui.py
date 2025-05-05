from typing import Callable, Any, List, Tuple
from dataclasses import dataclass
from collections import namedtuple
from math import pi
from collections import deque

from vec3 import Vector3d as Vec3

import pygame
import sys

State = List[Any]
UIState = namedtuple("UIState", ["pause", "locked", "mouse"])


@dataclass
class Simulation:
    frame_rate: int
    width: int
    height: int
    caption: str
    dt: float
    center: Tuple[float, float] = (0, 0)
    center_offset: Tuple[float, float] = (0, 0)
    zoom: float = 1.0
    trail_length: int = 0
    trail_width: int = 1
    trail_skip: int = 1
    wheel_sensitivity: float = 0.1
    screen: pygame.surface.Surface = None
    clock: pygame.time.Clock = None

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()

    def __to_pizel_coordinates(self, pos: Vec3) -> Tuple[float, float]:
        canvas_center = Vec3(self.width, self.height, 0) / 2
        canvas_center_offset = Vec3(*self.center_offset, 0)
        world_center = Vec3(self.center[0], self.center[1], 0)

        res = canvas_center - canvas_center_offset + \
            (pos - world_center) * self.zoom
        return (res.x, res.y)

    def __handle_events(
        self,
        ui: UIState,
        state: State,
    ) -> UIState:
        pause, locked, mouse = ui.pause, ui.locked, ui.mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and
                event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not ui.pause
                elif event.key == pygame.K_f:
                    locked = None
                elif event.key == pygame.K_k:
                    if ui.locked is None:
                        locked = 0
                    else:
                        locked = (ui.locked + 1) % len(state)
                    self.center_offset = (0, 0)
                elif event.key == pygame.K_j:
                    if ui.locked is None:
                        locked = 0
                    else:
                        locked = (ui.locked - 1) % len(state)
                    self.center_offset = (0, 0)
            elif event.type == pygame.MOUSEWHEEL:
                self.zoom *= (1 + event.y * self.wheel_sensitivity)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = None
            elif event.type == pygame.MOUSEMOTION:
                if mouse is not None:
                    x, y = event.pos
                    self.center_offset = (
                        self.center_offset[0] + ui.mouse[0] - x,
                        self.center_offset[1] + ui.mouse[1] - y,
                    )
                    mouse = event.pos

        return UIState(pause=pause, locked=locked, mouse=mouse)

    def __render(
        self,
        trails: List[List[Vec3]],
        state: State,
        locked: int,
    ):
        self.screen.fill((0, 0, 0))

        for i, (t, s) in enumerate(zip(trails, state)):
            # let's cook some spaghetti lol
            if self.trail_skip > 1:
                t = list(t)[::self.trail_skip]
            if len(t) >= 2 and i != locked:
                if locked is None:
                    _t = t
                else:
                    if self.trail_skip > 1:
                        focused_trail = list(trails[locked])[::self.trail_skip]
                    else:
                        focused_trail = trails[locked]
                    _t = [
                        p - (c - state[locked].pos)
                        for p, c in zip(t, focused_trail)
                    ]
                pygame.draw.lines(
                    self.screen,
                    s.color,
                    False,
                    list(map(self.__to_pizel_coordinates, _t)),
                    width=self.trail_width
                )
            pygame.draw.circle(
                self.screen,
                s.color,
                self.__to_pizel_coordinates(s.pos),
                (3 * s.mass / (4 * pi * s.density)) ** 0.333 * self.zoom,
            )
        pygame.display.flip()

    def loop(
        self,
        initial_state: State,  # the items in the state should all have fields
                               # `pos`, `color` and `mass`
        update: Callable[[State, float], State],
    ):
        state = initial_state
        trails: List[deque] = [deque() for _ in state]

        ui = UIState(pause=False, locked=None, mouse=None)

        self.center_offset = (
            self.center[0] * self.zoom,
            self.center[1] * self.zoom,
        )

        time_step = 0

        while True:
            ui = self.__handle_events(ui, state)

            if ui.locked is not None:
                center = state[ui.locked].pos
                self.center = (center.x, center.y)

            self.__render(trails, state, ui.locked)
            self.clock.tick(self.frame_rate)

            if not ui.pause:
                state = update(state, self.dt)

                if self.trail_length > 0:
                    for ti, s in zip(trails, state):
                        ti.append(s.pos)
                    if time_step > self.trail_length:
                        for t in trails:
                            t.popleft()

            time_step += 1
