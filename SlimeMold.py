import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ExampleGraphs
import importlib
from Drawing import DrawGraph
import argparse
import sys

def main(args):

    parser = argparse.ArgumentParser(description='Simulate slime mold behavior in a maze')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('--custom', action='store_true',help='Allow user to draw a custom maze')
    group.add_argument('--example', default='takagaki', choices=['takagaki','maze0'], help='Specify an example maze to use')
    
    parser.add_argument('--video', action='store_true', help='Create .MP4 video of simulation')
    parser.add_argument('--rounds', type=int, default=25, help='Number of time steps to simulate')
 
    args = parser.parse_args(args[1:])
    
    
    # Get the maze
    graph_params = None
    
    if args.custom:
        graph_params = DrawGraph().userDrawGraph()
    elif args.example == 'takagaki':
        graph_params = ExampleGraphs.TakagakiMaze()
    else:
        graph_params = ExampleGraphs.exampleMaze0()

    D = graph_params['D']
    L = graph_params['L']
    pos = graph_params['pos']
    src = graph_params['src']
    sinks = graph_params['sinks']

    graph = nx.from_numpy_matrix(D)
    
    N = len(L)

    for round in range(args.rounds):

        # Update nx graph edges for visualization
        for i in range(N):
            for j in range(i, N):
                if(D[i][j] != 0):
                    graph[i][j]['weight'] = D[i][j]
        weights = [graph[u][v]['weight'] for u,v in graph.edges()]

        plt.cla()
        #fig = plt.figure()
        nx.draw(graph, pos, 
                width=list(weights * 100),
                with_labels=True,
                node_color='lightgreen')

        plt.savefig(f'images/graph{str(round).zfill(2)}.png', dpi=200)

        #fig.show()

        #plt.close(fig)

        # sum of currents leaving each node using KCL
        sums = np.zeros(N)
        sums[src] = 1
        sink_flow = -1 / len(sinks)

        for sink in sinks:
            sums[int(sink)] = sink_flow

        # Conductance of edges = D / L
        cond = np.divide(D,L)

        # Solve for node pressures 

        A = - np.copy(cond)

        for i in range(N):
            A[i][i] = np.sum(cond[i]) - cond[i][i]

        # Pressure of sink nodes is 0
        #for sink in sinks:
        #    A[int(sink), :] = 0

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
        
        
        
    # Create mp4 from images
    import subprocess

    cmd = "ffmpeg -y -framerate 2 -i images/graph%2d.png animation.mp4"
    returned_value = subprocess.call(cmd)  # returns the exit code in unix
    if returned_value == 0:
        print('Successfully created MP4 video of animation')
    else:
        print('Failed to create MP4 video of Animation')
    
    

if __name__ == "__main__":
   main(sys.argv)
