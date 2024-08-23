import glfw, glm
from OpenGL.GL import *

from modules.window import Window
from modules.figures import Square, Cube
from modules.model import Model
from modules.materials import materials
from modules.structures import Material, DirLight, PointLight, SpotLight

winWidth: int = 1080
winHeight: int = 720


def main() -> None:
    windowContainer: Window = Window(winWidth, winHeight, fullscreen=False)
    window = windowContainer.get_window()

    scene = windowContainer.get_scene()

    # Light section
    dirlight = DirLight(
        direction=glm.vec3(-1)
    )
    scene.dirLights.extend([dirlight])

    pointlight = PointLight(
        position=glm.vec3(0.7, 0.9, 3.5)
    )
    scene.pointLights.extend([pointlight])

    spotlight = SpotLight(
        position=glm.vec3(0, -1, 2),
        direction=glm.vec3(0, 0, -10)
    )
    spotlight2 = SpotLight(
        constant=0.4,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(-5, -1, -12),
        direction=glm.vec3(0, 5, -20),
        cutOff=70,
        outerCutOff=75
    )
    spotlight3 = SpotLight(
        constant=0.4,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(5, -1, -12),
        direction=glm.vec3(0, 5, -20),
        cutOff=70,
        outerCutOff=75
    )
    scene.spotLights.extend(
        [
            spotlight,
            spotlight2,
            spotlight3
        ]
    )

    # IMPORTANT: scene.update_shader_lights_count() 
    # is required if you change the number of lights
    scene.update_shader_lights_count()

    # Background

    # Models section
    capybara_material = Material(
        "capybara",
        glm.vec3(0.18, 0.07, 0.01),
        glm.vec3(0.8, 0.32, 0),
        glm.vec3(1, 0.9, 0.9),
        50.0,
    )
    capybara1 = Model.from_model("capybara.obj", material=capybara_material)
    capybara1.translate(glm.vec3(-0.045, -1, 1.95)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(-90, 0, 90)
    ).scale(glm.vec3(0.1))
    capybara2 = Model.from_model("capybara.obj", material=materials.get("ruby"))
    capybara2.translate(glm.vec3(0.045, -1, 1.95)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(90, 180, 90)
    ).scale(glm.vec3(0.1))

    eiffel_material = Material(
        "eiffel",
        glm.vec3(0.16, 0.05, 0.0),
        glm.vec3(0.35, 0.1, 0.0),
        glm.vec3(0.71, 0.24, 0.16),
        32.0,
    )
    eiffel = Model.from_model(
        "EiffelTower.obj",
        material=materials.get("bronze"),
        diffuse_texture="rusted_metal.jpg",
        specular_texture="rusted_metal.jpg",
        fragmentShader="fs_textures.glsl",
    )
    eiffel.translate(glm.vec3(0, -1, -20.0)).scale(glm.vec3(0.2, 0.25, 0.2))

    scene.objects.extend([eiffel, capybara1, capybara2])

    for light in scene.pointLights + scene.spotLights:
        lamp = Model.from_figure(
            Cube, vertexShader="vs_light.glsl", fragmentShader="fs_light.glsl"
        )
        lamp.translate(light.position).scale(glm.vec3(0.01))
        scene.objects.append(lamp)

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

        scene.render(
            resolution=resolution,
            time=time,
            animation_mode=windowContainer.animation_mode,
        )

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
