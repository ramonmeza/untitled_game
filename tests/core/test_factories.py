import pytest

import untitled_game.core.factories as test_module
from untitled_game.core.integrations.raylib import (
    RaylibInputSource,
    RaylibRenderer,
    RaylibWindow,
)


@pytest.mark.parametrize(
    ("impl_cls",),
    ([RaylibInputSource],),
    ids=("raylib",),
)
def test_create_input_source_returns_implementation_type(impl_cls: type) -> None:
    assert isinstance(test_module.create_input_source(), impl_cls)


@pytest.mark.parametrize(
    ("impl_cls",),
    ([RaylibRenderer],),
    ids=("raylib",),
)
def test_create_renderer_returns_implementation_type(impl_cls: type) -> None:
    assert isinstance(test_module.create_renderer(), impl_cls)


@pytest.mark.parametrize(
    ("impl_cls",),
    ([RaylibWindow],),
    ids=("raylib",),
)
def test_create_window_returns_implementation_type(impl_cls: type) -> None:
    assert isinstance(test_module.create_window("Mock Title"), impl_cls)
