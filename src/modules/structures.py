import glm
from OpenGL.GL import *


class DirLight:
    def __init__(
        self,
        direction: glm.vec3,
        ambient: glm.vec3 = glm.vec3(0.2),
        diffuse: glm.vec3 = glm.vec3(0.8),
        specular: glm.vec3 = glm.vec3(1.0)
    ):
        self.direction = direction
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def set_uniforms(self, program, index: int, *ars: any, **kwargs: any):
        glUniform3fv(
            glGetUniformLocation(program, f"dirlights[{index}].direction"),
            1,
            glm.value_ptr(self.direction),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"dirlights[{index}].ambient"),
            1,
            glm.value_ptr(self.ambient),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"dirlights[{index}].diffuse"),
            1,
            glm.value_ptr(self.diffuse),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"dirlights[{index}].specular"),
            1,
            glm.value_ptr(self.specular),
        )


class PointLight:
    def __init__(
        self,
        position: glm.vec3,
        ambient: glm.vec3 = glm.vec3(0.2),
        diffuse: glm.vec3 = glm.vec3(0.8),
        specular: glm.vec3 = glm.vec3(1.0),
        constant: float = 1.0,
        linear: float = 0.35,
        quadratic: float = 0.45,
    ):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic

    def set_uniforms(self, program, index: int, *args: any, **kwargs: any):
        glUniform3fv(
            glGetUniformLocation(program, f"pointlights[{index}].position"),
            1,
            glm.value_ptr(self.position),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"pointlights[{index}].ambient"),
            1,
            glm.value_ptr(self.ambient),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"pointlights[{index}].diffuse"),
            1,
            glm.value_ptr(self.diffuse),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"pointlights[{index}].specular"),
            1,
            glm.value_ptr(self.specular),
        )
        glUniform1f(
            glGetUniformLocation(program, f"pointlights[{index}].constant"),
            self.constant,
        )
        glUniform1f(
            glGetUniformLocation(program, f"pointlights[{index}].linear"), self.linear
        )
        glUniform1f(
            glGetUniformLocation(program, f"pointlights[{index}].quadratic"),
            self.quadratic,
        )


class SpotLight:
    def __init__(
        self,
        position: glm.vec3,
        direction: glm.vec3,
        ambient: glm.vec3 = glm.vec3(0.2),
        diffuse: glm.vec3 = glm.vec3(0.8),
        specular: glm.vec3 = glm.vec3(1.0),
        constant: float = 1.0,
        linear: float = 0.045,
        quadratic: float = 0.0075,
        cutOff: float = 35.0,
        outerCutOff: float = 45.0,
    ):
        self.position = position
        self.direction = direction
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        self.cutOff = glm.cos(glm.radians(cutOff))
        self.outerCutOff = glm.cos(glm.radians(outerCutOff))

    def set_uniforms(self, program, index: int, *args: any, **kwargs: any):
        glUniform3fv(
            glGetUniformLocation(program, f"spotlights[{index}].position"),
            1,
            glm.value_ptr(self.position),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"spotlights[{index}].direction"),
            1,
            glm.value_ptr(self.direction),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"spotlights[{index}].ambient"),
            1,
            glm.value_ptr(self.ambient),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"spotlights[{index}].diffuse"),
            1,
            glm.value_ptr(self.diffuse),
        )
        glUniform3fv(
            glGetUniformLocation(program, f"spotlights[{index}].specular"),
            1,
            glm.value_ptr(self.specular),
        )
        glUniform1f(
            glGetUniformLocation(program, f"spotlights[{index}].constant"),
            self.constant,
        )
        glUniform1f(
            glGetUniformLocation(program, f"spotlights[{index}].linear"), self.linear
        )
        glUniform1f(
            glGetUniformLocation(program, f"spotlights[{index}].quadratic"),
            self.quadratic,
        )
        glUniform1f(
            glGetUniformLocation(program, f"spotlights[{index}].cutOff"), self.cutOff
        )
        glUniform1f(
            glGetUniformLocation(program, f"spotlights[{index}].outerCutOff"),
            self.outerCutOff,
        )


class Material:
    def __init__(
        self,
        name: str,
        ambient: glm.vec3,
        diffuse: glm.vec3,
        specular: glm.vec3,
        shininess: float,
    ):
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess * 128

    def __repr__(self):
        return f"Material(name={self.name}, ambient={self.ambient}, diffuse={self.diffuse}, specular={self.specular}, shininess={self.shininess})"
