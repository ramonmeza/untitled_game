from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest

from untitled_game.core.engine import Engine

type EngineDependencyFixture = Generator[dict[str, Engine | Mock]]


@pytest.fixture
def engine_dependencies() -> EngineDependencyFixture:
    with (
        patch("untitled_game.core.engine.TickContext") as tick_context_cls,
        patch("untitled_game.core.engine.InputState") as input_state_cls,
        patch("untitled_game.core.engine.InputHandler") as input_handler_cls,
        patch("untitled_game.core.engine.create_input_source") as input_source_factory,
        patch("untitled_game.core.engine.create_renderer") as renderer_factory,
        patch("untitled_game.core.engine.create_dev_world") as world_factory,
        patch("untitled_game.core.engine.WorldRunner") as world_runner_cls,
        patch("untitled_game.core.engine.perf_counter", return_value=10.0),
    ):
        input_state = Mock(name="input_state")
        input_state_cls.return_value = input_state

        tick_context = Mock(name="tick_context")
        tick_context_cls.return_value = tick_context

        input_handler = input_handler_cls.return_value
        renderer = renderer_factory.return_value
        world = world_factory.return_value
        world_runner = world_runner_cls.return_value

        engine = Engine()

        yield {
            "engine": engine,
            "tick_context": tick_context,
            "input_state": input_state,
            "input_handler": input_handler,
            "renderer": renderer,
            "world": world,
            "world_runner": world_runner,
            "input_source_factory": input_source_factory,
            "input_handler_cls": input_handler_cls,
            "renderer_factory": renderer_factory,
            "world_factory": world_factory,
            "world_runner_cls": world_runner_cls,
        }


def test_initialize_initializes_renderer(engine_dependencies: EngineDependencyFixture):
    deps = engine_dependencies

    deps["engine"].initialize()

    deps["renderer"].initialize.assert_called_once_with()


def test_update_tick_context_updates_elapsed_time_and_input(
    engine_dependencies: Generator[dict[str, Mock]],
):
    deps = engine_dependencies
    engine = deps["engine"]
    input_state = deps["input_state"]

    engine.prev_tick_time = 10.0
    deps["input_handler"].get_input_state.return_value = input_state

    with patch(
        "untitled_game.core.engine.perf_counter",
        return_value=10.025,
    ):
        engine.update_tick_context()

    assert engine.prev_tick_time == pytest.approx(10.025)
    assert engine._tick_context.delta_time == pytest.approx(0.025)
    assert engine._tick_context.input_state is input_state
    deps["input_handler"].get_input_state.assert_called_once_with()


def test_tick_update_does_not_tick_before_interval(
    engine_dependencies: EngineDependencyFixture,
):
    deps = engine_dependencies
    engine = deps["engine"]
    engine._tick_accumulator = engine.tick_interval * 0.5

    engine.tick_update()

    deps["world_runner"].tick.assert_not_called()
    assert engine.num_ticks == 0


def test_tick_update_runs_one_tick_when_interval_is_reached(
    engine_dependencies: EngineDependencyFixture,
):
    deps = engine_dependencies
    engine = deps["engine"]
    engine._tick_accumulator = engine.tick_interval

    engine.tick_update()

    deps["world_runner"].tick.assert_called_once_with(deps["tick_context"])
    assert engine.num_ticks == 1
    assert engine._tick_accumulator == pytest.approx(0.0)


def test_tick_update_runs_multiple_ticks_for_accumulated_time(
    engine_dependencies: EngineDependencyFixture,
):
    deps = engine_dependencies
    engine = deps["engine"]
    engine._tick_accumulator = engine.tick_interval * 3.5

    engine.tick_update()

    assert deps["world_runner"].tick.call_count == 3
    assert engine.num_ticks == 3
    assert engine._tick_accumulator == pytest.approx(engine.tick_interval * 0.5)


def test_render_renders_world_with_current_context_and_renderer(
    engine_dependencies: EngineDependencyFixture,
):
    deps = engine_dependencies

    deps["engine"].render()

    deps["world_runner"].render.assert_called_once_with(
        deps["tick_context"],
        deps["renderer"],
    )


def test_update_refreshes_context_ticks_and_renders(
    engine_dependencies: EngineDependencyFixture,
):
    deps = engine_dependencies
    engine = deps["engine"]

    # One full simulation tick should be due after updating the context.
    engine.prev_tick_time = 10.0
    engine._tick_accumulator = 0.0
    deps["input_handler"].get_input_state.return_value = deps["input_state"]

    with patch(
        "untitled_game.core.engine.perf_counter",
        return_value=10.0 + engine.tick_interval,
    ):
        engine.update()

    deps["input_handler"].get_input_state.assert_called_once_with()
    deps["world_runner"].tick.assert_called_once_with(deps["tick_context"])
    deps["world_runner"].render.assert_called_once_with(
        deps["tick_context"],
        deps["renderer"],
    )
    assert engine.num_ticks == 1


def test_teardown_tears_down_renderer(engine_dependencies: EngineDependencyFixture):
    deps = engine_dependencies

    deps["engine"].teardown()

    deps["renderer"].teardown.assert_called_once_with()
