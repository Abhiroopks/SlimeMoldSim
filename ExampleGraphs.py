import numpy as np
from EdgeSetter import EdgeSetter

# Returns approximation of the maze in
# T. Nakagaki, H. Yamada, and A. Toth. Maze-solving by an amoeboid organism. Nature, 407:470, 2000.
def TakagakiMaze():
    
    N = 19
    
    # Length, width of edges
    L = np.ones((N,N))
    D = np.zeros((N,N))    
     
    # dict of x,y coords for each node. Useful for visualization in networkx
    pos = {}
    pos[0] = [-1, -1]
    pos[1] = [-1, 0]
    pos[2] = [-1, 1]
    pos[3] = [-0.67, -1]
    pos[4] = [-0.67, 0]
    pos[5] = [-0.67, 0.5]
    pos[6] = [-0.33, -1]
    pos[7] = [-0.33, 0]
    pos[8] = [-0.33, 0.5]
    pos[9] = [0, 1]
    pos[10] = [0.33, 1]
    pos[11] = [0.33, 0.5]
    pos[12] = [0.33, -0.5]
    pos[13] = [0.67, 1]
    pos[14] = [1, -0.5]
    pos[15] = [1, -1]
    pos[16] = [0.67, -0.5]
    pos[17] = [0.67, -1]
    pos[18] = [0.33, -1]
    
    edgesetter = EdgeSetter(D,L,pos)
    
    # initialize the edges and lengths
    edgesetter.setEdge(0,1)          
    edgesetter.setEdge(1,2)            
    edgesetter.setEdge(3,4)            
    edgesetter.setEdge(1,4)            
    edgesetter.setEdge(4,5)            
    edgesetter.setEdge(6,7)            
    edgesetter.setEdge(7,8)            
    edgesetter.setEdge(5,9)            
    edgesetter.setEdge(2,9)            
    edgesetter.setEdge(9,10)            
    edgesetter.setEdge(8,11)            
    edgesetter.setEdge(10,11)            
    edgesetter.setEdge(10,13)            
    edgesetter.setEdge(13,14)            
    edgesetter.setEdge(14,15)            
    edgesetter.setEdge(14,16)            
    edgesetter.setEdge(16,17)            
    edgesetter.setEdge(12,16)            
    edgesetter.setEdge(11,12)            
    edgesetter.setEdge(17,18)            
    
    return {'L': L, 'D': D, 'pos': pos, 'src': 0, 'sink' : [18]}
    