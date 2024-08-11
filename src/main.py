import glfw, glm
from OpenGL.GL import *

from modules.window import Window
from modules.figures import Square, Cube
from modules.models import Model
from modules.materials import materials

winWidth: int = 1080
winHeight: int = 720

def main() -> None:
    windowContainer: Window = Window(winWidth, winHeight)
    window = windowContainer.get_window()
    scene = windowContainer.get_scene()

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    capybara = Model("capybara.obj", fragmentShader="fs_test.glsl", material = materials.get("white_plastic"))
    capybara.scale(glm.vec3(0.1)).rotate(glm.vec3(-90, 0, 90))

    scene.objects.extend([capybara])

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