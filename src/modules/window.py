import glfw
from OpenGL.GL import *
from modules.scene import Scene

class Window:
    def __init__(self, 
                 width: int = 1080, 
                 height: int = 720, 
                 fullscreen: bool = False,
                 rotation_mode: bool = False,
                 animation_mode: bool = False):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")
        
        self.monitor: glfw._GLFWmonitor = glfw.get_primary_monitor()
        self.vidmode: glfw._GLFWvidmode = glfw.get_video_mode(self.monitor)
        if fullscreen:
            self.window: glfw._GLFWwindow = glfw.create_window(self.vidmode.size.width,
                                                               self.vidmode.size.height,
                                                               "Main",
                                                               self.monitor,
                                                               None)
        else:
            self.window: glfw._GLFWwindow = glfw.create_window(width, height, "Main", None, None)
        self.fullscreen = fullscreen

        self.width = width
        self.height = height

        self.rotation_mode = rotation_mode
        self.animation_mode = animation_mode

        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        self.__set_callbacks()

        self.scene = Scene(aspect = self.width / self.height)

    def get_window(self) -> glfw._GLFWwindow:
        return self.window
    
    def get_scene(self) -> Scene:
        return self.scene

    def __set_callbacks(self):
        glfw.set_window_size_callback(self.window, self.__window_size_callback)
        glfw.set_key_callback(self.window, self.__key_callback)

    def __window_size_callback(self, window: glfw._GLFWwindow, width, height) -> None:
        self.scene.aspect = width / height
        glViewport(0, 0, width, height)

    def __key_callback(self, window: glfw._GLFWwindow, key, scancode, action, mods) -> None:
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(window, True)

        if glfw.PRESS == glfw.get_key(window, glfw.KEY_BACKSPACE):
            if self.fullscreen:
                glfw.set_window_monitor(window, None, 100, 100, self.width, self.height, self.vidmode.refresh_rate)
            else:
                glfw.set_window_monitor(window, self.monitor, 0, 0, self.vidmode.size.width, self.vidmode.size.height, self.vidmode.refresh_rate)

            self.fullscreen = not self.fullscreen

        if glfw.PRESS == glfw.get_key(window, glfw.KEY_R):
            self.rotation_mode = not self.rotation_mode

        if glfw.PRESS == glfw.get_key(window, glfw.KEY_SPACE):
            self.animation_mode = not self.animation_mode