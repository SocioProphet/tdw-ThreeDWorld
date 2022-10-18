from __future__ import annotations
from typing import List
from tdw.replicant.actions.action import Action
from tdw.replicant.action_status import ActionStatus
from tdw.replicant.collision_detection import CollisionDetection
from tdw.replicant.replicant_dynamic import ReplicantDynamic
from tdw.replicant.replicant_static import ReplicantStatic
from tdw.replicant.image_frequency import ImageFrequency
from tdw.controller import Controller
from tdw.librarian import HumanoidAnimationLibrarian, HumanoidAnimationRecord


class Animate(Action):
    """
    Play an animation.

    The animation will end either when the animation clip is finished or if the Replicant collides with something (see `self.collision_detection`).
    The collision detection will respond normally to walls, objects, obstacle avoidance, etc.
    Additionally, if the previous action was `Animate`, and it was the same animation, and it ended in a collision, this action fails immediately without trying to play the animation.
    """

    def __init__(self, animation: str, collision_detection: CollisionDetection, forward: bool = True,
                 library: str = "humanoid_animations.json", previous: Action = None):
        """
        :param animation: The name of the animation.
        :param collision_detection: The [`CollisionDetection`](../collision_detection.md) rules.
        :param forward: If True, play the animation forwards. If False, play the animation backwards.
        :param library: The name animation library.
        :param previous: The previous action. Can be None.
        """

        super().__init__()
        # Add the animation library.
        if library not in Controller.HUMANOID_ANIMATION_LIBRARIANS:
            Controller.HUMANOID_ANIMATION_LIBRARIANS[library] = HumanoidAnimationLibrarian(library)
        """:field
        The `HumanoidAnimationRecord` of the animation.
        """
        self.record: HumanoidAnimationRecord = Controller.HUMANOID_ANIMATION_LIBRARIANS[library].get_record(animation)
        """:field
        The [`CollisionDetection`](../collision_detection.md) rules.
        """
        self.collision_detection: CollisionDetection = collision_detection
        # Don't try to play the same animation twice if the first one ended in a collision.
        if self.collision_detection.previous_was_same and previous is not None and isinstance(previous, Animate) and \
                previous.status == ActionStatus.collision and previous.record.name == self.record.name:
            self.status = ActionStatus.collision
        """:field
        If True, play the animation forwards. If False, play the animation backwards.
        """
        self.forward: bool = forward

    def get_initialization_commands(self, resp: List[bytes], static: ReplicantStatic, dynamic: ReplicantDynamic,
                                    image_frequency: ImageFrequency) -> List[dict]:
        commands = super().get_initialization_commands(resp=resp, static=static, dynamic=dynamic,
                                                       image_frequency=image_frequency)
        # Download the animation if needed. Play the animation.
        commands.extend([{"$type": "add_humanoid_animation",
                          "name": self.record.name,
                          "url": self.record.get_url()},
                         {"$type": "play_humanoid_animation",
                          "name": self.record.name,
                          "id": static.replicant_id,
                          "framerate": self.record.framerate,
                          "forward": self.forward}])
        return commands

    def get_ongoing_commands(self, resp: List[bytes], static: ReplicantStatic, dynamic: ReplicantDynamic) -> List[dict]:
        # If there was a collision, stop the animation.
        if len(dynamic.get_collision_enters(collision_detection=self.collision_detection)) > 0:
            self.status = ActionStatus.collision
        # Continue the animation.
        elif self._get_motion_complete(replicant_id=static.replicant_id, resp=resp):
            self.status = ActionStatus.success
        return []

    def get_end_commands(self, resp: List[bytes], static: ReplicantStatic, dynamic: ReplicantDynamic,
                         image_frequency: ImageFrequency) -> List[dict]:
        commands = super().get_end_commands(resp=resp, static=static, dynamic=dynamic, image_frequency=image_frequency)
        # Stop the animation.
        commands.append({"$type": "stop_humanoid_animation",
                         "id": static.replicant_id})
        return commands
