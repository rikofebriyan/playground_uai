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

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True
        )
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
