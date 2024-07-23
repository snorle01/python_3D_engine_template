import pygame, moderngl, sys
import engine.scene as scene
from engine.vao import VAOs_class
from engine.camera import camera_class
from engine.texture import texture_class
from engine.light import light_class

class engine_class:
    def __init__(self, window_size:tuple[int, int], start_scene: scene.base_scene):
        pygame.init()
        # initilize variables
        self.window_size = window_size
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.camera = camera_class(self, (0, 0, 4))
        # set atribute of openGL
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(self.window_size, flags=pygame.OPENGL | pygame.DOUBLEBUF)

        # change mouse settings
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # classes
        self.light = light_class((50, 50, -50))
        self.texture_class = texture_class(self)
        self.VAOs_class = VAOs_class(self.ctx)
        self.scene = start_scene(self)

    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    def destroy(self):
        self.VAOs_class.destroy()
        self.texture_class.destroy()