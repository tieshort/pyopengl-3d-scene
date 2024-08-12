import glm
from modules.light import Light

class Scene:
    def __init__(self, aspect):
        self.objects = []
        self.light_sources = []
        self.light = None

        self.background_color = glm.vec3(0)
        self.background_texture = None
        self.aspect = aspect

        self.center = glm.vec3(0)

        self.projection_matrix = glm.perspective(glm.radians(90), self.aspect, 0.01, 100.0)
        self.view_matrix = glm.lookAt(glm.vec3(0, 0, 2), self.center, glm.vec3(0, 1, 0))

    def render(self, **kwargs: any):
        for model in self.objects:
            try:
                model.render(
                    light = self.light,
                    projection_matrix = self.projection_matrix,
                    view_matrix = self.view_matrix,
                    **kwargs
                    )
            except Exception as e:
                print(f"{model} is not rendered")
                print(f"Detail: {e}")

    def set_light(self, 
                  model = None,
                  light: Light = Light(glm.vec3(0.1), glm.vec3(0), glm.vec3(0))):
        if model is not None:
            model.translate(light.position)
            self.objects.append(model)
        self.light = light