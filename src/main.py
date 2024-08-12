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
    windowContainer: Window = Window(winWidth, winHeight, fullscreen = True)
    window = windowContainer.get_window()

    scene = windowContainer.get_scene()

    lamp = Figure(Cube, vertexShader = "vs_light.glsl", fragmentShader = "fs_light.glsl")
    scene.set_light(lamp, Light(color = glm.vec3(1, 1, 0.7), 
                                position = glm.vec3(0.9, 0.9, 0.3), 
                                view_position = glm.vec3(0)))
    lamp.scale(glm.vec3(0.05))

    capybara_material = Material("capybara", glm.vec3(0.3, 0.07, 0.01), glm.vec3(0.9, 0.22, 0), glm.vec3(1, 0.9, 0.9), 50.0)

    capybara = Model("capybara.obj", material = capybara_material)
    capybara.scale(glm.vec3(0.1)).rotate(glm.vec3(-90, 0, 90))

    scene.objects.extend([capybara])

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        scene.render(resolution = glfw.get_window_size(window),
                    time = glfw.get_time(),
                    animation_mode = windowContainer.animation_mode)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()