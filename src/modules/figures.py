import glm
import numpy as np

class Primitive:
    vertices: np.ndarray
    indices: np.ndarray

class Square(Primitive):
    vertices = np.array([
        glm.vec3(-1, -1, 0),
        glm.vec3(1, -1, 0),
        glm.vec3(1, 1, 0),
        glm.vec3(-1, 1, 0)], dtype = 'float32')
    
    indices = np.array([
        0, 1, 2, 2, 3, 0
        ], dtype='uint32')
    
class Cube(Primitive):
    vertices = np.array([
        glm.vec3(1, 1, 1),
        glm.vec3(-1, 1, 1),
        glm.vec3(-1, -1, 1),
        glm.vec3(1, -1, 1),
        glm.vec3(1, 1, -1),
        glm.vec3(-1, 1, -1),
        glm.vec3(-1, -1, -1),
        glm.vec3(1, -1, -1)], dtype = 'float32')
    
    indices = np.array([
        0, 1, 2,
        2, 3, 0,
        4, 5, 6,
        6, 7, 4,
        0, 4, 5,
        5, 1, 0,
        1, 5, 6,
        6, 2, 1,
        2, 6, 7,
        7, 3, 2,
        3, 7, 4,
        4, 0, 3
        ], dtype='uint32')
