# SceneBounds

`from scene.scene_bounds import SceneBounds`

Data for the scene bounds and its rooms.

In order to initialize this object, the controller must have sent `send_environments` to the build on the previous frame:

```python
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.scene.scene_bounds import SceneBounds

c = Controller()
c.start()
resp = c.communicate([TDWUtils.create_empty_room(12, 12),
                      {"$type": "send_environments"}])
scene_bounds = SceneBounds(resp=resp)
```

***

## Fields

- `x_min` Minimum x positional coordinate of the scene.

- `x_max` Maximum x positional coordinate of the scene.

- `y_min` Minimum y positional coordinate of the scene.

- `y_max` Maximum y positional coordinate of the scene.

- `z_min` Minimum z positional coordinate of the scene.

- `z_max` Maximum z positional coordinate of the scene.

- `rooms` All of the rooms in the scene.

***

## Functions

#### \_\_init\_\_

**`SceneBounds(resp)`**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| resp |  List[bytes] |  | The response from the build. |

