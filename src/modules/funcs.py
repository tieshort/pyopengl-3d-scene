from OpenGL.GL import *
from PIL import Image

def load_cubemap(cubeMapDir: str = "cubemap"):
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
        image = Image.open(f"{cubeMapDir}/{file}")
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

def load_texture(filePath: str):
    texture = GLuint(0)
    glGenTextures(1, texture)
    image = Image.open(f'{filePath}').transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    image_data = image.tobytes()

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture


def load_shaders(
        vertexShaderPath: str, 
        fragmentShaderPath: str,
        geometryShaderPath: str = None):
    vertexShaderId: int = glCreateShader(GL_VERTEX_SHADER)
    fragmentShaderId: int = glCreateShader(GL_FRAGMENT_SHADER)
    geometryShaderId: int = glCreateShader(GL_GEOMETRY_SHADER) if geometryShaderPath is not None else None

    with open(vertexShaderPath, 'r') as f:
        vertexShader = f.read()

    with open(fragmentShaderPath, 'r') as f:
        fragmentShader = f.read()

    if geometryShaderPath is not None:
        with open(geometryShaderPath, 'r') as f:
            geometryShader = f.read()

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

    if geometryShaderPath is not None:
        try:
            print("Compiling shader: ", geometryShaderPath)
            glShaderSource(geometryShaderId, geometryShader)
            glCompileShader(geometryShaderId)
        except Exception as e:
            print("Error compiling geometry shader: ", e)

    try:
        print("Linking Program")
        shaderProgram: int = glCreateProgram()
        glAttachShader(shaderProgram, vertexShaderId)
        if geometryShaderPath is not None:
            glAttachShader(shaderProgram, geometryShaderId)
        glAttachShader(shaderProgram, fragmentShaderId)
        glLinkProgram(shaderProgram)
    except Exception as e:
        print("Error linking program: ", e)

    glDeleteShader(vertexShaderId)
    glDeleteShader(fragmentShaderId)

    return shaderProgram