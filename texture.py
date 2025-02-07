import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path="textures/img.jpg")
        self.textures[1] = self.get_texture(path="textures/img_1.jpg")
        self.textures[2] = self.get_texture(path="textures/img_2.jpg")
        self.textures["cat"] = self.get_texture(path="objects/cat/fence.png")
        self.textures["skybox"] = self.get_texture_cube(
            dir_path="textures/skybox1/", ext="png"
        )
        self.textures["depth_texture"] = self.get_depth_texture()
        self.textures["bola"] = self.get_texture(path="objects\sphere\darkMarble.jpg")
        self.textures["apple"] = self.get_texture(
            path="newobjects\Shading&Texture\Texture\Apple_Sphere.png"
        )
        self.textures["cone"] = self.get_texture(path="textures/cone2.png")
        self.textures["fenceRight"] = self.get_texture(path="objects/cat/fence.png")
        self.textures["fenceback"] = self.get_texture(path="objects/cat/fence.png")
        self.textures["fencefront"] = self.get_texture(path="objects/cat/fence.png")
        self.textures["papan"] = self.get_texture(path="textures/team.png")
        self.textures["table"] = self.get_texture(path="textures/wood_meja2.png")
        self.textures["cylinder"] = self.get_texture(path="textures/metal.jpg")
        self.textures["darkwall"] = self.get_texture(path="textures/bricks.jpg")
        self.textures["mug"] = self.get_texture(path="textures/img_2.jpg")

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext="png"):
        faces = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f"{face}.{ext}").convert()
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB"),
        )
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
