from typing import List, Dict, Optional
from tdw.output_data import OutputData, Environments
from tdw.scene.room_bounds import RoomBounds


class SceneBounds:
    """
    Data for the scene bounds and its rooms.
    """

    def __init__(self, resp: List[bytes]):
        """
        :param resp: The response from the build.
        """

        env: Optional[Environments] = None
        for i in range(len(resp) - 1):
            r_id = OutputData.get_data_type_id(resp[i])
            if r_id == "envi":
                env = Environments(resp[i])
                break
        assert env is not None, "No scene data in response from build!"

        # Get the overall size of the scene.
        """:field
        Minimum x positional coordinate of the scene.
        """
        self.x_min: float = 1000
        """:field
        Maximum x positional coordinate of the scene.
        """
        self.x_max: float = 0
        """:field
        Minimum z positional coordinate of the scene.
        """
        self.z_min: float = 1000
        """:field
        Maximum z positional coordinate of the scene.
        """
        self.z_max: float = 0
        """:field
        All of the rooms in the scene.
        """
        self.rooms: List[RoomBounds] = list()
        for i in range(env.get_num()):
            e = RoomBounds(env=env, i=i)
            if e.x_min < self.x_min:
                self.x_min = e.x_min
            if e.z_min < self.z_min:
                self.z_min = e.z_min
            if e.x_max > self.x_max:
                self.x_max = e.x_max
            if e.z_max > self.z_max:
                self.z_max = e.z_max
            self.rooms.append(e)

    def get_bounds(self) -> Dict[str, float]:
        """
        :return: A dictionary of bounds data.
        """

        return {"x_min": self.x_min,
                "x_max": self.x_max,
                "z_min": self.z_min,
                "z_max": self.z_max}
