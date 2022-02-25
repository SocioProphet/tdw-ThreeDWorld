from typing import List, Dict, Tuple, Union
import numpy as np
from tdw.tdw_utils import TDWUtils
from tdw.scene_data.interior_region import InteriorRegion
from tdw.cardinal_direction import CardinalDirection
from tdw.librarian import ModelRecord
from tdw.proc_gen.arrangements.kitchen_counter_top_base import KitchenCounterTopBase


class Dishwasher(KitchenCounterTopBase):
    """
    A dishwasher with a kitchen counter top with objects on it.

    - The dishwasher model is chosen randomly; see `Dishwasher.MODEL_CATEGORIES["dishwasher"]`.
    - The dishwasher is placed next to a wall.
      - The dishwasher's position is automatically adjusted to set it flush to the way.
      - The dishwasher is automatically rotated so that it faces away from the wall.
    - The dishwasher has a floating kitchen counter top above it.
    - The floating kitchen counter top always has a rectangular arrangement of objects on top of it. The objects are chosen randomly; see `Dishwasher.ON_TOP_OF["kitchen_counter"]`.
    - All dishwashers have a door that can be opened.
    - The root object of the dishwasher is kinematic and the door sub-object is non-kinematic.
    """

    _DISHWASHER_OFFSET: float = 0.025

    def __init__(self, direction: CardinalDirection, material: str, wall: CardinalDirection, region: InteriorRegion,
                 model: Union[str, ModelRecord], position: Dict[str, float], rng: np.random.RandomState):
        """
        :param direction: The direction of the lateral arrangement.
        :param material: The name of the visual material.
        :param wall: The wall as a [`CardinalDirection`](../../cardinal_direction.md) that the root object is next to.
        :param region: The [`InteriorRegion`](../../scene_data/interior_region.md) that the object is in.
        :param model: Either the name of the model (in which case the model must be in `models_core.json` or a `ModelRecord`.
        :param position: The position of the root object. This might be adjusted.
        :param rng: The random number generator.
        """

        self._direction: CardinalDirection = direction
        super().__init__(material=material, wall=wall, region=region, model=model, position=position, rng=rng)

    def get_commands(self) -> List[dict]:
        commands = self._add_root_object()
        commands.extend(super().get_commands())
        commands.extend(self._get_rotation_commands())
        return commands

    def _get_position(self, position: Dict[str, float]) -> Dict[str, float]:
        depth = self._get_depth()
        if self._wall == CardinalDirection.north:
            pos = {"x": position["x"],
                   "y": 0,
                   "z": self._region.z_max - depth / 2}
        elif self._wall == CardinalDirection.south:
            pos = {"x": position["x"],
                   "y": 0,
                   "z": self._region.z_min + depth / 2}
        elif self._wall == CardinalDirection.west:
            pos = {"x": self._region.x_min + depth / 2,
                   "y": 0,
                   "z": position["z"]}
        elif self._wall == CardinalDirection.east:
            pos = {"x": self._region.x_max - depth / 2,
                   "y": 0,
                   "z": position["z"]}
        else:
            raise Exception(self._wall)
        # Offset the position to leave a little gap.
        if self._direction == CardinalDirection.north:
            pos["z"] += Dishwasher._DISHWASHER_OFFSET
        elif self._direction == CardinalDirection.south:
            pos["z"] -= Dishwasher._DISHWASHER_OFFSET
        elif self._direction == CardinalDirection.east:
            pos["x"] += Dishwasher._DISHWASHER_OFFSET
        elif self._direction == CardinalDirection.west:
            pos["x"] -= Dishwasher._DISHWASHER_OFFSET
        else:
            raise Exception(self._direction)
        return pos

    def get_length(self) -> float:
        return TDWUtils.get_bounds_extents(bounds=self._record.bounds)[0]

    def _get_rotation(self) -> float:
        if self._wall == CardinalDirection.north:
            return 180
        elif self._wall == CardinalDirection.east:
            return 270
        elif self._wall == CardinalDirection.south:
            return 0
        else:
            return 90

    def _get_depth(self) -> float:
        return TDWUtils.get_bounds_extents(bounds=self._record.bounds)[2]

    def _get_size(self) -> Tuple[float, float]:
        extents = TDWUtils.get_bounds_extents(bounds=self._record.bounds)
        return extents[0] + Dishwasher._DISHWASHER_OFFSET * 2, Dishwasher.DEFAULT_CELL_SIZE

    def _get_category(self) -> str:
        return "dishwasher"
