import glfw, glm
from OpenGL.GL import *

from modules.window import Window
from modules.figures import Square, Cube
from modules.model import Model, Skybox
from modules.structures import Material, TextureMaterial, DirLight, PointLight, SpotLight

winWidth: int = 1080
winHeight: int = 720


def main() -> None:
    windowContainer: Window = Window(winWidth, winHeight, fullscreen=False)
    window = windowContainer.get_window()

    scene = windowContainer.get_scene()

    # Light section
    dirlight = DirLight(
        ambient=glm.vec3(0.2, 0.2, 0.1),
        direction=glm.vec3(1, -1, 0.5)
    )
    scene.dirLights.extend([dirlight])

    pointlight = PointLight(
        position=glm.vec3(0.0, 0.0, 1.7)
    )
    scene.pointLights.extend([pointlight])

    spotlight1 = SpotLight(
        constant=1.0,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(-3, -1, 2),
        direction=glm.vec3(0, 0, -1),
        cutOff=40,
        outerCutOff=45
    )
    spotlight2 = SpotLight(
        constant=1.0,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(3, -1, 2),
        direction=glm.vec3(0, 0, -1),
        cutOff=40,
        outerCutOff=45
    )
    scene.spotLights.extend([
        spotlight1,
        spotlight2,
    ])

    # IMPORTANT: scene.update_shader_lights_count() 
    # is required if you change the number of lights
    scene.update_shader_lights_count()

    # Background
    skybox = Skybox()
    floor = Model.from_figure(
        Cube, 
        mode="m", 
        material="black_plastic",
        # geometryShader="gs_custom.glsl"
    )
    floor.translate(glm.vec3(0, -1.15, 0)).scale((1.3, 0.15, 1.3))

    # Models section
    capybara1_material = Material(
        "capybara",
        glm.vec3(0.44, 0.20, 0.17),
        glm.vec3(0.6, 0.24, 0.0),
        glm.vec3(0.81, 0.38, 0.19),
        0.04,
        0.0,
        0.03,
        0.0
    )
    capybara2_material = Material(
        "capybara",
        glm.vec3(0.44, 0.0, 0.0),
        glm.vec3(0.8, 0.21, 0.21),
        glm.vec3(1.0, 0.55, 0.55),
        0.04,
        0.0,
        0.03,
        0.0
    )
    capybara1 = Model.from_model("capybara.obj", material=capybara1_material)
    capybara1.translate(glm.vec3(-0.045, -1, 1.015)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(-90, 0, 90)
    ).scale(glm.vec3(0.1))
    capybara1_matrix = capybara1.model_matrix

    capybara2 = Model.from_model("capybara.obj", material=capybara2_material)
    capybara2.translate(glm.vec3(0.045, -1, 1.0)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(90, 180, 90)
    ).scale(glm.vec3(0.1))
    capybara2_matrix = capybara2.model_matrix

    eiffel_material = TextureMaterial(
        "eiffel_texture",
        "iron_texture.jpg",
        "iron_texture_specular.jpg",
        0.4,
    )
    eiffel = Model.from_model(
        "EiffelTower2.obj",
        mode="t",
        material=eiffel_material,
    )
    eiffel.translate(glm.vec3(0, -1, 0.0)).scale(glm.vec3(0.045))

    scene.objects.extend([
        skybox,
        floor,
        eiffel, 
        capybara1, 
        capybara2
    ])

    # for light in scene.pointLights + scene.spotLights:
    #     lamp = Model.from_figure(
    #         Cube, mode="light"
    #     )
    #     lamp.translate(light.position).scale(glm.vec3(0.01))
    #     scene.objects.append(lamp)

    animate_capybara1 = scene.animate_object(scene.objects.index(capybara1))(animate_capybara)
    animate_capybara2 = scene.animate_object(scene.objects.index(capybara2))(animate_capybara)

    # Window params
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_MULTISAMPLE)

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
            skybox=skybox
        )
        if windowContainer.animation_mode:
            animate_capybara1(initial_matrix=capybara1_matrix)
            animate_capybara2(initial_matrix=capybara2_matrix)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

def animate_capybara(capybara, *, time, delta_time, initial_matrix = glm.mat4(1.0)):
    capybara.model_matrix = initial_matrix

    r = 10
    v = 1.0

    x = glm.sin(time * -v)
    y = glm.cos(time * v)
    z = 0
    capybara.translate(glm.vec3(x, y, z) * r)
    capybara.rotate(glm.vec3(0, 0, -time) * 50)

    return capybara

if __name__ == "__main__":
    main()