from OpenGL.GL import *
from config import SOURCES_DIR
from PIL import Image

def load_cubemap(cubemapdir: str = "cubemap"):
    files = [
        "posx.jpg",
        "negx.jpg",
        "posy.jpg",
        "negy.jpg",
        "posz.jpg",
        "negz.jpg",
    ]
    texture = GLuint(0)
    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture)
    for i, file in enumerate(files):
        image = Image.open(f"{SOURCES_DIR}/cubemaps/{cubemapdir}/{file}")
        image = image.convert('RGB')
        image_data = image.tobytes()
        glTexImage2D(
            GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 
            0, 
            GL_RGB, 
            image.width, 
            image.height, 
            0, 
            GL_RGB, 
            GL_UNSIGNED_BYTE, 
            image_data
        )

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    return texture

def load_texture(filename: str):
    texture = GLuint(0)
    glGenTextures(1, texture)
    image = Image.open(f'{SOURCES_DIR}/textures/{filename}').transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    image_data = image.tobytes()

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
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