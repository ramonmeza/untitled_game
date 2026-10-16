from unittest.mock import Mock, patch

import pytest

from untitled_game.core.application import Application, ApplicationConfig


@pytest.fixture
def window():
    return Mock()


@patch("untitled_game.core.application.Engine")
def test_initialize_opens_window_and_initializes_engine(mock_engine_cls, window):
    engine = mock_engine_cls.return_value
    app = Application(window)

    app.initialize()

    window.open.assert_called_once_with(800, 800)
    engine.initialize.assert_called_once_with()


@patch("untitled_game.core.application.Engine")
def test_loop_updates_engine_until_window_closes(mock_engine_cls, window):
    engine = mock_engine_cls.return_value
    window.is_open.side_effect = [True, True, True, False]
    app = Application(window)

    app.loop()

    assert window.is_open.call_count == 4
    assert engine.update.call_count == 3


@patch("untitled_game.core.application.Engine")
def test_loop_does_not_update_engine_if_window_is_closed(mock_engine_cls, window):
    engine = mock_engine_cls.return_value
    window.is_open.return_value = False
    app = Application(window)

    app.loop()

    engine.update.assert_not_called()


@patch("untitled_game.core.application.Engine")
def test_teardown_tears_down_engine_and_closes_window(mock_engine_cls, window):
    engine = mock_engine_cls.return_value
    app = Application(window)

    app.teardown()

    engine.teardown.assert_called_once_with()
    window.close.assert_called_once_with()


@patch("untitled_game.core.application.Engine")
def test_run_executes_application_lifecycle_in_order(mock_engine_cls, window):
    engine = mock_engine_cls.return_value
    window.is_open.side_effect = [True, True, False]
    app = Application(window)

    events = []

    window.open.side_effect = lambda *args: events.append("window.open")
    engine.initialize.side_effect = lambda: events.append("engine.initialize")
    engine.update.side_effect = lambda: events.append("engine.update")
    engine.teardown.side_effect = lambda: events.append("engine.teardown")
    window.close.side_effect = lambda: events.append("window.close")

    app.run()

    assert events == [
        "window.open",
        "engine.initialize",
        "engine.update",
        "engine.update",
        "engine.teardown",
        "window.close",
    ]


def test_application_config_defaults():
    config = ApplicationConfig()

    assert config.window_width == 800
    assert config.window_height == 800


def test_application_config_accepts_custom_dimensions():
    config = ApplicationConfig(window_width=1024, window_height=768)

    assert config.window_width == 1024
    assert config.window_height == 768
