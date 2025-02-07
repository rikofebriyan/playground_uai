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
        n, s = 50, 2
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
        for i in range(3):
            for j in range(3):
                add(Apple(app, pos=(-0.7 + i, -0.85, 6.5 + j)))

        add(Bola(app, pos=(-1, -1.5, -8)))
        # add(Apple(app, pos=(0, -0.85, 7)))
        add(Cone(app, pos=(-5, -0.3, -7)))
        add(Papan(app, pos=(19.2, 8, 0)))

        for i in range(2):
            for j in range(3):
                add(Table(app, pos=(5 + (j * -7), -1, 10 + (i * -19))))

        add(Cylinder(app, pos=(-11, -0.3, -7)))
        add(Darkwall(app, pos=(-7, 0.1, 12)))
        add(Mug(app, pos=(-2, 0, 10)))

        # moving cube
        self.moving_cube_1 = MovingCube(app, pos=(19, 14, 0), scale=(2, 2, 2), tex_id=1)
        add(self.moving_cube_1)

        self.moving_cube_2 = MovingCube(
            app, pos=(19, 5, 12), scale=(1.5, 1.5, 1.5), tex_id=1
        )
        add(self.moving_cube_2)

        self.moving_cube_3 = MovingCube(
            app, pos=(19, 5, -12), scale=(1.5, 1.5, 1.5), tex_id=1
        )
        add(self.moving_cube_3)

        # self.moving_cube_2 = MovingCube(app, pos=(0, 6, -10), scale=(3, 3, 3), tex_id=1)
        # add(self.moving_cube_2)

    def update(self):
        self.moving_cube_1.rot.xyz = self.app.time
        self.moving_cube_2.rot.xyz = self.app.time
        self.moving_cube_3.rot.xyz = self.app.time
        # self.moving_cube_2.rot.xyz = self.app.time
