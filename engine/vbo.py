import numpy, moderngl
from typing import Dict, List

class VBOs_class:
    def __init__(self, ctx:moderngl.Context):
        self.VBOs: Dict[str, base_VBO] = {}

    def destroy(self):
        [VBO.destroy() for VBO in self.VBOs.values()]

# parent class holds most of the functions needed
class base_VBO:
    def __init__(self, ctx:moderngl.Context):
        self.ctx = ctx
        self.VBO = self.get_VBO()
        self.format: str = None
        self.attribs: List[str] = None

    def get_vertex_data(self): ...

    @staticmethod
    def get_data(vertices: List[tuple[int, int, int]], indices: List[tuple[int, int, int]]):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype="f4")

    def get_VBO(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.VBO.release()

class cube_VBO(base_VBO):
    def __init__(self, ctx: moderngl.Context):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # verticies 
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        
        # gets position from vertices variable
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_data(vertices, indices)

        # uv maping
        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        # normal
        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = numpy.array(normals, dtype="f4").reshape(36, 3)

        vertex_data = numpy.hstack([normals, vertex_data])
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])
        return vertex_data
    
class skybox_VBO(base_VBO):
    def __init__(self, ctx: moderngl.Context):
        super().__init__(ctx)
        self.format = "3f"
        self.attribs = ["in_position"]

    def get_vertex_data(self):
        z = 0.9999
        vertices = [(-1, -1, z), (1, 1, z), (-1, 1, z),
                    (-1, -1, z), (1, -1, z), (1, 1, z)]
        vertex_data = numpy.array(vertices, dtype="f4")
        return vertex_data