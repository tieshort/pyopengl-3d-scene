import glm
import numpy as np


class Primitive:
    vertices: np.ndarray
    indices: np.ndarray
    normals: np.ndarray
    tex_coords: np.ndarray


class Square(Primitive):
    vertices = np.array(
        [
            glm.vec3(-1, -1, 0),
            glm.vec3(1, -1, 0),
            glm.vec3(1, 1, 0),
            glm.vec3(-1, 1, 0),
        ],
        dtype="float32",
    )

    indices = np.array([0, 1, 2, 2, 3, 0], dtype="uint32")

    normals = np.array(
        [
            glm.vec3(0, 0, 1),
            glm.vec3(0, 0, 1),
            glm.vec3(0, 0, 1),
            glm.vec3(0, 0, 1),
        ],
        dtype="float32",
    )

    texcoords = np.array(
        [
            glm.vec2(0, 0),
            glm.vec2(1, 0),
            glm.vec2(1, 1),
            glm.vec2(0, 1),
        ],
        dtype="float32",
    )


class Cube(Primitive):
    vertices = np.array(
        [
            glm.vec3(1, 1, 1),   # 0
            glm.vec3(-1, 1, 1),  # 1
            glm.vec3(-1, -1, 1), # 2
            glm.vec3(1, -1, 1),  # 3
            glm.vec3(1, 1, -1),  # 4
            glm.vec3(-1, 1, -1), # 5
            glm.vec3(-1, -1, -1),# 6
            glm.vec3(1, -1, -1), # 7
        ],
        dtype="float32",
    )

    indices = np.array(
        [
            0, 1, 2, 2, 3, 0,  # Front face
            4, 7, 6, 6, 5, 4,  # Back face
            0, 3, 7, 7, 4, 0,  # Right face
            1, 5, 6, 6, 2, 1,  # Left face
            1, 0, 4, 4, 5, 1,  # Top face
            3, 2, 6, 6, 7, 3,  # Bottom face
        ],
        dtype="uint32",
    )

    normals = np.array(
        [
            glm.vec3(0, 0, 1),  # Front face
            glm.vec3(0, 0, 1),
            glm.vec3(0, 0, 1),
            glm.vec3(0, 0, 1),

            glm.vec3(0, 0, -1), # Back face
            glm.vec3(0, 0, -1),
            glm.vec3(0, 0, -1),
            glm.vec3(0, 0, -1),

            glm.vec3(1, 0, 0),  # Right face
            glm.vec3(1, 0, 0),
            glm.vec3(1, 0, 0),
            glm.vec3(1, 0, 0),

            glm.vec3(-1, 0, 0), # Left face
            glm.vec3(-1, 0, 0),
            glm.vec3(-1, 0, 0),
            glm.vec3(-1, 0, 0),

            glm.vec3(0, 1, 0),  # Top face
            glm.vec3(0, 1, 0),
            glm.vec3(0, 1, 0),
            glm.vec3(0, 1, 0),

            glm.vec3(0, -1, 0), # Bottom face
            glm.vec3(0, -1, 0),
            glm.vec3(0, -1, 0),
            glm.vec3(0, -1, 0),
        ],
        dtype="float32",
    )

    texcoords = np.array(
        [
            glm.vec2(1, 1),  # Front face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),

            glm.vec2(1, 1),  # Back face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),

            glm.vec2(1, 1),  # Right face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),

            glm.vec2(1, 1),  # Left face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),

            glm.vec2(1, 1),  # Top face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),

            glm.vec2(1, 1),  # Bottom face
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),
        ],
        dtype="float32",
    )
