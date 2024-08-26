import glm, ctypes, tinyobjloader
import numpy as np
from OpenGL.GL import *
from typing import Literal

from modules.figures import Primitive
from modules.materials import materials
from modules.structures import Material, TextureMaterial
from modules.funcs import load_shaders, load_cubemap
from config import SHADERS_DIR, MODELS_DIR, SOURCES_DIR

sizeof_float = ctypes.sizeof(ctypes.c_float)
void_p = ctypes.c_void_p

class Model:
    def __init__(self, 
                 vertices: np.ndarray,
                 vertex_indices: np.ndarray,
                 normals: np.ndarray = None,
                 texcoords: np.ndarray = None,
                 mode: str | Literal["light", "l", "materials", "m", "textures", "t", "custom"] = "materials",
                 material: str | Material | TextureMaterial = None,
                 vertexShader: str = None, 
                 fragmentShader: str = None,
                 geometryShader:str = None):
        self.vao = GLuint(0)
        self.vbo = GLuint(0)
        self.ebo = GLuint(0)

        glGenVertexArrays(1, self.vao)
        glGenBuffers(1, self.vbo)
        glGenBuffers(1, self.ebo)

        self.mode = mode
        self.material = None

        if self.mode in ["light", "l"]:
            vertexShader = "vs_light.glsl"
            fragmentShader = "fs_light.glsl"
        elif self.mode in ["textures", "t"]:
            if isinstance(material, TextureMaterial):
                self.material = material
            elif isinstance(material, str):
                try:
                    self.material = materials[material]
                except:
                    raise ValueError(f"{material} is not found\nPlease try other values")
            else:
                raise ValueError(f"material must be TextureMaterial or a string\nPlease try other values")
            vertexShader = "vs.glsl"
            fragmentShader = "fs_textures.glsl"
        elif self.mode in ["materials", "m"]:
            if isinstance(material, Material):
                self.material = material
            elif isinstance(material, str):
                try:
                    self.material = materials[material]
                except:
                    raise ValueError(f"{material} is not found\nPlease try other values")
            else:
                raise ValueError(f"material must be a Material or a string\nPlease try other values")
            vertexShader = "vs.glsl"
            fragmentShader = "fs.glsl"
        elif self.mode in ["custom"]:
            if isinstance(material, Material):
                self.material = material
            elif isinstance(material, str):
                try:
                    self.material = materials[material]
                except:
                    raise ValueError(f"{material} is not found\nPlease try other values")
            else:
                raise ValueError(f"material must be a Material or a string\nPlease try other values")
            vertexShader = vertexShader if vertexShader is not None else "vs.glsl"
            fragmentShader = fragmentShader if fragmentShader is not None else "fs.glsl"
        
        vertexShaderPath = f"{SHADERS_DIR}/{vertexShader}"
        fragmentShaderPath = f"{SHADERS_DIR}/{fragmentShader}"
        geometryShaderPath = f"{SHADERS_DIR}/{geometryShader}" if geometryShader is not None else None
        self.shaderProgram = load_shaders(
            vertexShaderPath, 
            fragmentShaderPath,
            geometryShaderPath
        )

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
    
    @classmethod
    def from_figure(cls,
                    figure: Primitive,
                    mode: str | Literal["light", "l", "materials", "m", "textures", "t"] = "materials",
                    material: str | Material | TextureMaterial = None,
                    vertexShader: str = None, 
                    fragmentShader: str = None,
                    geometryShader: str = None):
        vertices = figure.vertices
        indices = figure.indices if figure.indices is not None else np.arange(len(vertices), dtype="uint32")
        normals = figure.normals if figure.normals is not None else None
        texcoords = figure.texcoords if figure.texcoords is not None else None
        return cls(
            vertices,
            indices,
            normals,
            texcoords,
            mode = mode,
            material = material,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader,
            geometryShader = geometryShader
        )
    
    @classmethod
    def from_model(cls,
                   filename: str,
                   mode: str | Literal["light", "l", "materials", "m", "textures", "t"] = "materials",
                   material: str | Material | TextureMaterial = None,
                   vertexShader: str = None, 
                   fragmentShader: str = None,
                   geometryShader: str = None):
        reader = tinyobjloader.ObjReader()

        print(f"loading {filename}")

        if not reader.ParseFromFile(f"{MODELS_DIR}/{filename}"):
            print("Failed to load : ", filename)
            print("Warn:", reader.Warning())
            print("Err:", reader.Error())

        if reader.Warning():
            print("Warn:", reader.Warning())

        print(f"{filename} loaded succesfully")

        attrib = reader.GetAttrib()
        shapes = reader.GetShapes()
        materials = reader.GetMaterials()

        vertices = np.array(attrib.vertices, dtype = 'float32').reshape(-1, 3)
        normals = np.array(attrib.normals, dtype = 'float32').reshape(-1, 3)
        texcoords = np.array(attrib.texcoords, dtype = 'float32').reshape(-1, 2)

        vertex_indices = np.array([index.vertex_index for shape in shapes for index in shape.mesh.indices], dtype = 'uint32')
        return cls(
            vertices,
            vertex_indices,
            normals,
            texcoords,
            mode = mode,
            material = material,
            vertexShader = vertexShader, 
            fragmentShader = fragmentShader,
            geometryShader = geometryShader
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
               skybox = None,
               **kwargs: any):
        view_pos = view_position

        glUseProgram(self.shaderProgram)

        glUniform2fv(glGetUniformLocation(self.shaderProgram, "resolution"), 1, resolution)
        glUniform1f(glGetUniformLocation(self.shaderProgram, "time"), time)

        glUniform3fv(glGetUniformLocation(self.shaderProgram, "viewPos"), 1, glm.value_ptr(view_pos))

        if self.mode not in ["light", "l"]:
            if dir_lights is not None:
                for i, light in enumerate(dir_lights):
                    light.set_uniforms(self.shaderProgram, i)

            if point_lights is not None:
                for i, light in enumerate(point_lights):
                    light.set_uniforms(self.shaderProgram, i)

            if spot_lights is not None:
                for i, light in enumerate(spot_lights):
                    light.set_uniforms(self.shaderProgram, i)

        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "projection"), 1, GL_FALSE, glm.value_ptr(projection_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_matrix));
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "model"), 1, GL_FALSE, glm.value_ptr(self.model_matrix));

        if self.material is not None:
            self.material.set_uniforms(self.shaderProgram)

        glBindVertexArray(self.vao)
        if self.mode in ["custom"]:
            glBindTexture(GL_TEXTURE_CUBE_MAP, skybox.texture)
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

class Skybox:
    def __init__(self,
                 directory: str = "skybox",
                 vertexShader: str = "vs_skybox.glsl", 
                 fragmentShader: str = "fs_skybox.glsl"):
        self.vao = GLuint(0)
        self.vbo = GLuint(0)

        glGenVertexArrays(1, self.vao)
        glGenBuffers(1, self.vbo)

        self.shaderProgram = load_shaders(f"{SHADERS_DIR}/{vertexShader}", f"{SHADERS_DIR}/{fragmentShader}")
        self.texture = load_cubemap(f"{SOURCES_DIR}/cubemaps/{directory}")

        skyboxVertices = np.array([
            # positions
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,

            1.0, -1.0, -1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0, -1.0,
            1.0, -1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,

            -1.0,  1.0, -1.0,
            1.0,  1.0, -1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0
        ], dtype=np.float32)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, skyboxVertices.nbytes, skyboxVertices.data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof_float, void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def render(self,
               projection_matrix,
               view_matrix,
               **kwargs: any):
        glDepthMask(GL_FALSE)

        glUseProgram(self.shaderProgram)

        view_matrix = glm.mat4(glm.mat3(view_matrix))
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "projection"), 1, GL_FALSE, glm.value_ptr(projection_matrix))
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_matrix))

        glBindVertexArray(self.vao)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glDepthMask(GL_TRUE)