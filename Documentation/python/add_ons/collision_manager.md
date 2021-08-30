# CollisionManager

`from tdw.add_ons.collision_manager import CollisionManager`

Manager add-on for all collisions on this frame.

***

## Fields

- `commands` These commands will be appended to the commands of the next `communicate()` call.

- `initialized` If True, this module has been initialized.

- `obj_collisions` All collisions between two objects that occurred on the frame.
Key = An `IntPair` (a pair of object IDs). Value = [The collision.](../collision_data/collision_obj_obj.md)

- `env_collisions` All collisions between an object and the environment that occurred on the frame.
Key = the object ID. Value = [The collision.](../collision_data/collision_obj_env.md)

***

## Functions

#### \_\_init\_\_

**`CollisionManager()`**

**`CollisionManager(enter=True, stay=False, exit=False, objects=True, environment=True)`**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| enter |  bool  | True | If True, listen for collision enter events. |
| stay |  bool  | False | If True, listen for collision stay events. |
| exit |  bool  | False | If True, listen for collision exit events. |
| objects |  bool  | True | If True, listen for collisions between objects. |
| environment |  bool  | True | If True, listen for collisions between an object and the environment. |

#### get_initialization_commands

**`self.get_initialization_commands()`**

This function gets called exactly once per add-on. To call it again, set `self.initialized = False`.

_Returns:_  A list of commands that will initialize this module.

#### on_send

**`self.on_send(resp)`**

This is called after commands are sent to the build and a response is received.

Use this function to send commands to the build on the next frame, given the `resp` response.
Any commands in the `self.commands` list will be sent on the next frame.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| resp |  List[bytes] |  | The response from the build. |

##### before_send

**`self.before_send(commands)`**

This is called before sending commands to the build. By default, this function doesn't do anything.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| commands |  List[dict] |  | The commands that are about to be sent to the build. |



