# TDW Robotics

## Robotics API

TDW's robots are handled very similarly to how 3D models are handled. They are stored in a robot library and have [corresponding metadata records](../python/librarian/robot_librarian.md). 

Add robots to the scene using either [the `add_robot` command or `Controller.get_add_robot()`](../python/librarian/robot_librarian.md#command-api).

| Command                   | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `add_robot`               | Add a robot to the scene.                                    |
| `destroy_robot`           | Destroys a robot in the scene.                               |
| `set_immovable`           | Set whether or not the root object of the robot is immovable. Its joints will still be moveable. |
| `set_prismatic_target`    | Set the target position of a prismatic robot joint. Per frame, the joint will move towards the target until it is either no longer possible to do so (i.e. due to physics) or because it has reached the target position. |
| `set_revolute_target`     | Set the target angle of a revolute robot joint. Per frame, the joint will revolve towards the target until it is either no longer possible to do so (i.e. due to physics) or because it has reached the target angle. |
| `set_spherical_target`    | Set the target angles (x, y, z) of a spherical robot joint. Per frame, the joint will revolve towards the targets until it is either no longer possible to do so (i.e. due to physics) or because it has reached the target angles. |
| `add_force_to_prismatic`  | Add a force to a prismatic joint.                            |
| `add_torque_to_revolute`  | Add a torque to a revolute joint.                            |
| `add_torque_to_spherical` | Add a torque to a spherical joint.                           |
| `send_robots`             | [Send data for each robot in the scene](https://github.com/threedworld-mit/tdw/blob/master/Documentation/api/output_data.md#Robot) (including Magnebots). |
| `send_static_robots`      | [Send static data for each robot in the scene](https://github.com/threedworld-mit/tdw/blob/master/Documentation/api/output_data.md#StaticRobot) (including Magnebots). |
| `parent_avatar_to_robot`  | Parent an avatar to a robot.                                 |
| `set_robot_joint_drive`   | Set static joint drive parameters.                           |
| `set_robot_joint_mass`    | Set the mass of a robot joint.                               |
| `teleport_robot`          | Teleport the robot to a new position and rotation. This is a sudden movement that might disrupt the physics simulation. You should only use this command if you really need to (for example, if the robot falls over). |

### Joint targets

| Joint Type | Degrees of freedom | Units   |
| ---------- | ------------------ | ------- |
| fixed      | 0                  |         |
| revolute   | 1                  | degrees |
| prismatic  | 1                  | meters  |
| spherical  | 3                  | degrees |

Once the target is set, the joint still needs to move to the target. You can determine if joints are still moving by checking the [`Robot.get_joint_positions()`](https://github.com/threedworld-mit/tdw/blob/master/Documentation/api/output_data.md#Robot). See `robot_arm.py` for example implementation.

Targets are always *cumulative*, not deltas. If you do this:

1. Set revolute target to `720`
2. Wait
3. Set revolute target to `0`
4. Wait

You will get the following behavior:

1. Joint turns 720 degrees
2. Joint turns -720 degrees

## Robots and Avatars

TDW has a built-in concept of what an "Avatar" is, which has implications for which commands can be sent to which objects in the scene. Robots are *not* avatars; they are *robots*.

Robots by default don't have cameras. However, you can add a camera to a robot by first creating an avatar and then parenting that avatar to the robot. See: `example_controllers/robot_camera.py` for example implementation.

## Robots Currently in TDW

TDW includes many real-world robots by default. Metadata records of each robot are stored in a [`RobotLibrarian`](../python/librarian/robot_librarian.md).

 To get a list of available robots:

```python
from tdw.librarian import RobotLibrarian

lib = RobotLibrarian()
for record in lib.records:
    print(record.name)
```

To search for a robot:

```python
from tdw.librarian import RobotLibrarian

lib = RobotLibrarian()

record = lib.get_record("ur3")
if record is not None:
    print(record.name, record.urls)
    
records = lib.search_records("ur3")
for record in records:
    print(record)
```

To add a robot:

```python
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.librarian import RobotLibrarian

c = Controller(launch_build=False)
c.start()

lib = RobotLibrarian()
record = lib.get_record(name="ur3")

c.communicate([TDWUtils.create_empty_room(12, 12),
               c.get_add_robot(name=record.name,
                               robot_id=0,
                               position={"x": 0.5, "y": 0, "z": 2})])
```

## How to Add a Robot to TDW

**It is possible to import any robot into TDW, given a .urdf or .xacro file.** To do so, use a `RobotCreator`. [Read this document to learn more about the API and installation requirements](../python/robot_creator.md).

## Magnebot API

The Magnebot is a specialized robot in TDW that can use "magnets" to pick up objects.

[**Get the high-level Magnebot API here.**](https://github.com/alters-mit/magnebot)

![](../images/robots/reach_high.gif)

Add a Magnebot to the scene with the `add_magnebot` command (`add_robot` will *not* add a Magnebot!). With the exception of `add_robot`, all other commands in the Robotics API are compatible with the Magnebot. 

<img src="../images/robots/magnebot_front.jpg" style="zoom: 67%;" />

<img src="../images/robots/magnebot_back.jpg" style="zoom:67%;" />

| Joint               | Command                |
| ------------------- | ---------------------- |
| `column`            | `set_revolute_target`  |
| `torso`             | `set_prismatic_target` |
| `shoulder_left`     | `set_spherical_target` |
| `shoulder_right`    | `set_spherical_target` |
| `elbow_left`        | `set_revolute_target`  |
| `elbow_right`       | `set_revolute_target`  |
| `wrist_left`        | `set_spherical_target` |
| `wrist_right`       | `set_spherical_target` |
| `magnet_left`       |                        |
| `magnet_right`      |                        |
| `wheel_left_front`  | `set_revolute_target`  |
| `wheel_right_front` | `set_revolute_target`  |
| `wheel_left_back`   | `set_revolute_target`  |
| `wheel_right_back`  | `set_revolute_target`  |

To get the corresponding name and object ID of each joint, see `send_static_robots`.

There are also additional commands that are specific to the Magnebot:

| Command              | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `set_magnet_targets` | Set the objects that the Magnebot magnet will try to pick up. If the magnet collides with any of these objects, the Magnebot will pick up them up. |
| `detach_from_magnet` | Detach an object from a Magnebot magnet.                     |
| `send_magnebots`     | [Send data for each Magnebot in the scene.](https://github.com/threedworld-mit/tdw/blob/master/Documentation/api/output_data.md#Magnebot) This includes the IDs of any held objects. |

### Picking up objects with magnets

The Magnebot's magnets "picks up" objects by first colliding with a target object (see `set_magnet_targets`), then caching Rigidbody data (mass, angular drag, etc.), adding the object's mass to the magnet's mass, then destroying the Rigidbody component, then parenting the object to the magnet. The Magnebot "puts down" the object by recreating the Rigidbody, subtracting the mass, and unparenting the object. This is to ensure maximum physics stability.

The upshot is that Rigidbody commands such as `set_mass` will throw an error if the object is being held by a Magnebot magnet. Data returned by `send_rigidbodies` will be 0s if the object is being held (for example, the mass will be 0).

## Example controllers

[**See the high-level Magnebot API for additional examples.**](https://github.com/alters-mit/magnebot)

| Controller        | Description                                  |
| ----------------- | -------------------------------------------- |
| `magnebot.py`     | Add a Magnebot and move it around the scene. |
| `robot_arm.py`    | Move the joints of a robot arm.              |
| `robot_camera.py` | Add a camera to a Magnebot.                  |

