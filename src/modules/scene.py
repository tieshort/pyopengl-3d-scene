import re, glob
import glm
from modules.structures import DirLight, PointLight, SpotLight
from config import SHADERS_DIR
from typing import Iterable
from functools import wraps


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
        self.animation_time = 0.0

        self.fov = 90.0
        self.aspect = aspect
        self.near = 0.01
        self.far = 100.0

    def update_shader_lights_count(self):
        shader_file_pattern = "fs*.glsl"
        shader_files = glob.glob(f'{SHADERS_DIR}/{shader_file_pattern}')

        patterns = (
            r'#define NUM_DIRLIGHTS \d+',
            r'#define NUM_POINTLIGHTS \d+',
            r'#define NUM_SPOTLIGHTS \d+'
        )
        repls = (
            f'#define NUM_DIRLIGHTS {len(self.dirLights)}',
            f'#define NUM_POINTLIGHTS {len(self.pointLights)}',
            f'#define NUM_SPOTLIGHTS {len(self.spotLights)}'
        )

        for file in shader_files:
            with open(file, 'r') as f:
                shader = f.read()

            for pattern, repl in zip(patterns, repls):
                shader = re.sub(pattern, repl, shader)

            with open(file, 'w') as f:
                f.write(shader)

    def render(self, time: float = 0, **kwargs: any):
        self.delta_time = time - self.last_frame_time
        self.last_frame_time = time
        for model in self.objects:
            try:
                model.render(
                    projection_matrix=glm.perspective(
                        glm.radians(self.fov), self.aspect, self.near, self.far
                    ),
                    view_matrix=self.camera.get_view_matrix(),
                    view_position=self.camera.position,
                    time=time,
                    dir_lights=self.dirLights,
                    point_lights=self.pointLights,
                    spot_lights=self.spotLights,
                    **kwargs,
                )
            except Exception as e:
                print(f"{model} is not rendered")
                print(f"Detail: {e}")

    def animate_object(self, index):
        def outer_wrapper(animation):
            @wraps(animation)
            def inner_wrapper(*args, **kwargs):
                self.animation_time += self.delta_time
                self.objects[index] = animation(
                    self.objects[index], 
                    time = self.animation_time,
                    delta_time = self.delta_time, 
                    *args, 
                    **kwargs
                )
                return self.objects[index]
            return inner_wrapper
        return outer_wrapper


class Camera:
    def __init__(
        self,
        position=glm.vec3(0, 0, 3),
        target=glm.vec3(0, 0, -1),
        up=glm.vec3(0, 1, 0),
    ):
        self.position = position
        self.target = target
        self.up = up

        self.yaw = -90.0
        self.pitch = 0.0
        self.sensitivity = 0.3
        self.speed = 1

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.target, self.up)
