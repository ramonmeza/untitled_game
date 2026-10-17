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
    mock_input_source = MagicMock()
    with (
        patch("untitled_game.core.engine.create_input_source", return_value=mock_input_source),
        patch("untitled_game.core.engine.create_renderer", return_value=mock_renderer),
    ):
        engine = Engine()
        engine.teardown()

        mock_renderer.teardown.assert_called_once()
