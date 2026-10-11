# Untitled Game

## Developer's Guide
### Prerequisites
- Visual Studio Code
- Python 3.13
- `uv`

### Install
```sh
uv sync
```

## Overview
```sh
uv run pyreverse -o mmd .\src\untitled_game
```
### Classes
```mermaid
classDiagram
  class Actions {
    name
  }
  class BoxComponent {
    height : int
    width : int
  }
  class Camera {
    position
    zoom : float
  }
  class CameraFollowSystem {
    update(camera: Camera, target: PositionComponent, delta_time: float) None
  }
  class Controller {
    poll_input() list[GameAction]
  }
  class Game {
    box_components : dict[int, BoxComponent]
    entities : list[int]
    game_state
    main_camera
    movement_components : dict[int, MovementComponent]
    player_controller
    position_components : dict[int, PositionComponent]
    time_since_start : float
    create_entity() int
    generate_entity_id() int
    get_input() None
    load() None
    tick(delta_time: float) None
    update_systems(delta_time: float) None
  }
  class GameAction {
    action : int
    value : Any
  }
  class GameState {
    player_inputs : list[GameAction]
    get_player_input_value(action: int) Any
  }
  class KeyboardController {
    poll_input() list[GameAction]
  }
  class MovementComponent {
    movement_style
  }
  class MovementStyle {
    name
  }
  class MovementSystem {
    time_since_start : float
    update(movement_components: dict[int, MovementComponent], positions_components: dict[int, PositionComponent], delta_time: float) None
  }
  class PositionComponent {
    x : float
    y : float
  }
  class RenderSystem {
    update(position_components: dict[int, PositionComponent], box_components: dict[int, BoxComponent]) None
  }
  class Renderer {
    camera
    render_system
    ui_style
    draw_background_grid() None
    draw_game(game: Game) None
    draw_ui(game: Game) None
    render(game: Game) None
    update_camera(camera: Camera) None
  }
  class UIStyle {
    bar_height : int
    bar_width : int
    font_color
    font_size : int
    hpadding : int
    vpadding : int
    vspacing : int
  }
  Game --> BoxComponent : box_components
  Game --> MovementComponent : movement_components
  MovementComponent --> MovementStyle : movement_style
  Camera --> PositionComponent : position
  Game --> PositionComponent : position_components
  Camera --* Game : main_camera
  Controller --* Game : player_controller
  GameState --* Game : game_state
  RenderSystem --* Renderer : render_system
  UIStyle --* Renderer : ui_style
```

### Packages
```mermaid
classDiagram
  class untitled_game {
  }
  class __main__ {
  }
  class components {
  }
  class controllers {
  }
  class core {
  }
  class game {
  }
  class rendering {
  }
  class systems {
  }
  class ui {
  }
  class utils {
  }
  __main__ --> game
  __main__ --> rendering
  controllers --> core
  core --> components
  game --> components
  game --> controllers
  game --> core
  game --> systems
  rendering --> components
  rendering --> controllers
  rendering --> core
  rendering --> game
  rendering --> ui
  systems --> components
  systems --> core
  systems --> utils
```