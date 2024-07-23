import glm

class light_class:
    def __init__(self, position: tuple[int, int, int], color: tuple[int, int, int] = (1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # ambient light
        self.Ia = 0.1 * self.color
        # difuse lighting
        self.Id = 0.8 * self.color
        # specular lighting
        self.Is = 1.0 * self.color