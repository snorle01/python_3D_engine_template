import pygame, moderngl
from typing import Dict

class texture_class:
    def __init__(self, game):
        self.game = game
        self.ctx: moderngl.Context = game.ctx
        self.textures: Dict[str, moderngl.Texture] = {}

        """
        obselete cant find a way to get a dict to return a default value
        # make error texture
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 0))
        texture = self.ctx.texture(size=surface.get_size(), components=3, data=pygame.image.tostring(surface, "RGB"))
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        self.textures["ERROR"] = texture
        """

    # skybox texture
    """
    loads all skybox textures from a folder.
    images need to be split into 6 images.
    images needs to be named "right" "left" "top" "bottom", "front", "back".

    texture name needs to be "skybox" since its hard coded for skybox model to try and find a texture nemed skybox.
    """
    def get_texture_cube(self, dir_path: str, ext: str):
        faces = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]
        textures = []
        for face in faces:
            texture = pygame.image.load(dir_path + f"{face}.{ext}").convert()
            if face in ["right", "left", "front", "back"]:
                texture = pygame.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pygame.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        self.textures["skybox"] = texture_cube

    # default texture
    def get_texture(self, texture_name: str, path: str) -> moderngl.Texture:
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pygame.image.tostring(texture, "RGB"))
        # mipmaps
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        
        self.textures[texture_name] = texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]