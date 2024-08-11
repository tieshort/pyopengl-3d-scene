import glm

class Light:
    def __init__(self, color: glm.vec3, position: glm.vec3, view_position: glm.vec3):
        self.color = color
        self.position = position
        self.view_position = view_position