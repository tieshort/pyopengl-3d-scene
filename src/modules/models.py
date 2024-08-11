import glm, ctypes, tinyobjloader
import numpy as np
from OpenGL.GL import *
from modules.figures import Primitive
from modules.materials import Material, white_rubber
from config import SHADERS_DIR, MODELS_DIR

sizeof_float = ctypes.sizeof(ctypes.c_float)
void_p = ctypes.c_void_p

class BaseModel:
    def __init__(self, 
                 vertexShader: str, 
                 fragmentShader: str,
                 material: Material):
        self.vao = GLuint(0)
        self.vbo = GLuint(0)
        self.ebo = GLuint(0)

        self.shaderProgram = load_shaders(f"{SHADERS_DIR}/{vertexShader}", f"{SHADERS_DIR}/{fragmentShader}")

        glGenVertexArrays(1, self.vao)
        glGenBuffers(1, self.vbo)
        glGenBuffers(1, self.ebo)

        self.model_matrix = glm.mat4(1)

        self.ambient = material.ambient
        self.diffuse = material.diffuse
        self.specular = material.specular
        self.shininess = material.shininess

    def render(self, 
               resolution: tuple[int, int] = None,
               time: float = 0.0,
               light_color : glm.vec3 = glm.vec3(0.5),
               animation_mode: bool = False,
               projection_matrix: glm.mat4 = glm.mat4(1),
               view_matrix: glm.mat4 = glm.mat4(1),
               **kwargs: any):
        light_pos = glm.vec3(0.5)
        view_pos = glm.vec3(0)
        light_color = glm.vec3(1)

        ambient = self.ambient
        diffuse = self.diffuse
        specular = self.specular
        shininess = self.shininess

        glUseProgram(self.shaderProgram)

        # glUniform2fv(glGetUniformLocation(self.shaderProgram, "resolution"), 1, resolution)
        # glUniform1f(glGetUniformLocation(self.shaderProgram, "time"), time)
        glUniform3fv(glGetUniformLocation(self.shaderProgram, "lightPos"), 1, glm.value_ptr(light_pos))
        glUniform3fv(glGetUniformLocation(self.shaderProgram, "viewPos"), 1, glm.value_ptr(view_pos))
        glUniform3fv(glGetUniformLocation(self.shaderProgram, "lightColor"), 1, glm.value_ptr(light_color))

        glUniform3fv(glGetUniformLocation(self.shaderProgram, "ambient"), 1, glm.value_ptr(ambient))
        glUniform3fv(glGetUniformLocation(self.shaderProgram, "diffuse"), 1, glm.value_ptr(diffuse))
        glUniform3fv(glGetUniformLocation(self.shaderProgram, "specular"), 1, glm.value_ptr(specular))
        glUniform1f(glGetUniformLocation(self.shaderProgram, "shininess"), shininess)

        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "projection"), 1, GL_FALSE, glm.value_ptr(projection_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "model"), 1, GL_FALSE, glm.value_ptr(self.model_matrix));

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        glUseProgram(0)
        return self

    def translate(self, pos: glm.vec3):
        self.model_matrix = glm.translate(self.model_matrix, pos)
        return self

    def scale(self, scalers: glm.vec3):
        self.model_matrix = glm.scale(self.model_matrix, scalers)
        return self

    def rotate(self, angles: glm.vec3):
        angles = glm.radians(angles)
        self.model_matrix = glm.rotate(self.model_matrix, angles.x, glm.vec3(1, 0, 0))
        self.model_matrix = glm.rotate(self.model_matrix, angles.y, glm.vec3(0, 1, 0))
        self.model_matrix = glm.rotate(self.model_matrix, angles.z, glm.vec3(0, 0, 1))
        return self
    
class Figure(BaseModel):
    def __init__(self, 
                 figure: Primitive, 
                 vertexShader: str = "vs.glsl", 
                 fragmentShader: str = "fs.glsl",
                 material: Material = white_rubber):
        super().__init__(vertexShader = vertexShader, fragmentShader = fragmentShader, material = material)

        vertices = figure.vertices
        indices = figure.indices

        self.vertex_count = len(vertices)
        self.index_count = len(indices)


        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.data, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(3 * sizeof_float))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 2 * sizeof_float, void_p(6 * sizeof_float))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.data, GL_STATIC_DRAW)

        glBindVertexArray(0)

class Model(BaseModel):
    def __init__(self, 
                 filename: str,
                 vertexShader: str = "vs.glsl", 
                 fragmentShader: str = "fs.glsl",
                 material: Material = white_rubber):
        super().__init__(vertexShader = vertexShader, fragmentShader = fragmentShader, material = material)

        reader = tinyobjloader.ObjReader()
        if not reader.ParseFromFile(f"{MODELS_DIR}/{filename}"):
            print("Failed to load : ", filename)
            print("Warn:", reader.Warning())
            print("Err:", reader.Error())

        if reader.Warning():
            print("Warn:", reader.Warning())

        # Получение атрибутов из объекта reader
        attrib = reader.GetAttrib()
        shapes = reader.GetShapes()
        materials = reader.GetMaterials()

        # Подготовка массива вершин, нормалей и текстурных координат
        vertices = []
        normals = []
        texcoords = []
        vertex_indices = []

        for i in range(0, len(attrib.vertices), 3):
            vertices.append(glm.vec3(
                float(attrib.vertices[i]), 
                float(attrib.vertices[i + 1]), 
                float(attrib.vertices[i + 2])
            ))

        for i in range(0, len(attrib.normals), 3):
            normals.append(glm.vec3(
                float(attrib.normals[i]),
                float(attrib.normals[i + 1]),
                float(attrib.normals[i + 2])
            ))

        for i in range(0, len(attrib.texcoords), 2):
            texcoords.append(glm.vec2(
                float(attrib.texcoords[i]),
                float(attrib.texcoords[i + 1])
            ))

        vertices = np.array(vertices)
        normals = np.array(normals)
        texcoords = np.array(texcoords)

        for shape in shapes:
            for index in shape.mesh.indices:
                vertex_indices.append(index.vertex_index)

        vertex_indices = np.array(vertex_indices, dtype='uint32')

        self.vertex_count = len(vertices)
        self.index_count = len(vertex_indices)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes + normals.nbytes, None, GL_STATIC_DRAW)

        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices.data)
        glBufferSubData(GL_ARRAY_BUFFER, vertices.nbytes, normals.nbytes, normals.data)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(vertices.nbytes))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 2 * sizeof_float, void_p(6 * sizeof_float))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, vertex_indices.nbytes, vertex_indices.data, GL_STATIC_DRAW)

        glBindVertexArray(0)

# class Light(BaseModel):
#     def __init__(self, 
#                  figure: Primitive,
#                  vertexShader: str = "vs_light.glsl", 
#                  fragmentShader:str = "fs_light.glsl"):
#         super().__init__(vertexShader, fragmentShader)

#         vertices = figure.vertices
#         indices = figure.indices

#         self.vertex_count = len(vertices)
#         self.index_count = len(indices)

#         glBindVertexArray(self.vao)

#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
#         glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.data, GL_STATIC_DRAW)

#         glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(0))
#         glEnableVertexAttribArray(0)

#         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
#         glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.data, GL_STATIC_DRAW)

#         glBindVertexArray(0)

def load_shaders(vertexShaderPath: str, fragmentShaderPath: str):
    vertexShaderId: int = glCreateShader(GL_VERTEX_SHADER)
    fragmentShaderId: int = glCreateShader(GL_FRAGMENT_SHADER)

    with open(vertexShaderPath, 'r') as f:
        vertexShader = f.read()

    with open(fragmentShaderPath, 'r') as f:
        fragmentShader = f.read()

    try:
        print("Compiling shader: ", vertexShaderPath)
        glShaderSource(vertexShaderId, vertexShader)
        glCompileShader(vertexShaderId)
    except Exception as e:
        print("Error compiling vertex shader: ", e)

    try:
        print("Compiling shader: ", fragmentShaderPath)
        glShaderSource(fragmentShaderId, fragmentShader)
        glCompileShader(fragmentShaderId)
    except Exception as e:
        print("Error compiling fragment shader: ", e)

    try:
        print("Linking Program")
        shaderProgram: int = glCreateProgram()
        glAttachShader(shaderProgram, vertexShaderId)
        glAttachShader(shaderProgram, fragmentShaderId)
        glLinkProgram(shaderProgram)
    except Exception as e:
        print("Error linking program: ", e)

    glDeleteShader(vertexShaderId)
    glDeleteShader(fragmentShaderId)

    return shaderProgram