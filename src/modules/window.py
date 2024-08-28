import glfw, glm
from OpenGL.GL import *
from modules.scene import Scene


class Window:
    def __init__(
        self,
        width: int = 1080,
        height: int = 720,
        fullscreen: bool = False,
        rotation_mode: bool = False,
        animation_mode: bool = False,
    ):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        self.monitor: glfw._GLFWmonitor = glfw.get_primary_monitor()
        self.vidmode: glfw._GLFWvidmode = glfw.get_video_mode(self.monitor)
        if fullscreen:
            self.width, self.height = self.vidmode.size.width, self.vidmode.size.height
            self.window: glfw._GLFWwindow = glfw.create_window(
                self.width, self.height, "Main", self.monitor, None
            )
        else:
            self.width, self.height = width, height
            self.window: glfw._GLFWwindow = glfw.create_window(
                self.width, self.height, "Main", None, None
            )
        self.fullscreen: bool = fullscreen

        self.rotation_mode: bool = rotation_mode
        self.animation_mode: bool = animation_mode

        self.x_last = self.width // 2
        self.y_last = self.height // 2

        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.keys: list[bool] = [False] * 1024
        self.__set_callbacks()

        self.scene = Scene(aspect=self.width / self.height)

    def get_window(self) -> glfw._GLFWwindow:
        return self.window

    def get_scene(self) -> Scene:
        return self.scene

    def __set_callbacks(self) -> None:
        glfw.set_window_size_callback(self.window, self.__window_size_callback)
        glfw.set_key_callback(self.window, self.__key_callback)
        glfw.set_cursor_pos_callback(self.window, self.__mouse_callback)
        glfw.set_scroll_callback(self.window, self.__scroll_callback)

    def __window_size_callback(self, window: glfw._GLFWwindow, width, height) -> None:
        self.scene.aspect = width / height
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)

    def __key_callback(
        self, window: glfw._GLFWwindow, key, scancode, action, mods
    ) -> None:
        if action == glfw.PRESS and not self.keys[key]:
            self.keys[key] = True
        elif action == glfw.RELEASE and self.keys[key]:
            self.keys[key] = False

        camera_speed = self.scene.camera.speed * self.scene.delta_time

        if self.keys[glfw.KEY_ESCAPE]:
            glfw.set_window_should_close(window, True)

        if self.keys[glfw.KEY_BACKSPACE]:
            if self.fullscreen:
                glfw.set_window_monitor(
                    window,
                    None,
                    100,
                    100,
                    self.width,
                    self.height,
                    self.vidmode.refresh_rate,
                )
            else:
                glfw.set_window_monitor(
                    window,
                    self.monitor,
                    0,
                    0,
                    self.vidmode.size.width,
                    self.vidmode.size.height,
                    self.vidmode.refresh_rate,
                )
            self.fullscreen = not self.fullscreen

        if self.keys[glfw.KEY_R]:
            glfw.set_cursor_pos(self.window, self.x_last, self.y_last)
            self.rotation_mode = not self.rotation_mode

        if self.keys[glfw.KEY_SPACE]:
            self.animation_mode = not self.animation_mode

        if self.keys[glfw.KEY_W]:
            self.scene.camera.position += camera_speed * self.scene.camera.target

        if self.keys[glfw.KEY_S]:
            self.scene.camera.position -= camera_speed * self.scene.camera.target

        if self.keys[glfw.KEY_A]:
            self.scene.camera.position -= (
                glm.normalize(glm.cross(self.scene.camera.target, self.scene.camera.up))
                * camera_speed
            )

        if self.keys[glfw.KEY_D]:
            self.scene.camera.position += (
                glm.normalize(glm.cross(self.scene.camera.target, self.scene.camera.up))
                * camera_speed
            )

    def __mouse_callback(
        self, window: glfw._GLFWwindow, xpos: float, ypos: float
    ) -> None:
        front = glm.vec3(0)
        if self.rotation_mode:
            xoffset = xpos - self.x_last
            yoffset = self.y_last - ypos
            self.x_last = xpos
            self.y_last = ypos

            xoffset *= self.scene.camera.sensitivity
            yoffset *= self.scene.camera.sensitivity

            self.scene.camera.yaw += xoffset
            self.scene.camera.pitch += yoffset

            if self.scene.camera.pitch > 89.0:
                self.scene.camera.pitch = 89.0
            if self.scene.camera.pitch < -89.0:
                self.scene.camera.pitch = -89.0

        front.x = glm.cos(glm.radians(self.scene.camera.yaw)) * glm.cos(
            glm.radians(self.scene.camera.pitch)
        )
        front.y = glm.sin(glm.radians(self.scene.camera.pitch))
        front.z = glm.sin(glm.radians(self.scene.camera.yaw)) * glm.cos(
            glm.radians(self.scene.camera.pitch)
        )

        self.scene.camera.target = glm.normalize(front)

    def __scroll_callback(
        self, window: glfw._GLFWwindow, xoffset: float, yoffset: float
    ) -> None:
        if self.scene.fov >= 1.0 and self.scene.fov <= 90.0:
            self.scene.fov -= yoffset
        self.scene.fov = (
            1.0
            if self.scene.fov < 1.0
            else 90.0 if self.scene.fov > 90.0 else self.scene.fov
        )
