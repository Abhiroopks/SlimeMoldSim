#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import tkinter.simpledialog
from EdgeSetter import EdgeSetter
import numpy as np

class DrawGraph:
    
    def __init__(self):

        self.pos = {}
        self.R = 10

        # Used for keeping track of line being drawn
        self.coords = {"x":0,"y":0,"x2":0,"y2":0}
        self.latestLine = None

        self.edges = []
        
    def userDrawGraph(self):

        root = tk.Tk()
        self.canvas= tk.Canvas(root, width=600, height=600)
        canvas = self.canvas

        canvas.pack()
        canvas.bind("<Button-3>", self.rightclick)
        canvas.bind("<B3-Motion>", self.rightdrag)
        canvas.bind("<ButtonRelease-3>", self.rightRelease)
        canvas.bind("<Button-1>", self.leftclick)

        canvas.mainloop()
        
        pos = self.pos
        edges = self.edges
        N = len(pos)
        # Length, width of edges
        L = np.ones((N,N))
        D = np.zeros((N,N)) 

        edgesetter = EdgeSetter(D,L,pos)

        for i in range(len(edges)):
            edgesetter.setEdge(edges[i][0], edges[i][1])
            
        # Ask user which node is source, and which are sinks
        print('Specify the source node by index')
        valid = False
        
        while not valid:
            source_node = int(input())
            if source_node < len(pos) and source_node >= 0:
                valid = True
            else:
                print(f'Invalid index for source node. Must be: 0 <= index < {len(pos)}')
        
        
        print('Specify the sink nodes by index, separated by single spaces')
        
        valid = False
        
        while not valid:
            valid = True
            
            sink_nodes = input().split(' ')
            
            for i in range(len(sink_nodes)):
                if int(sink_nodes[i]) < 0:
                    print(f'Invalid index for sink node: {sink_nodes[i]}. Must be >= 0 ')
                    valid = False
                    break
                elif not int(sink_nodes[i]) < len(pos):
                    print(f'Invalid index for sink node: {sink_nodes[i]}. Must be < {len(pos)}')
                    valid = False
                    break
                elif int(sink_nodes[i]) == source_node:
                    print(f'Sink node cannot be same as source node. Choose index other than {source_node}')
                    valid = False
                    break
                       
        
        return {'L': L, 'D': D, 'pos': pos, 'src': source_node, 'sinks': sink_nodes}

    def leftclick(self,event):

        pos = self.pos
        R = self.R

        # Store position of node in dict
        pos[len(pos)] = [(event.x - 300)/300, (300 - event.y)/300]

        self.canvas.create_oval(event.x - R, event.y - R, event.x + R, event.y + R, fill='red', outline='blue')
        
        # Draw text for index of this point
        self.canvas.create_text(event.x, event.y,fill='#fff', state=tk.DISABLED, text=str(len(pos)-1))


    def isCoordWithinPoint(self,point, coord):

        R = self.R

        x = (coord[0]-300)/300
        y = (300 - coord[1])/300

        R_adj = R/300

        leftx = point[0] - R_adj
        lefty = point[1] + R_adj
        rightx = point[0] + R_adj
        righty = point[1] - R_adj

        return (leftx <= x <= rightx) and (lefty >= y >= righty)


    def isCoordAcceptable(self,coord):
        '''
        Given [x,y] of a point, ensure it is within an existing node
        Return index of node it is within, -1 if none
        '''

        pos = self.pos

        for i in range(len(pos)):
            if self.isCoordWithinPoint(pos[i], coord):
                return i

        return -1


    def isLineAcceptable(self,lineCoords):
        '''
        Validate latest added line
        Both endpoints must be within existing nodes
        '''
        return (self.isCoordAcceptable([lineCoords[0], lineCoords[1]]), self.isCoordAcceptable([lineCoords[2], lineCoords[3]]))

    def rightRelease(self,event):

        latestLine = self.latestLine
        edges = self.edges
        canvas = self.canvas
        pos = self.pos

        (ind0, ind1) = self.isLineAcceptable(canvas.coords(latestLine))

        # Ensure both indices are valid (not -1)
        if (ind0 == -1) or (ind1 == -1):
            print("Invalid line")
            canvas.delete(latestLine)
            return

        # Store this edge
        edges.append((ind0, ind1))
        
        # Center endpoints of line within center of nodes
        canvas.coords(latestLine, 300*pos[ind0][0] + 300, -(300*pos[ind0][1] - 300), 300*pos[ind1][0] + 300, -(300*pos[ind1][1] - 300))


    def rightclick(self,event):

        coords = self.coords

        # define start point for line
        coords["x"] = event.x
        coords["y"] = event.y

        # create a line on this point and store it in the list
        self.latestLine = self.canvas.create_line(coords["x"],coords["y"],coords["x"],coords["y"], width=3)

    def rightdrag(self, e):
        coords = self.coords
        canvas = self.canvas

        # update the coordinates from the event
        coords["x2"] = e.x
        coords["y2"] = e.y

        # Change the coordinates of the last created line to the new coordinates
        canvas.coords(self.latestLine, coords["x"],coords["y"],coords["x2"],coords["y2"])




