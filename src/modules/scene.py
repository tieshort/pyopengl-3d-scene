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
        self.aspect = aspect

        self.camera = Camera(glm.vec3(0, -1, 2))

        self.projection_matrix = glm.perspective(glm.radians(90), self.aspect, 0.01, 100.0)
        self.view_matrix = glm.lookAt(self.camera.position, self.camera.target, self.camera.up)

        # self.projection_matrix = glm.mat4(1)
        # self.view_matrix = glm.mat4(1)

    def render(self, **kwargs: any):
        for model in self.objects:
            try:
                model.render(
                    projection_matrix = self.projection_matrix,
                    view_matrix = self.view_matrix,
                    view_position = self.camera.target,
                    dir_lights = self.dirLights,
                    point_lights = self.pointLights,
                    spot_lights = self.spotLights,
                    **kwargs
                    )
            except Exception as e:
                print(f"{model} is not rendered")
                print(f"Detail: {e}")

class Camera:
    def __init__(self, position = glm.vec3(0, 0, 1), target = glm.vec3(0), up = glm.vec3(0, 1, 0)):
        self.position = position
        self.target = target
        self.up = up