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
  class ActionEmitter {
    poll_actions() list[ActionValue]
  }
  class ActionEmitterComponent {
    action_emitter
    actions : list[ActionValue]
  }
  class ActionID {
    name
  }
  class ActionSystem {
    update(emitter_comps: list[ActionEmitterComponent]) None
  }
  class ActionValue {
    id
    value : Any
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
  class ECS {
    components : dict[ComponentsTypes, list[EntityComponentPair]]
    entities : list[int]
    add_component(entity_id: int, component_cls: ComponentsTypes) None
    create_entity() int
    generate_entity_id() int
    get_all_components_of_type(component_cls: type[T]) list[T]
    get_all_entities_with_components() list[int]
    get_components(entity_id: int) list[Components]
    get_components_of_type(entity_id: int, component_cls: type[T]) list[T]
  }
  class EntityComponentPair {
    component
    entity_id : int
  }
  class Game {
    ecs
    main_camera
    get_action_value(entity_id: int, action: int, default: Any) Any
    get_player_entity_id() int
    load() None
    tick(delta_time: float) None
    update_systems(delta_time: float) None
  }
  class KeyboardActionEmitter {
    poll_actions() list[ActionValue]
  }
  class MovementComponent {
  }
  class MovementSystem {
    time_since_start : float
    apply_movement(position_comp: PositionComponent, emitter_comp: ActionEmitterComponent)* None
    update(ecs: ECS, movables: list[int], delta_time: float) None
  }
  class PositionComponent {
    x : float
    y : float
  }
  class RenderSystem {
    update(ecs: ECS) None
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
  ActionEmitterComponent --> ActionEmitter : action_emitter
  ActionValue --> ActionID : id
  Camera --> PositionComponent : position
  Camera --* Game : main_camera
  ECS --* Game : ecs
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
  class actions {
  }
  class camera {
  }
  class components {
  }
  class ecs {
  }
  class emitters {
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
  camera --> components
  components --> actions
  ecs --> components
  emitters --> actions
  game --> camera
  game --> components
  game --> ecs
  game --> emitters
  game --> systems
  rendering --> actions
  rendering --> camera
  rendering --> components
  rendering --> ecs
  rendering --> game
  rendering --> ui
  systems --> camera
  systems --> components
  systems --> ecs
  systems --> utils
```