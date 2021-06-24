from typing import List, Dict, Union, Optional
from tdw.add_ons.third_person_camera_base import ThirdPersonCameraBase


class ThirdPersonCamera(ThirdPersonCameraBase):
    """
    Add a third-person camera to the scene. This includes initialization parameters (position, rotation, etc.) and some basic movement parameters (whether to follow or look at a target),.

    ```python
    from tdw.controller import Controller
    from tdw.tdw_utils import TDWUtils
    from tdw.add_ons.third_person_camera import ThirdPersonCamera

    c = Controller(launch_build=False)
    c.start()
    cam = ThirdPersonCamera(avatar_id="c",
                            position={"x": 1, "y": 2.2, "z": -0.5},
                            rotation={"x": 0, "y": -45, "z": 0})
    c.add_ons.append(cam)
    c.communicate(TDWUtils.create_empty_room(12, 12))
    ```

    By itself, a `ThirdPersonCamera` won't capture images (though it will render them on the screen). For image capture, include an `ImageCapture` add-on:

    ```python
    from tdw.controller import Controller
    from tdw.tdw_utils import TDWUtils
    from tdw.add_ons.third_person_camera import ThirdPersonCamera
    from tdw.add_ons.image_capture import ImageCapture

    c = Controller(launch_build=False)
    c.start()
    cam = ThirdPersonCamera(avatar_id="c",
                            position={"x": 1, "y": 2.2, "z": -0.5},
                            rotation={"x": 0, "y": -45, "z": 0})
    cap = ImageCapture(path="images", avatar_ids=["c"])
    c.add_ons.append(cam)
    c.add_ons.append(cap)
    c.communicate(TDWUtils.create_empty_room(12, 12))
    ```

    ## Third-person cameras and avatars

    The `ThirdPersonCamera` is a wrapper class for a standard `A_Img_Caps_Kinematic` TDW avatar. All non-physics avatar commands may be sent for this camera.

    In this document, the words "camera" and "avatar" may be used interchangeably.

    ## Multiple cameras

    Unlike most `AddOn` objects, it is possible to add multiple `ThirdPersonCamera`s to the scene:

    ```python
    from tdw.controller import Controller
    from tdw.tdw_utils import TDWUtils
    from tdw.add_ons.third_person_camera import ThirdPersonCamera
    from tdw.add_ons.image_capture import ImageCapture

    c = Controller(launch_build=False)
    c.start()

    # Add two cameras.
    cam_0 = ThirdPersonCamera(avatar_id="c0",
                              position={"x": 1, "y": 2.2, "z": -0.5},
                              rotation={"x": 0, "y": -45, "z": 0})
    cam_1 = ThirdPersonCamera(avatar_id="c1",
                              position={"x": 2, "y": 1, "z": -5})

    # Enable image capture for both cameras.
    cap = ImageCapture(path="images", avatar_ids=["c0", "c1"])

    c.add_ons.extend([cam_0, cam_1, cap])
    c.communicate(TDWUtils.create_empty_room(12, 12))
    ```
    """

    def __init__(self, avatar_id: str = None, position: Dict[str, float] = None, rotation: Dict[str, float] = None,
                 fov: int = None, pass_masks: List[str] = None, framerate: int = None,
                 look_at: Union[int, Dict[str, float]] = None, follow_object: int = None, follow_rotate: bool = False):
        """
        :param avatar_id: The ID of the avatar (camera). If None, a random ID is generated.
        :param position: The initial position of the object.If None, defaults to `{"x": 0, "y": 0, "z": 0}`.
        :param rotation: The initial rotation of the camera. Can be Euler angles (keys are `(x, y, z)`) or a quaternion (keys are `(x, y, z, w)`). If None, defaults to `{"x": 0, "y": 0, "z": 0}`.
        :param look_at: If not None, rotate look at this target every frame. Overrides `rotation`. Can be an int (an object ID) or an `(x, y, z)` dictionary (a position).
        :param fov: If not None, this is the initial field of view. Otherwise, defaults to 35.
        :param follow_object: If not None, follow an object per frame. The `position` parameter will be treated as a relative value from the target object rather than worldspace coordinates.
        :param follow_rotate: If True, match the rotation of the object. Ignored if `follow_object` is None.
        :param pass_masks: The pass masks. If None, defaults to `["_img"]`.
        :param framerate: If not None, sets the target framerate.
        """

        super().__init__(avatar_id=avatar_id, position=position, rotation=rotation, fov=fov, pass_masks=pass_masks,
                         framerate=framerate)

        """:field
        The target object or position that the camera will look at. Can be None (the camera won't look at a target).
        """
        self.look_at_target: Optional[Union[int, Dict[str, float]]] = look_at
        self._init_commands.extend(self._get_look_at_commands())
        """:field
        The ID of the object the camera will try to follow. Can be None (the camera won't follow an object).
        """
        self.follow_object: Optional[int] = follow_object
        """:field
        If `follow_object` is not None, this determines whether the camera will follow the object's rotation.
        """
        self.follow_rotate: bool = follow_rotate

    def on_communicate(self, resp: List[bytes], commands: List[dict]) -> None:
        # Look at and focus on a target object or position.
        if self.look_at_target is not None:
            self.commands.extend(self._get_look_at_commands())
        # Follow a target object.
        if self.follow_object is not None and self.position is not None:
            self.commands.append({"$type": "follow_object",
                                  "object_id": self.follow_object,
                                  "position": self.position,
                                  "rotation": self.follow_rotate,
                                  "avatar_id": self.avatar_id})

    def _get_look_at_commands(self) -> List[dict]:
        """
        :return: A command for looking at a target.
        """

        commands = []
        if self.look_at_target is None:
            return commands
        # Look at and focus on the object.
        elif isinstance(self.look_at_target, int):
            commands.extend([{"$type": "look_at",
                              "object_id": self.look_at_target,
                              "use_centroid": True,
                              "avatar_id": self.avatar_id},
                             {"$type": "focus_on_object",
                              "object_id": self.look_at_target,
                              "use_centroid": True,
                              "avatar_id": self.avatar_id}])
        elif isinstance(self.look_at_target, dict):
            commands.append({"$type": "look_at_position",
                             "position": self.look_at_target,
                             "avatar_id": self.avatar_id})
        else:
            raise TypeError(f"Invalid look-at target: {self.look_at_target}")
