import glm, ctypes, tinyobjloader
import numpy as np
from OpenGL.GL import *
from modules.figures import Primitive
from modules.materials import Material, white_rubber
from modules.light import Light
from config import SHADERS_DIR, MODELS_DIR

sizeof_float = ctypes.sizeof(ctypes.c_float)
void_p = ctypes.c_void_p

class BaseModel:
    def __init__(self, 
                 vertices: np.ndarray,
                 vertex_indices: np.ndarray,
                 normals: np.ndarray = None,
                 texcoords: np.ndarray = None,
                 material: Material = white_rubber,
                 vertexShader: str = "vs.glsl", 
                 fragmentShader: str = "fs.glsl"):
        self.vao = GLuint(0)
        self.vbo = GLuint(0)
        self.ebo = GLuint(0)

        glGenVertexArrays(1, self.vao)
        glGenBuffers(1, self.vbo)
        glGenBuffers(1, self.ebo)

        self.shaderProgram = load_shaders(f"{SHADERS_DIR}/{vertexShader}", f"{SHADERS_DIR}/{fragmentShader}")

        self.vertex_count = len(vertices)
        self.index_count = len(vertex_indices)

        vertices_size = vertices.nbytes
        normals_size = normals.nbytes if normals is not None else 0
        texcoords_size = texcoords.nbytes if texcoords is not None else 0

        glBindVertexArray(self.vao)

        buffer_size = vertices_size + normals_size + texcoords_size
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, buffer_size, None, GL_STATIC_DRAW)

        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices_size, vertices.data)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(0))
        glEnableVertexAttribArray(0)

        if normals is not None:
            glBufferSubData(GL_ARRAY_BUFFER, vertices_size, normals_size, normals.data)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(vertices_size))
            glEnableVertexAttribArray(1)

        if texcoords is not None:
            glBufferSubData(GL_ARRAY_BUFFER, vertices_size + normals_size, texcoords_size, texcoords.data)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 2 * sizeof_float, void_p(vertices_size + normals_size))
            glEnableVertexAttribArray(2)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, vertex_indices.nbytes, vertex_indices.data, GL_STATIC_DRAW)

        glBindVertexArray(0)

        self.model_matrix = glm.mat4(1)

        self.ambient = material.ambient
        self.diffuse = material.diffuse
        self.specular = material.specular
        self.shininess = material.shininess

    def render(self, 
               resolution: tuple[int, int] = None,
               time: float = 0.0,
               light: Light = None,
               animation_mode: bool = False,
               projection_matrix: glm.mat4 = glm.mat4(1),
               view_matrix: glm.mat4 = glm.mat4(1),
               **kwargs: any):
        if light is None:
            light_pos = glm.vec3(0.5)
            view_pos = glm.vec3(0)
            light_color = glm.vec3(1)
        else:
            light_pos = light.position
            view_pos = light.view_position
            light_color = light.color

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
                 material: Material = white_rubber,
                 vertexShader: str = "vs.glsl", 
                 fragmentShader: str = "fs.glsl"):
        vertices = figure.vertices
        indices = figure.indices

        super().__init__(
            vertices,
            indices,
            material = material,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader)

class Model(BaseModel):
    def __init__(self, 
                 filename: str,
                 material: Material = white_rubber,
                 vertexShader: str = "vs.glsl", 
                 fragmentShader: str = "fs.glsl"):
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

        super().__init__(
            vertices,
            vertex_indices,
            normals,
            material = material,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader)


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