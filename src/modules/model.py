import glm, ctypes, tinyobjloader
import numpy as np
from OpenGL.GL import *
from PIL import Image

from modules.figures import Primitive
from modules.materials import white_rubber
from modules.structures import Material, DirLight, PointLight, SpotLight
from config import SHADERS_DIR, MODELS_DIR, IMAGES_DIR

sizeof_float = ctypes.sizeof(ctypes.c_float)
void_p = ctypes.c_void_p

class Model:
    def __init__(self, 
                 vertices: np.ndarray,
                 vertex_indices: np.ndarray,
                 normals: np.ndarray = None,
                 texcoords: np.ndarray = None,
                 material: Material = white_rubber,
                 diffuse_texture: str | None = None,
                 specular_texture: str | None = None,
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

        self.material = material
        self.diffuse_texture = None
        self.specular_texture = None

        if texcoords is not None:
            if diffuse_texture is not None:
                self.diffuse_texture = load_texture(diffuse_texture)
            if specular_texture is not None:
                self.specular_texture = load_texture(specular_texture)
        print(f'{self.diffuse_texture = }')
        print(f'{self.specular_texture = }')
    
    @classmethod
    def from_figure(cls,
                    figure: Primitive,
                    material: Material = white_rubber,
                    diffuse_texture: str | None = None,
                    specular_texture: str | None = None,
                    vertexShader: str = "vs.glsl", 
                    fragmentShader: str = "fs.glsl"):
        vertices = figure.vertices
        indices = figure.indices
        return cls(
            vertices,
            indices,
            material = material,
            diffuse_texture = diffuse_texture,
            specular_texture = specular_texture,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader
        )
    
    @classmethod
    def from_model(cls,
                   filename: str,
                   material: Material = white_rubber,
                   diffuse_texture: str | None = None,
                   specular_texture: str | None = None,
                   vertexShader: str = "vs.glsl", 
                   fragmentShader: str = "fs.glsl"):
        reader = tinyobjloader.ObjReader()

        print(f"loading {filename}")

        if not reader.ParseFromFile(f"{MODELS_DIR}/{filename}"):
            print("Failed to load : ", filename)
            print("Warn:", reader.Warning())
            print("Err:", reader.Error())

        if reader.Warning():
            print("Warn:", reader.Warning())

        print(f"{filename} loaded succesfully")

        # Получение атрибутов из объекта reader
        attrib = reader.GetAttrib()
        shapes = reader.GetShapes()
        materials = reader.GetMaterials()

        # Подготовка массива вершин, нормалей и текстурных координат
        vertices = np.array(attrib.vertices, dtype = 'float32').reshape(-1, 3)
        normals = np.array(attrib.normals, dtype = 'float32').reshape(-1, 3)
        texcoords = np.array(attrib.texcoords, dtype = 'float32').reshape(-1, 2)

        vertex_indices = np.array([index.vertex_index for shape in shapes for index in shape.mesh.indices], dtype = 'uint32')
        return cls(
            vertices,
            vertex_indices,
            normals,
            texcoords,
            material = material,
            diffuse_texture = diffuse_texture,
            specular_texture = specular_texture,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader
        )

    def render(self, 
               projection_matrix: glm.mat4 = glm.mat4(1),
               view_matrix: glm.mat4 = glm.mat4(1),
               view_position: glm.vec3 = glm.vec3(0),
               resolution: tuple[int, int] = None,
               time: float = 0.0,
               animation_mode: bool = False,
               dir_lights = None,
               point_lights = None,
               spot_lights = None,
               **kwargs: any):
        view_pos = view_position

        ambient = self.material.ambient
        diffuse = self.material.diffuse
        specular = self.material.specular
        shininess = self.material.shininess

        glUseProgram(self.shaderProgram)

        glUniform2fv(glGetUniformLocation(self.shaderProgram, "resolution"), 1, resolution)
        glUniform1f(glGetUniformLocation(self.shaderProgram, "time"), time)

        glUniform3fv(glGetUniformLocation(self.shaderProgram, "viewPos"), 1, glm.value_ptr(view_pos))

        if dir_lights is not None:
            for i, light in enumerate(dir_lights):
                light.set_uniforms(self.shaderProgram, i)

        if point_lights is not None:
            for i, light in enumerate(point_lights):
                light.set_uniforms(self.shaderProgram, i)

        if spot_lights is not None:
            for i, light in enumerate(spot_lights):
                light.set_uniforms(self.shaderProgram, i)

        glUniform3fv(glGetUniformLocation(self.shaderProgram, "material.ambient"), 1, glm.value_ptr(ambient))
        if self.diffuse_texture is None:
            glUniform3fv(glGetUniformLocation(self.shaderProgram, "material.diffuse"), 1, glm.value_ptr(diffuse))
        if self.specular_texture is None:
            glUniform3fv(glGetUniformLocation(self.shaderProgram, "material.specular"), 1, glm.value_ptr(specular))
        glUniform1f(glGetUniformLocation(self.shaderProgram, "material.shininess"), shininess)

        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "projection"), 1, GL_FALSE, glm.value_ptr(projection_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "model"), 1, GL_FALSE, glm.value_ptr(self.model_matrix));

        if self.diffuse_texture is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.diffuse_texture)
        if self.specular_texture is not None:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.specular_texture)

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


def load_texture(filename: str):
    texture = GLuint(0)
    glGenTextures(1, texture)
    image = Image.open(f'{IMAGES_DIR}/{filename}').transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    image_array = np.array(image, dtype=np.uint8)

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_array.data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture


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