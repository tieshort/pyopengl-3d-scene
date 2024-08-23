import glm
from modules.structures import DirLight, PointLight, SpotLight
from typing import Iterable

class Scene:
    def __init__(self, aspect):
        self.objects = []
        self.dirLights: Iterable[DirLight] = []
        self.pointLights: Iterable[PointLight] = []
        self.spotLights: Iterable[SpotLight] = []

        self.background_color = glm.vec3(0)
        self.background_texture = None

        self.camera = Camera(glm.vec3(0, -1, 2))
        self.delta_time = 0.0
        self.last_frame_time = 0.0

        self.fov = 90.0
        self.aspect = aspect
        self.near = 0.01
        self.far = 100.0

    def render(self, time: float = 0, **kwargs: any):
        self.delta_time = time - self.last_frame_time
        self.last_frame_time = time
        for model in self.objects:
            try:
                model.render(
                    projection_matrix = glm.perspective(glm.radians(self.fov), 
                                                        self.aspect,
                                                        self.near,
                                                        self.far),
                    view_matrix = self.camera.get_view_matrix(),
                    view_position = self.camera.position + self.camera.target,
                    time = time,
                    dir_lights = self.dirLights,
                    point_lights = self.pointLights,
                    spot_lights = self.spotLights,
                    **kwargs
                    )
            except Exception as e:
                print(f"{model} is not rendered")
                print(f"Detail: {e}")

class Camera:
    def __init__(self, 
                 position = glm.vec3(0, 0, 3), 
                 target = glm.vec3(0, 0, -1), 
                 up = glm.vec3(0, 1, 0)):
        self.position = position
        self.target = target
        self.up = up

        self.yaw = -90.0
        self.pitch = 0.0
        self.sensitivity = 0.3
        self.speed = 0.1

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.target, self.up)