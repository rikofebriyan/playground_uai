import numpy as np
import moderngl as mgl
import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos["cube"] = CubeVBO(ctx)
        self.vbos["cat"] = CatVBO(ctx)
        self.vbos["skybox"] = SkyBoxVBO(ctx)
        self.vbos["advanced_skybox"] = AdvancedSkyBoxVBO(ctx)
        self.vbos["bola"] = BolaVBO(ctx)
        self.vbos["fenceRight"] = FenceRightVBO(ctx)
        self.vbos["fenceback"] = FenceBackVBO(ctx)
        self.vbos["fencefront"] = FenceFrontVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]

        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6,
        ]
        normals = np.array(normals, dtype="f4").reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data


class CatVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/cat/fence.obj",
            cache=True,
            parse=True,
            collect_faces=True,  # Ensure face data is collected
            create_materials=True,  # Automatically create default materials
        )

        # Extract geometry data from the first material
        obj = list(objs.materials.values())[0]
        vertex_data = obj.vertices  # Access vertex data
        vertex_data = np.array(vertex_data, dtype="f4")  # Convert to NumPy array
        return vertex_data

    # def get_vertex_data(self):
    #     # objs = pywavefront.Wavefront('objects/cat/20430_Cat_v1_NEW.obj', cache=True, parse=True)
    #     objs = pywavefront.Wavefront("objects/cat/fence.obj", cache=True, parse=True)
    #     obj = objs.materials.popitem()[1]
    #     vertex_data = obj.vertices
    #     vertex_data = np.array(vertex_data, dtype="f4")
    #     return vertex_data


class SkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "3f"
        self.attribs = ["in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]

        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order="C")
        return vertex_data


class AdvancedSkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "3f"
        self.attribs = ["in_position"]

    def get_vertex_data(self):
        # in clip space
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype="f4")
        return vertex_data


class BolaVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/sphere/sphere.obj",
            cache=True,
            parse=True,
            collect_faces=True,  # Ensure face data is collected
            create_materials=True,  # Automatically create default materials
        )

        # Extract geometry data from the first material
        obj = list(objs.materials.values())[0]
        vertex_data = obj.vertices  # Access vertex data
        vertex_data = np.array(vertex_data, dtype="f4")  # Convert to NumPy array
        return vertex_data


class FenceRightVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/cat/fence.obj",
            cache=True,
            parse=True,
            collect_faces=True,  # Ensure face data is collected
            create_materials=True,  # Automatically create default materials
        )

        # Extract geometry data from the first material
        obj = list(objs.materials.values())[0]
        vertex_data = obj.vertices  # Access vertex data
        vertex_data = np.array(vertex_data, dtype="f4")  # Convert to NumPy array
        return vertex_data


class FenceBackVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/cat/fence.obj",
            cache=True,
            parse=True,
            collect_faces=True,  # Ensure face data is collected
            create_materials=True,  # Automatically create default materials
        )

        # Extract geometry data from the first material
        obj = list(objs.materials.values())[0]
        vertex_data = obj.vertices  # Access vertex data
        vertex_data = np.array(vertex_data, dtype="f4")  # Convert to NumPy array
        return vertex_data


class FenceFrontVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/cat/fence.obj",
            cache=True,
            parse=True,
            collect_faces=True,  # Ensure face data is collected
            create_materials=True,  # Automatically create default materials
        )

        # Extract geometry data from the first material
        obj = list(objs.materials.values())[0]
        vertex_data = obj.vertices  # Access vertex data
        vertex_data = np.array(vertex_data, dtype="f4")  # Convert to NumPy array
        return vertex_data
