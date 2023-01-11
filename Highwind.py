from operator import index
from struct import Struct
from array import array
from OpenGL import GL
import ctypes

scale = 10

class HighwindPart:

    def __init__(self,nome):
        registro = Struct("<fffBBBB")
        registroFace = Struct("<Biii")
        vertices = array("f")
        cores = array("f")
        indices = array("i")
        nvertex = 0
        nface = 0
        with open(f"objs/highwind/{nome}","rb") as f:
            for i, linha in enumerate(f):
                l2 = linha.decode('ascii')[:-1].split(" ")
                if len(l2) == 3 and l2[1] == "vertex":
                    nvertex = int(l2[2])
                if len(l2) == 3 and l2[1] == "face":
                    nface = int(l2[2])
                if l2[0] == "end_header":
                    break

            for i in range(nvertex):
                x, y, z, r, g, b, a = registro.unpack(f.read(registro.size))
                vertices.append(x)
                vertices.append(y)
                vertices.append(z)
               
                cores.append(r/255)
                cores.append(g/255)
                cores.append(b/255)
                cores.append(a/255)

            for i in range(nface):
                n,v0,v1,v2 = registroFace.unpack(f.read(registroFace.size))
                indices.append(v0)
                indices.append(v1)
                indices.append(v2)
                

        self.arrayBufferId = GL.glGenVertexArrays(1)
        self.N = len(indices)
        GL.glBindVertexArray(self.arrayBufferId)
        GL.glEnableVertexAttribArray(0) # POSITION
        GL.glEnableVertexAttribArray(1) # COLOR

        idBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idBuffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(vertices)*vertices.itemsize, ctypes.c_void_p(vertices.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
#        GL.glVertexAttribPointer(1,4,GL.GL_FLOAT,GL.GL_FALSE,0,0)

        idBufferColor = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idBufferColor)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(cores)*cores.itemsize, ctypes.c_void_p(cores.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(1,4,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        idIndex = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, idIndex)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(indices)*indices.itemsize, ctypes.c_void_p(indices.buffer_info()[0]), GL.GL_STATIC_DRAW)

    def draw(self):
        GL.glBindVertexArray(self.arrayBufferId)
        GL.glDrawElements(GL.GL_TRIANGLES, self.N, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

class Highwind:

    def __init__(self):
        arquivos = [
            "ImageToStl.com_deck.ply",
            "ImageToStl.com_front_end.ply",
            "ImageToStl.com_fuselage_hollow.ply",
            "ImageToStl.com_fuselage_solid.ply",
            "ImageToStl.com_left_boom.ply",
            "ImageToStl.com_left_prop.ply",
            "ImageToStl.com_left_turbine.ply",
            "ImageToStl.com_right_boom.ply",
            "ImageToStl.com_right_prop.ply",
            "ImageToStl.com_right_turbine.ply",
            "ImageToStl.com_rotors.ply"
        ]
        self.parts = []
        for a in arquivos:
            self.parts.append(HighwindPart(a))


    def draw(self):
        for p in self.parts:
            p.draw()


