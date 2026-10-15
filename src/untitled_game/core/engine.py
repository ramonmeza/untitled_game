from time import perf_counter

from ..core.tick_context import TickContext
from ..game.prefabs import create_empty_world
from .factories import create_input_source, create_renderer
from .input import InputHandler, InputState
from .renderer import Renderer
from .world.runner import WorldRunner
from .world.world import World


class Engine:
    def __init__(self) -> None:
        self._tick_context: TickContext = TickContext(0, InputState())
        self._input_handler: InputHandler = InputHandler(create_input_source())
        self._renderer: Renderer = create_renderer()

        world: World = create_empty_world()
        self._world_runner: WorldRunner = WorldRunner(world)

        self.prev_tick_time: float = perf_counter()
        self._tick_accumulator: float = 0.0
        self.tick_interval: float = 1.0 / 60.0
        self.num_ticks: int = 0

    def initialize(self) -> None:
        self._renderer.initialize()

    def update_tick_context(self) -> None:
        tick_time: float = perf_counter()
        delta_time: float = tick_time - self.prev_tick_time
        self._tick_accumulator += delta_time
        self.prev_tick_time = tick_time
        self._tick_context.delta_time = delta_time
        self._tick_context.input_state = self._input_handler.get_input_state()

    def update(self) -> None:
        self.update_tick_context()
        self.tick_update()
        self.render()

    def tick_update(self) -> None:
        while self._tick_accumulator >= self.tick_interval:
            self._tick_accumulator -= self.tick_interval
            self._world_runner.tick(self._tick_context)
            self.num_ticks += 1

    def render(self) -> None:
        self._world_runner.render(self._tick_context, self._renderer)

    def teardown(self) -> None:
        self._renderer.teardown()
