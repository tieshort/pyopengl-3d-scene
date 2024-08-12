import glfw, glm
from OpenGL.GL import *

from modules.window import Window
from modules.figures import Square, Cube
from modules.models import Model, Figure
from modules.materials import Material, materials
from modules.light import Light

winWidth: int = 1080
winHeight: int = 720

def main() -> None:
    windowContainer: Window = Window(winWidth, winHeight, fullscreen = False)
    window = windowContainer.get_window()

    scene = windowContainer.get_scene()

    # Light section
    lamp = Figure(Cube, vertexShader = "vs_light.glsl", fragmentShader = "fs_light.glsl")
    scene.set_light(lamp, Light(color = glm.vec3(1), 
                                position = glm.vec3(0.9, 0.9, -0.7), 
                                view_position = glm.vec3(0)))
    lamp.scale(glm.vec3(0.03))

    # Models section
    capybara_material = Material("capybara", glm.vec3(0.2, 0.07, 0.01), glm.vec3(0.9, 0.22, 0), glm.vec3(1, 0.9, 0.9), 50.0)
    capybara1 = Model("capybara.obj", material = capybara_material)
    capybara1.translate(glm.vec3(-0.045, -1.1, 0.9)).scale(glm.vec3(0.01)).rotate(glm.vec3(-90, 0, 90))
    capybara2 = Model("capybara.obj", material = materials.get("ruby"))
    capybara2.translate(glm.vec3(0.045, -1.1, 0.9)).scale(glm.vec3(0.01)).rotate(glm.vec3(90, 180, 90))

    eiffel_material = Material("eiffel", glm.vec3(0.16, 0.05, 0.0), glm.vec3(0.35, 0.1, 0.0), glm.vec3(0.71, 0.24, 0.16), 32.0)
    eiffel = Model("EiffelTower.obj", material = materials.get("bronze"))
    eiffel.translate(glm.vec3(0, -1, -0.3)).scale(glm.vec3(0.02))

    scene.objects.extend([eiffel, capybara1, capybara2])

    # Window params
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    # glClearColor(1, 1, 1, 1)
    
    # Main event loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        scene.render(resolution = glfw.get_window_size(window),
                    time = glfw.get_time(),
                    animation_mode = windowContainer.animation_mode)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()