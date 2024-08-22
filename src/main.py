import glfw, glm
from OpenGL.GL import *

from modules.window import Window
from modules.figures import Square, Cube
from modules.models import Model, Figure
from modules.materials import materials
from modules.structures import Material, DirLight, PointLight, SpotLight

winWidth: int = 1080
winHeight: int = 720

def main() -> None:
    windowContainer: Window = Window(winWidth, winHeight, fullscreen = False)
    window = windowContainer.get_window()

    scene = windowContainer.get_scene()

    # Light section 
    # IMPORTANT: CHANGING LIGHTS COUNT NEEDS CHANGING
    # THE NUMBER OF LIGHT SOURCES IN FRAGMENT SHADER 

    dirlight = DirLight(direction = glm.vec3(-1), 
                        ambient = glm.vec3(0.2),
                        diffuse = glm.vec3(0.3),
                        specular = glm.vec3(0.4))
    scene.dirLights.extend([dirlight])

    pointlight = PointLight(position = glm.vec3(0.7, 0.9, 3.5),
                            ambient = glm.vec3(0.5),
                            diffuse = glm.vec3(0.8),
                            specular = glm.vec3(0.8),
                            constant = 1,
                            linear = 0.05,
                            quadratic = 0.003)
    scene.pointLights.extend([pointlight])

    spotlight = SpotLight(position = glm.vec3(0, -1, 2),
                          direction = glm.vec3(0, 0, -10),
                          ambient = glm.vec3(0.2),
                          diffuse = glm.vec3(0.8),
                          specular = glm.vec3(1),
                          constant = 1,
                          linear = 0.02,
                          quadratic = 0.001,
                          cutOff = 30.0,
                          outerCutOff = 40.0)
    scene.spotLights.extend([spotlight])

    # Background


    # Models section
    capybara_material = Material("capybara", glm.vec3(0.18, 0.07, 0.01), glm.vec3(0.8, 0.32, 0), glm.vec3(1, 0.9, 0.9), 50.0)
    capybara1 = Model("capybara.obj", material = capybara_material)
    capybara1\
        .translate(glm.vec3(-0.045, -1, 1.95))\
        .scale(glm.vec3(0.1))\
        .rotate(glm.vec3(-90, 0, 90))\
        .scale(glm.vec3(0.1))
    capybara2 = Model("capybara.obj", material = materials.get("ruby"))
    capybara2\
        .translate(glm.vec3(0.045, -1, 1.95))\
        .scale(glm.vec3(0.1))\
        .rotate(glm.vec3(90, 180, 90))\
        .scale(glm.vec3(0.1))

    eiffel_material = Material("eiffel", glm.vec3(0.16, 0.05, 0.0), glm.vec3(0.35, 0.1, 0.0), glm.vec3(0.71, 0.24, 0.16), 32.0)
    eiffel = Model("EiffelTower.obj", material = materials.get("bronze"))
    eiffel.translate(glm.vec3(0, -1, -30.0)).scale(glm.vec3(0.2, 0.25, 0.2))

    scene.objects.extend([eiffel, capybara1, capybara2])

    # Window params
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_POINT_SMOOTH)
    glPointSize(1.0)

    glEnable(GL_LINE_SMOOTH)
    glLineWidth(1.0)

    # glPolygonMode(GL_FRONT, GL_FILL)
    # glClearColor(1, 1, 1, 1)
    
    # Main event loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        time = glfw.get_time()
        resolution = glfw.get_window_size(window)

        scene.render(resolution = resolution,
                    time = time,
                    animation_mode = windowContainer.animation_mode)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()