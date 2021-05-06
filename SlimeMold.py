import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ExampleGraphs
import importlib
from Drawing import DrawGraph
import argparse
import sys
import os

def main(args):

    parser = argparse.ArgumentParser(description='Simulate slime mold behavior in a maze. Creates MP4 video of simulation. If video creation does not work, you can still see the frames in the images/ folder. For best results , make sure there is an actual path from source to sink!')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('--custom', action='store_true',help='Allows you to draw a custom maze')
    group.add_argument('--example', action='store_true', help='Use the example takagaki maze instead of making your own')
    
    parser.add_argument('--videoname', type=str, default='animation.mp4', help='Specify filename to save simulation video as (.mp4 file).')
    parser.add_argument('--framerate', type=int, default=2, help='Framerate of video in frames/second')
    parser.add_argument('--rounds', type=int, default=30, help='Number of time steps to simulate')
 
    args = parser.parse_args(args[1:])
    
    # Create images folder if not there already
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = 'images'
    images_path = os.path.join(curr_dir, images_dir)
    
    if not os.path.isdir(images_path): 
        os.mkdir(images_path)
    
    # Get the maze
    graph_params = None
    
    if args.custom:
        graph_params = DrawGraph().userDrawGraph()
    else:
        graph_params = ExampleGraphs.TakagakiMaze()

    D = graph_params['D']
    L = graph_params['L']
    pos = graph_params['pos']
    src = graph_params['src']
    sink = graph_params['sink']
    
    if not pos:
        return

    graph = nx.from_numpy_matrix(D)
    
    N = len(L)
    
    node_colors = ['grey']*N
    node_colors[src] = 'lightgreen'
    node_colors[sink] = 'lightgreen'
    
    try:
        for round in range(args.rounds):

            # Update nx graph edges for visualization
            for i in range(N):
                for j in range(i, N):
                    if(D[i][j] != 0):
                        graph[i][j]['weight'] = D[i][j]
            weights = [graph[u][v]['weight'] for u,v in graph.edges()]

            plt.cla()
            #fig = plt.figure()
            nx.draw(graph, pos, node_color=node_colors,
                    width=list(weights * 100),
                    with_labels=True)

            plt.savefig(f'{images_dir}/graph{str(round).zfill(2)}.png', dpi=200)

            #fig.show()

            #plt.close(fig)

            # sum of currents leaving each node using KCL
            sums = np.zeros(N)
            sums[src] = 1
            sums[sink] = -1


            # Conductance of edges = D / L
            cond = np.divide(D,L)

            # Solve for node pressures 

            A = - np.copy(cond)

            for i in range(N):
                A[i][i] = np.sum(cond[i]) - cond[i][i]

            # Pressure of sink node is 0
            A[sink, :] = 0

            A_inv = np.linalg.pinv(A)

            press = np.matmul(A_inv,sums)

            # Update diameters using slime mold algorithm

            # difference in pressure between nodes
            dP = np.zeros((N,N))
            for i in range(N):
                for j in range(i, N):
                    dP[i][j] = press[i] - press[j]
                    dP[j][i] = - dP[i][j]

            #print("dP:" + str(dP))

            # Flow through each edge
            Q = cond * dP

            # Update diameters
            D = 0.5*( (Q*dP / (L*press[src])) + D)
        
    except:
        print('Something weird happened during simulation :( Try redrawing your graph')
        return
        
        
    # Create mp4 from images
    import subprocess

    cmd = f"ffmpeg -y -framerate {args.framerate} -i images/graph%2d.png {args.videoname}"
    returned_value = subprocess.call(cmd)  # returns the exit code in unix
    if returned_value == 0:
        print('Successfully created MP4 video of animation')
    else:
        print('Failed to create MP4 video of Animation')
    
    

if __name__ == "__main__":
   main(sys.argv)
