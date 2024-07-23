import engine.model as model
import engine.vbo as vbo
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from main import engine_class

# parent scene
class base_scene:
    def __init__(self, game):
        self.game: engine_class = game
        self.objects: List[model.base_model] = []

    def add_object(self, object: model.base_model):
        self.objects.append(object)

    def load(self): ...

    def render(self):
        for object in self.objects:
            object.render()
        self.skybox.render()

    # get functions
    # texture
    def get_texture(self, texture_name: str, path: str):
        self.game.texture_class.get_texture(texture_name, path)
    def get_texture_cube(self, path: str, ext: str):
        self.game.texture_class.get_texture_cube(path, ext)
    # VBO
    def get_VBO(self, VBO_name: str, VBO: vbo.base_VBO):
        self.game.VAOs_class.VBOs_class.VBOs[VBO_name] = VBO
    # shader program
    def get_shader_program(self, shader_name: str):
        self.game.VAOs_class.programs.get_shader_program(shader_name)
    # VAO
    def get_VAO(self, VAO_name: str, program_name: str, VBO_name: str):
        self.game.VAOs_class.get_VAO(VAO_name, program_name, VBO_name)