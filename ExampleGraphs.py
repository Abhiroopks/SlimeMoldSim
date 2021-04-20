import numpy as np

# Returns approximation of the maze in
# T. Nakagaki, H. Yamada, and A. Toth. Maze-solving by an amoeboid organism. Nature, 407:470, 2000.
def TakagakiMaze():
    
    N = 23
    
    # Length, width of edges
    L = np.ones((N,N))
    D = np.zeros((N,N))    
    
    # initialize the edges and lengths
    setEdge(D,L,
   
    
    
    
# Returns another example maze
def exampleMaze0():
    
    N = 10
    
    # Length, width of edges
    L = np.ones((N,N))
    D = np.zeros((N,N))
    
    # initialize the edges and lengths
    setEdge(D,L,0,1,1)
    setEdge(D,L,1,9,1)
    setEdge(D,L,2,9,0.5)
    setEdge(D,L,1,3,0.5)
    setEdge(D,L,3,4,1)
    setEdge(D,L,2,5,1)
    setEdge(D,L,5,6,0.5)
    setEdge(D,L,5,8,2)
    setEdge(D,L,6,7,2)
    setEdge(D,L,8,7,0.5)
    
    
    # dict of x,y coords for each node. Useful for visualization in networkx
    pos = {}
    pos[0] = [-1, -1]
    pos[1] = [-1, 0]
    pos[2] = [-0.5, 1]
    pos[3] = [-0.5, 0]
    pos[4] = [-0.5, -1]
    pos[5] = [0.5, 1]
    pos[6] = [1, 1]
    pos[7] = [1, -1]
    pos[8] = [0.5, -1]
    pos[9] = [-1, 1]
    
    return {'L': L, 'D': D, 'pos': pos}
    
"""
Create both edges:
* frm -> to
* to -> from

"""
def setEdge(D, L, frm, to, length):
    
    D[frm][to] = D[to][frm] = 1
    L[frm][to] = L[to][frm] = length