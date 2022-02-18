from pathlib import Path
from json import loads
from pkg_resources import resource_filename
from abc import ABC, abstractmethod
from typing import Dict, List
from tdw.add_ons.container_manager_data.container_collider_tag import ContainerColliderTag
from tdw.add_ons.container_manager_data.container_trigger_collider_decoder import ContainerTriggerColliderDecoder
from tdw.collision_data.trigger_collider_shape import TriggerColliderShape


class ContainerTriggerCollider(ABC):
    """
    Data for a container trigger collider.
    """

    def __init__(self, tag: ContainerColliderTag, position: Dict[str, float]):
        """
        :param tag: The collider's semantic [`ContainerColliderTag`](container_collider_tag.md).
        :param position: The local position of the collider.
        """

        """:field
        The collider's semantic [`ContainerColliderTag`](container_collider_tag.md).
        """
        self.tag: ContainerColliderTag = tag
        """:field
        The collider's local position.
        """
        self.position: Dict[str, float] = {"x": round(position["x"], 8),
                                           "y": round(position["y"], 8),
                                           "z": round(position["z"], 8)}
        """:field
        The [`TriggerColliderShape`](../../collision_data/trigger_collider_shape.md).
        """
        self.shape: TriggerColliderShape = self._get_shape()

    @abstractmethod
    def _get_shape(self) -> TriggerColliderShape:
        """
        :return: The shape of the collider.
        """

        raise Exception()


# A dictionary of all container model names and their trigger colliders.
CONTAINERS: Dict[str, List[ContainerTriggerCollider]] = loads(Path(resource_filename(__name__, "colliders.json")).read_text(),
                                                              cls=ContainerTriggerColliderDecoder)
