import numpy as np

"""
Create both edges:
* frm -> to
* to -> from

Calculates edge length from node positions

"""
class EdgeSetter:
    
    def __init__(self, D, L, pos):
        self.D = D
        self.L = L
        self.pos = pos


    def setEdge(self, frm, to):
    
        length = np.linalg.norm((np.array(self.pos[frm]) - np.array(self.pos[to])), 2)
        self.D[frm][to] = self.D[to][frm] = 1
        self.L[frm][to] = self.L[to][frm] = length