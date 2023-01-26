from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.oculus_leap_motion import OculusLeapMotion

"""
Minimal Oculus Leap Motion example.
"""

c = Controller()
vr = OculusLeapMotion()
c.add_ons.append(vr)
c.communicate([TDWUtils.create_empty_room(12, 12),
               c.get_add_object(model_name="rh10",
                                object_id=Controller.get_unique_id(),
                                position={"x": 0, "y": 0, "z": 0.5}),
               {"$type": "set_teleportation_area"}])
while True:
    c.communicate([])
