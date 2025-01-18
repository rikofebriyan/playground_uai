from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # floor
        n, s = 40, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        # columns
        # left column
        for i in range(5):
            add(Cube(app, pos=(18, i * s, 6), tex_id=2))

        # right column
        for i in range(5):
            add(Cube(app, pos=(18, i * s, -6), tex_id=2))

        # top bar
        for i in range(-6, 5, s):
            add(Cube(app, pos=(18, 4 * s, i), tex_id=2))

        for i in range(9):
            add(Cat(app, pos=(-21 + (i * 4.5), -1, 20)))
        for i in range(9):
            add(FenceRight(app, pos=(-17 + (i * 4.5), -1, -20)))
        for i in range(9):
            add(FenceBack(app, pos=(-21, -1, -20 + (i * 4.5))))
        for i in range(3):
            add(FenceFront(app, pos=(19, -1, -16 + (i * 4.5))))
        for i in range(3):
            add(FenceFront(app, pos=(19, -1, 11.5 + (i * 4.5))))
        # cat
        # add(Cat(app, pos=(0, -1, -20)))

        add(Bola(app, pos=(-10, -6, -10)))

        # moving cube
        self.moving_cube_1 = MovingCube(app, pos=(0, 6, 8), scale=(3, 3, 3), tex_id=1)
        add(self.moving_cube_1)

        # self.moving_cube_2 = MovingCube(app, pos=(0, 6, -10), scale=(3, 3, 3), tex_id=1)
        # add(self.moving_cube_2)

    def update(self):
        self.moving_cube_1.rot.xyz = self.app.time
        # self.moving_cube_2.rot.xyz = self.app.time
