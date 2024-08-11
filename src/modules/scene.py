import glm
from OpenGL.GL import glGetError

class Scene:
    def __init__(self, aspect):
        self.objects = []
        self.light_sources = []

        self.background_color = (0, 0, 0)
        self.background_texture = None
        self.aspect = aspect

        self.projection_matrix = glm.perspective(glm.radians(90), self.aspect, 0.01, 100.0)
        self.view_matrix = glm.lookAt(glm.vec3(0, 0, 2), glm.vec3(0), glm.vec3(0, 1, 0))

    def render(self, **kwargs: any):
        for model in self.objects:
            try:
                model.render(
                    projection_matrix = self.projection_matrix,
                    view_matrix = self.view_matrix,
                    **kwargs
                    )
            except Exception as e:
                print(f"{model} is not rendered")
                print(f"Detail: {e}")

    def set_light(self, 
                  model = None):
        if model is not None:
            self.objects.append(model)