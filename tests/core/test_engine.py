from unittest.mock import MagicMock, patch

from untitled_game.core.engine import Engine


def test_engine_initialize() -> None:
    mock_renderer = MagicMock()
    mock_input_source = MagicMock()
    with (
        patch("untitled_game.core.engine.create_input_source", return_value=mock_input_source),
        patch("untitled_game.core.engine.create_renderer", return_value=mock_renderer),
    ):
        engine = Engine()
        engine.initialize()

        mock_renderer.initialize.assert_called_once()


def test_engine_teardown() -> None:
    mock_renderer = MagicMock()
    with (
        patch("untitled_game.core.engine.create_renderer", return_value=mock_renderer),
    ):
        engine = Engine()
        engine.teardown()

        mock_renderer.teardown.assert_called_once()


def test_update_with_frame_time_below_tick_interval() -> None:
    mock_input_source = MagicMock()
    mock_renderer = MagicMock()
    with (
        patch("untitled_game.core.engine.create_input_source", return_value=mock_input_source),
        patch("untitled_game.core.engine.create_renderer", return_value=mock_renderer),
    ):
        with patch("untitled_game.core.engine.perf_counter", return_value=0):
            engine = Engine()

        tick_interval: float = engine.tick_interval
        delta_time_smaller_than_tick_interval: float = tick_interval * 0.5
        assert engine.num_ticks == 0
        with patch(
            "untitled_game.core.engine.perf_counter",
            return_value=delta_time_smaller_than_tick_interval,
        ):
            engine.update()
        assert engine.num_ticks == 0


def test_update_with_frame_time_above_tick_interval() -> None:
    mock_input_source = MagicMock()
    mock_renderer = MagicMock()
    with (
        patch("untitled_game.core.engine.create_input_source", return_value=mock_input_source),
        patch("untitled_game.core.engine.create_renderer", return_value=mock_renderer),
    ):
        with patch("untitled_game.core.engine.perf_counter", return_value=0):
            engine = Engine()

        tick_interval: float = engine.tick_interval
        delta_time_larger_than_tick_interval: float = tick_interval * 2.0
        expected_num_ticks: int = int(delta_time_larger_than_tick_interval / tick_interval)
        assert engine.num_ticks == 0
        with patch(
            "untitled_game.core.engine.perf_counter",
            return_value=delta_time_larger_than_tick_interval,
        ):
            engine.update()
        assert engine.num_ticks == expected_num_ticks
