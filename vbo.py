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
        self.vbos["apple"] = AppleVBO(ctx)
        self.vbos["cone"] = ConeVBO(ctx)
        self.vbos["fenceRight"] = FenceRightVBO(ctx)
        self.vbos["fenceback"] = FenceBackVBO(ctx)
        self.vbos["fencefront"] = FenceFrontVBO(ctx)
        self.vbos["papan"] = ThinRectangleVBO(ctx)
        self.vbos["table"] = TableVBO(ctx)
        self.vbos["cylinder"] = CylinderVBO(ctx)
        self.vbos["darkwall"] = DarkwallVBO(ctx)
        self.vbos["mug"] = MugVBO(ctx)

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


class AppleVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "newobjects/Models/apple.obj",
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


class ConeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "newobjects/Models/cone.obj",
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


class ThinRectangleVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        # Definisi vertex untuk balok tipis dengan permukaan lebar
        vertices = [
            (-2, -0.05, 1),  # 0
            (2, -0.05, 1),  # 1
            (2, 0.05, 1),  # 2
            (-2, 0.05, 1),  # 3
            (-2, 0.05, -1),  # 4
            (-2, -0.05, -1),  # 5
            (2, -0.05, -1),  # 6
            (2, 0.05, -1),  # 7
        ]

        indices = [
            (0, 2, 3),
            (0, 1, 2),  # Depan
            (1, 7, 2),
            (1, 6, 7),  # Samping kanan
            (6, 5, 4),
            (4, 7, 6),  # Belakang
            (3, 4, 5),
            (3, 5, 0),  # Samping kiri
            (3, 7, 4),
            (3, 2, 7),  # Atas
            (0, 6, 1),
            (0, 5, 6),  # Bawah
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
            (0, 0, 1) * 6,  # Depan
            (1, 0, 0) * 6,  # Kanan
            (0, 0, -1) * 6,  # Belakang
            (-1, 0, 0) * 6,  # Kiri
            (0, 1, 0) * 6,  # Atas
            (0, -1, 0) * 6,  # Bawah
        ]
        normals = np.array(normals, dtype="f4").reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data


class TableVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        # Fungsi pembantu untuk membuat box (balok) dengan 6 sisi.
        # Setiap sisi terdiri dari 2 segitiga (6 vertex) dengan:
        # (texcoord, normal, posisi)
        def create_box(x_min, x_max, y_min, y_max, z_min, z_max):
            # Titik sudut
            p000 = (x_min, y_min, z_min)
            p001 = (x_min, y_min, z_max)
            p010 = (x_min, y_max, z_min)
            p011 = (x_min, y_max, z_max)
            p100 = (x_max, y_min, z_min)
            p101 = (x_max, y_min, z_max)
            p110 = (x_max, y_max, z_min)
            p111 = (x_max, y_max, z_max)

            vertices = []

            # Front face (sisi depan, z = z_max), normal (0, 0, 1)
            vertices += [
                ((0, 0), (0, 0, 1), p001),
                ((1, 0), (0, 0, 1), p101),
                ((1, 1), (0, 0, 1), p111),
                ((0, 0), (0, 0, 1), p001),
                ((1, 1), (0, 0, 1), p111),
                ((0, 1), (0, 0, 1), p011),
            ]

            # Back face (sisi belakang, z = z_min), normal (0, 0, -1)
            vertices += [
                ((0, 0), (0, 0, -1), p000),
                ((1, 1), (0, 0, -1), p110),
                ((1, 0), (0, 0, -1), p100),
                ((0, 0), (0, 0, -1), p000),
                ((0, 1), (0, 0, -1), p010),
                ((1, 1), (0, 0, -1), p110),
            ]

            # Left face (sisi kiri, x = x_min), normal (-1, 0, 0)
            vertices += [
                ((0, 0), (-1, 0, 0), p000),
                ((1, 0), (-1, 0, 0), p001),
                ((1, 1), (-1, 0, 0), p011),
                ((0, 0), (-1, 0, 0), p000),
                ((1, 1), (-1, 0, 0), p011),
                ((0, 1), (-1, 0, 0), p010),
            ]

            # Right face (sisi kanan, x = x_max), normal (1, 0, 0)
            vertices += [
                ((0, 0), (1, 0, 0), p100),
                ((1, 0), (1, 0, 0), p110),
                ((1, 1), (1, 0, 0), p111),
                ((0, 0), (1, 0, 0), p100),
                ((1, 1), (1, 0, 0), p111),
                ((0, 1), (1, 0, 0), p101),
            ]

            # Top face (atas, y = y_max), normal (0, 1, 0)
            vertices += [
                ((0, 0), (0, 1, 0), p010),
                ((1, 0), (0, 1, 0), p011),
                ((1, 1), (0, 1, 0), p111),
                ((0, 0), (0, 1, 0), p010),
                ((1, 1), (0, 1, 0), p111),
                ((0, 1), (0, 1, 0), p110),
            ]

            # Bottom face (bawah, y = y_min), normal (0, -1, 0)
            # Perbaikan: Urutan vertex diubah sehingga jika face culling aktif, sisi bawah tetap dirender
            vertices += [
                ((0, 0), (0, -1, 0), p000),
                ((1, 0), (0, -1, 0), p100),
                ((1, 1), (0, -1, 0), p101),
                ((0, 0), (0, -1, 0), p000),
                ((1, 1), (0, -1, 0), p101),
                ((0, 1), (0, -1, 0), p001),
            ]

            return vertices

        # --- Definisikan bagian meja ---

        # Table top: sebuah box dengan ketebalan 0.1 (y dari 1 sampai 1.1)
        top_vertices = create_box(
            x_min=-2, x_max=2, y_min=1, y_max=1.1, z_min=-2, z_max=2
        )

        # Kaki meja: masing-masing dibuat sebagai box dengan ukuran yang sesuai.
        leg1 = create_box(
            x_min=-1.7, x_max=-1.3, y_min=0, y_max=1, z_min=-1.7, z_max=-1.3
        )
        leg2 = create_box(
            x_min=1.3, x_max=1.7, y_min=0, y_max=1, z_min=-1.7, z_max=-1.3
        )
        leg3 = create_box(x_min=1.3, x_max=1.7, y_min=0, y_max=1, z_min=1.3, z_max=1.7)
        leg4 = create_box(
            x_min=-1.7, x_max=-1.3, y_min=0, y_max=1, z_min=1.3, z_max=1.7
        )

        # Gabungkan semua vertex
        all_vertices = top_vertices + leg1 + leg2 + leg3 + leg4

        # Konversi list vertex ke numpy array dengan format: [texcoord (2), normal (3), posisi (3)]
        vertex_data = []
        for texcoord, normal, position in all_vertices:
            vertex_data.append(list(texcoord) + list(normal) + list(position))

        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data


class CylinderVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "newobjects/Models/cylinder.obj",
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


class DarkwallVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "newobjects/Models/darkWallTest.obj",
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


class MugVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self):
        # Load .obj without .mtl
        objs = pywavefront.Wavefront(
            "objects/mug/mug.obj",
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
