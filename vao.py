from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos["cube"] = self.get_vao(
            program=self.program.programs["default"], vbo=self.vbo.vbos["cube"]
        )

        # shadow cube vao
        self.vaos["shadow_cube"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["cube"]
        )

        # cat vao
        self.vaos["cat"] = self.get_vao(
            program=self.program.programs["default"], vbo=self.vbo.vbos["cat"]
        )

        # shadow cat vao
        self.vaos["shadow_cat"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["cat"]
        )

        # skybox vao
        self.vaos["skybox"] = self.get_vao(
            program=self.program.programs["skybox"], vbo=self.vbo.vbos["skybox"]
        )

        # advanced_skybox vao
        self.vaos["advanced_skybox"] = self.get_vao(
            program=self.program.programs["advanced_skybox"],
            vbo=self.vbo.vbos["advanced_skybox"],
        )

        # bola vao
        self.vaos["bola"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["bola"],
        )

        # apple vao
        self.vaos["apple"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["apple"],
        )

        # cone vao
        self.vaos["cone"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["cone"],
        )

        # shadow apple vao
        self.vaos["shadow_apple"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["apple"]
        )

        # shadow cone vao
        self.vaos["shadow_cone"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["cone"]
        )

        # shadow bola vao
        self.vaos["shadow_bola"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["bola"]
        )

        # fenceRight vao
        self.vaos["fenceRight"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["fenceRight"],
        )

        # shadow fenceRight vao
        self.vaos["shadow_fenceRight"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["fenceRight"]
        )

        # fenceback vao
        self.vaos["fenceback"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["fenceback"],
        )

        # shadow fenceback vao
        self.vaos["shadow_fenceback"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["fenceback"]
        )

        # fencefront vao
        self.vaos["fencefront"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["fencefront"],
        )

        # shadow fencefront vao
        self.vaos["shadow_fencefront"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["fencefront"]
        )

        # papan vao
        self.vaos["papan"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["papan"],
        )

        # shadow papan vao
        self.vaos["shadow_papan"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["papan"]
        )

        # table vao
        self.vaos["table"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["table"],
        )

        # shadow table vao
        self.vaos["shadow_table"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["table"]
        )

        # cylinder vao
        self.vaos["cylinder"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["cylinder"],
        )

        # shadow cylinder vao
        self.vaos["shadow_cylinder"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["cylinder"]
        )

        # darkwall vao
        self.vaos["darkwall"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["darkwall"],
        )

        # shadow darkwall vao
        self.vaos["shadow_darkwall"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["darkwall"]
        )

        # mug vao
        self.vaos["mug"] = self.get_vao(
            program=self.program.programs["default"],
            vbo=self.vbo.vbos["mug"],
        )

        # shadow mug vao
        self.vaos["shadow_mug"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["mug"]
        )



    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True
        )
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
