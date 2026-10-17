from collections.abc import Generator

import pytest

from untitled_game.core.input.states import InputState
from untitled_game.core.renderer import Renderer
from untitled_game.core.tick_context import TickContext
from untitled_game.core.world.runner import World, WorldRunner


@pytest.fixture
def world_runner() -> Generator[WorldRunner]:
    world: World = World()
    world_runner: WorldRunner = WorldRunner(world)
    yield world_runner


def test_world_runner_mock_gameplay_system(world_runner: WorldRunner) -> None:
    class MockGameplaySystem:
        def __init__(self, expected_tick_context: TickContext) -> None:
            self.tick_context = expected_tick_context

        def update(self, tick_context: TickContext) -> None:
            assert tick_context == self.tick_context

    mock_tick_context: TickContext = TickContext(0, InputState())
    mock_gameplay_system = MockGameplaySystem(mock_tick_context)
    world_runner._gameplay_systems.clear()
    world_runner._gameplay_systems.append(mock_gameplay_system)
    world_runner.tick(mock_tick_context)


def test_world_runner_mock_rendering_system(world_runner: WorldRunner) -> None:
    class MockRenderer:
        def initialize(self) -> None:
            pass

        def teardown(self) -> None:
            pass

        def begin_frame(self) -> None:
            pass

        def end_frame(self) -> None:
            pass

        def draw_sprite(self, texture_path: str, x: int, y: int) -> None:
            pass

    class MockRenderingSystem:
        def __init__(self, expected_tick_context: TickContext) -> None:
            self.tick_context = expected_tick_context

        def render(self, world: World, tick_context: TickContext, renderer: Renderer) -> None:
            assert tick_context == self.tick_context

    mock_renderer = MockRenderer()
    mock_tick_context: TickContext = TickContext(0, InputState())
    mock_rendering_system = MockRenderingSystem(mock_tick_context)
    world_runner._rendering_systems.clear()
    world_runner._rendering_systems.append(mock_rendering_system)
    world_runner.render(mock_tick_context, mock_renderer)
    assert mock_rendering_system in world_runner.rendering_systems
