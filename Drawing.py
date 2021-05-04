#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import tkinter.simpledialog
from EdgeSetter import EdgeSetter
import numpy as np

class DrawGraph:
    
    def __init__(self):

        self.pos = {}
        self.root = tk.Tk('Graph Canvas')
        
        width  = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.width = int(min(width,height))
        
        self.R = self.width / 40
        
        self.root.geometry(f'{int(self.width)}x{int(self.width)}')
        
        self.root.resizable(0,0)
        
        self.canvas= tk.Canvas(self.root)
        self.canvas.pack_propagate(0)
        
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.bind("<Button-3>", self.rightclick)
        self.canvas.bind("<B3-Motion>", self.rightdrag)
        self.canvas.bind("<ButtonRelease-3>", self.rightRelease)
        self.canvas.bind("<Button-1>", self.leftclick)
        
        # Used for keeping track of line being drawn
        self.coords = {"x":0,"y":0,"x2":0,"y2":0}
        self.latestLine = None

        self.edges = []
        
    def userDrawGraph(self):
        
        
        helpMessage ="""
        To create new node: click left mouse button at desired location.\n
        To create new edge: click and drag right mouse button from one node to another.\n
        When finished, simply close the graph canvas window.
        """
        
        print(helpMessage)
        
        self.canvas.mainloop()

        
        pos = self.pos
        edges = self.edges
        N = len(pos)
        
        source_node = None
        sink_node = None
        
        # Length, width of edges
        L = np.ones((N,N))
        D = np.zeros((N,N)) 
        
        if N == 0:
            print('No nodes created. Exiting now')
            return {'L': L, 'D': D, 'pos': None, 'src': source_node, 'sink': sink_node}
        
        if len(edges) == 0:
            print('No edges created. Exiting now')
            return {'L': L, 'D': D, 'pos': None, 'src': source_node, 'sink': sink_node}
        
        
        edgesetter = EdgeSetter(D,L,pos)

        for i in range(len(edges)):
            edgesetter.setEdge(edges[i][0], edges[i][1])
            
        # Ask user which node is source, and which are sinks
        print('Specify the source node by index')
        valid = False
                
        while not valid:
            
            raw = input()
            
            try:
                source_node = int(raw)
            except:
                print(f'Enter a valid integer! Invalid input: {raw}')
                continue
            
            if source_node < len(pos) and source_node >= 0:
                valid = True
            else:
                print(f'Invalid index for source node. Must be: 0 <= index < {len(pos)}')
        
        
        print('Specify the sink nodes by index, separated by single spaces')
        
        valid = False
        
        while not valid:
            
            raw = input()
            
            try:
                sink_node = int(raw)
            except:
                print(f'Enter a valid integer! Invalid input: {raw}')
                continue
            if sink_node == source_node:
                print(f'Sink cannot be same as source node. Choose index other than {source_node}')
                continue   
            if sink_node >= len(pos) or sink_node < 0:
                print(f'Invalid index for sink node. Must be: 0 <= index < {len(pos)}')
                continue
                
            valid = True

        return {'L': L, 'D': D, 'pos': pos, 'src': source_node, 'sink': sink_node}

    def leftclick(self,event):
        
        ind = self.isCoordAcceptable([event.x, event.y])
        if ind != -1:
            print('Invalid point. Cannot be overlapping another node.')
            return

        pos = self.pos
        R = self.R

        # Store position of node in dict
        pos[len(pos)] = [(event.x - self.width)/self.width, (self.width - event.y)/self.width]

        self.canvas.create_oval(event.x - R, event.y - R, event.x + R, event.y + R, fill='red', outline='blue')
        
        # Draw text for index of this point
        self.canvas.create_text(event.x, event.y, font=('Arial', int(self.R/2)), fill='#fff', state=tk.DISABLED, text=str(len(pos)-1))


    def isCoordWithinPoint(self,point, coord):

        R = self.R

        x = (coord[0]-self.width)/self.width
        y = (self.width - coord[1])/self.width

        R_adj = R/self.width

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
        if ind0 == ind1:
            print("Invalid line. Cannot draw edge from a node to itself.")
            canvas.delete(latestLine)
            return

        # Store this edge
        edges.append((ind0, ind1))
        
        # Center endpoints of line within center of nodes
        canvas.coords(latestLine, self.width*pos[ind0][0] + self.width, -(self.width*pos[ind0][1] - self.width), self.width*pos[ind1][0] + self.width, -(self.width*pos[ind1][1] - self.width))


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




