from collections.abc import Generator
from unittest.mock import MagicMock

import pytest

from untitled_game.core.input.states import InputState
from untitled_game.core.tick_context import TickContext
from untitled_game.core.world.runner import World, WorldRunner


@pytest.fixture
def world_runner() -> Generator[WorldRunner]:
    world: World = World()
    world_runner: WorldRunner = WorldRunner(world)
    yield world_runner


def test_world_runner_mock_gameplay_system(world_runner: WorldRunner) -> None:
    mock_tick_context: TickContext = TickContext(0, InputState())
    mock_gameplay_system = MagicMock()
    world_runner._gameplay_systems.clear()
    world_runner._gameplay_systems.append(mock_gameplay_system)
    world_runner.tick(mock_tick_context)

    assert mock_gameplay_system in world_runner._gameplay_systems
    mock_gameplay_system.update.assert_called_once_with(mock_tick_context)


def test_world_runner_mock_rendering_system(world_runner: WorldRunner) -> None:
    mock_renderer = MagicMock()
    mock_tick_context: TickContext = TickContext(0, InputState())
    mock_rendering_system = MagicMock()
    world_runner._rendering_systems.clear()
    world_runner._rendering_systems.append(mock_rendering_system)
    world_runner.render(mock_tick_context, mock_renderer)

    assert mock_rendering_system in world_runner.rendering_systems
    mock_renderer.begin_frame.assert_called_once()
    mock_rendering_system.render.assert_called_once_with(
        world_runner._world, mock_tick_context, mock_renderer
    )
    mock_renderer.end_frame.assert_called_once()
