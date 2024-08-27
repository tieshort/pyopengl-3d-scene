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
        direction=glm.vec3(-1, -1, 0)
    )
    scene.dirLights.extend([dirlight])

    pointlight = PointLight(
        position=glm.vec3(0.0, 0.9, 1.5)
    )
    scene.pointLights.extend([pointlight])

    spotlight1 = SpotLight(
        constant=1.0,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(-3, -1, 2),
        direction=glm.vec3(0, 3, 0),
        cutOff=70,
        outerCutOff=75
    )
    spotlight2 = SpotLight(
        constant=1.0,
        linear=0.005,
        quadratic=0.000025,
        position=glm.vec3(3, -1, 2),
        direction=glm.vec3(0, 3, 0),
        cutOff=70,
        outerCutOff=75
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
        glm.vec3(0.27, 0.15, 0.08),
        glm.vec3(0.64, 0.24, 0.0),
        glm.vec3(0.91, 0.58, 0.39),
        0.04,
        0.0,
        0.03,
        0.0
    )
    capybara2_material = Material(
        "capybara",
        glm.vec3(0.27, 0.08, 0.08),
        glm.vec3(1.0, 0.31, 0.31),
        glm.vec3(1.0, 0.655, 0.655),
        0.04,
        0.0,
        0.03,
        0.0
    )
    capybara1 = Model.from_model("capybara.obj", material=capybara1_material)
    capybara1.translate(glm.vec3(-0.045, -1, 1.015)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(-90, 0, 90)
    ).scale(glm.vec3(0.1))
    capybara2 = Model.from_model("capybara.obj", material=capybara2_material)
    capybara2.translate(glm.vec3(0.045, -1, 1.0)).scale(glm.vec3(0.1)).rotate(
        glm.vec3(90, 180, 90)
    ).scale(glm.vec3(0.1))

    eiffel_material = TextureMaterial(
        "eiffel_texture",
        "gold_texture.jpg",
        "gold_texture.jpg",
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

    for light in scene.pointLights + scene.spotLights:
        lamp = Model.from_figure(
            Cube, mode="light"
        )
        lamp.translate(light.position).scale(glm.vec3(0.01))
        scene.objects.append(lamp)

    animate_capybara1 = scene.animate_object(scene.objects.index(capybara1))(animate_capybara)
    animate_capybara2 = scene.animate_object(scene.objects.index(capybara2))(animate_capybara)

    # Window params
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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
            skybox = skybox
        )
        if windowContainer.animation_mode:
            animate_capybara1(time=time)
            animate_capybara2(time=time)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

def animate_capybara(capybara, *, time, delta_time):
    animation_time = 5.0
    time = time % animation_time
    progress = time / animation_time * 100
    speed = 0.5 * delta_time
    if progress <= 40:
        capybara.rotate(glm.vec3(0, 0, 330) * speed)
    elif progress > 60:
        capybara.rotate(glm.vec3(0, 0, 360) * -speed)
    capybara.translate(glm.clamp(glm.vec3(glm.sin(time), glm.cos(time), 0), 0.0, 0.2))

    return capybara

if __name__ == "__main__":
    main()