from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from untitled_game.core.application import Application


class MockWindow(MagicMock):
    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)
        self.opened: bool = False

    def is_open(self) -> bool:
        return self.opened


type TestApplication = tuple[MagicMock, MockWindow, Application]


@pytest.fixture
def test_application() -> Generator[TestApplication]:
    mock_engine = MagicMock()
    mock_window = MockWindow()
    with patch("untitled_game.core.application.Engine", return_value=mock_engine):
        application = Application(mock_window)
        yield mock_engine, mock_window, application


def test_application_initialize(test_application: TestApplication) -> None:
    mock_engine = test_application[0]
    mock_window = test_application[1]
    app = test_application[2]

    app.initialize()

    mock_window.open.assert_called_once()
    mock_engine.initialize.assert_called_once()


def test_application_teardown(test_application: TestApplication) -> None:
    mock_engine = test_application[0]
    mock_window = test_application[1]
    app = test_application[2]

    app.teardown()

    mock_engine.teardown.assert_called_once()
    mock_window.close.assert_called_once()


def test_loop_when_window_is_closed(test_application: TestApplication) -> None:
    mock_engine = test_application[0]
    mock_window = test_application[1]
    app = test_application[2]

    mock_window.opened = False

    app.loop()

    mock_engine.update.assert_not_called()


def test_loop_when_window_is_open(test_application: TestApplication) -> None:
    mock_engine = test_application[0]
    mock_window = test_application[1]
    app = test_application[2]

    def engine_update_side_effect() -> None:
        nonlocal mock_window
        mock_window.opened = False

    mock_engine.update = MagicMock(side_effect=engine_update_side_effect)
    mock_window.opened = True

    app.loop()

    mock_engine.update.assert_called_once()


def test_run_when_window_closed(test_application: TestApplication) -> None:
    mock_engine = test_application[0]
    mock_window = test_application[1]
    app = test_application[2]

    mock_window.opened = False

    app.run()

    mock_window.open.assert_called_once()
    mock_engine.initialize.assert_called_once()
    mock_window.close.assert_called_once()
    mock_engine.teardown.assert_called_once()
