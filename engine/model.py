import moderngl
import glm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import engine_class

class base_model:
    def __init__(self, game, VAO_name: str, pos: tuple[int, int, int], rot: tuple[int, int, int] = (0, 0, 0), scale: tuple[int, int, int] = (1, 1, 1)):
        self.game: engine_class = game
        self.pos = glm.vec3(pos)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.VAO: moderngl.VertexArray = game.VAOs_class.VAOs[VAO_name]
        self.program: moderngl.Program = self.VAO.program

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.VAO.render()

class cube_model(base_model):
    def __init__(self, game, texture_name: str, pos: tuple[int, int, int], rot: tuple[int, int, int] = (0, 0, 0), scale: tuple[int, int, int] = (1, 1, 1)):
        super().__init__(game, "cube", pos, rot, scale)
        self.texture: moderngl.Texture = self.game.texture_class.textures[texture_name]
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program["m_view"].write(self.game.camera.m_view)
        self.program["cam_pos"].write(self.game.camera.position)
        self.program["m_model"].write(self.m_model)

    def on_init(self):
        # texture
        self.program["u_texture_0"] = 0
        self.texture.use()
        # matrix
        self.program["m_proj"].write(self.game.camera.m_proj)
        self.program["m_view"].write(self.game.camera.m_view)
        self.program["m_model"].write(self.m_model)
        # light
        self.program["light.position"].write(self.game.light.position)
        self.program["light.Ia"].write(self.game.light.Ia)
        self.program["light.Id"].write(self.game.light.Id)
        self.program["light.Is"].write(self.game.light.Is)

class skybox(base_model):
    def __init__(self, game):
        super().__init__(game, "skybox", (0, 0, 0), (0, 0, 0), (1, 1, 1))
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.game.camera.m_view))
        self.program["m_inv_proj_view"].write(glm.inverse(self.game.camera.m_proj * m_view))

    def on_init(self):
        self.texture = self.game.texture_class.textures["skybox"]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)