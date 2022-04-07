from tdw.controller import Controller
from tdw.add_ons.obi import Obi
from tdw.add_ons.third_person_camera import ThirdPersonCamera



"""
Minimal example of dropping a cloth sheet onto an object.
"""

c = Controller(launch_build=False)
c.communicate(Controller.get_add_scene(scene_name="tdw_room"))
cloth_id = Controller.get_unique_id()
receptacle_id = Controller.get_unique_id()
camera = ThirdPersonCamera(position={"x": -3.75, "y": 1.5, "z": -0.5},
                           look_at={"x": 0, "y": 0.5, "z": 0})
obi = Obi(output_data=False)
c.add_ons.extend([camera, obi])

# Create a disk-shaped emitter, pointing straight down.
obi.create_cloth_sheet(cloth_material="silk",
                       object_id=cloth_id,
                       position={"x": 0, "y": 3.0, "z": 0},
                       rotation={"x": 0, "y": 0, "z": 0},
                       sheet_type="cloth_vhd",
                       solver_id=0)
# Add an object for the fluid to interact with.
c.communicate(Controller.get_add_physics_object(model_name="sphere",
                                                object_id=receptacle_id,
                                                library="models_flex.json",
                                                kinematic=True,
                                                gravity=False,
                                                scale_factor={"x":1, "y": 1, "z":1}))
c.communicate([{"$type": "set_screen_size",
                "width": 1920,
                "height": 1080},
               {"$type": "set_render_quality",
                "render_quality": 5}])
c.communicate([{"$type": "set_obi_solver_substeps",  "solver_id": 0, "substeps": 2},
               {"$type": "set_obi_solver_scale",  "solver_id": 0, "scale_factor": 0.5}])

for i in range(750):
    c.communicate([])
c.communicate({"$type": "terminate"})