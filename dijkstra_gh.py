__author__ = "Gizem Yetis"
__institution__ = "Middle East Technical University, Department of Architecture, Building Science"
__mail__ = "gizemyetis93@gmail.com"

import rhinoscriptsyntax as rs
import sys
import itertools

faces=rs.MeshFaceVertices(mesh)
vertices=rs.MeshVertices(mesh)

edge_index=[]
for face in faces:
    edge_index += [[face[0]] + [face[1]]] + [[face[0]] + [face[2]]] + [[face[1]] + [face[2]]]

edges=[]
for ind in edge_index:
    edges.append(rs.AddLine(vertices[ind[0]] , vertices[ind[1]]))

edge_length=[]
for edge in edges:
    edge_length.append(rs.CurveLength(edge))

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = sys.maxint     
        self.visited = False  
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortpath(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortpath(v.previous, path)
    return

import heapq
from heapq import *

def dijkstra(aGraph, start):
    start.set_distance(0)

    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        for next in current.adjacent:
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

g = Graph()

for v in range(len(vertices)):
    g.add_vertex(v)

zipped=[]
for e , l in zip(edge_index , edge_length):
    zipped += [e + [l]]

for z in zipped:
    g.add_edge(z[0] , z[1] , z[2])

for v in g:
    for w in v.get_connections():
        vid = v.get_id()
        wid = w.get_id()

dijkstra(g, g.get_vertex(start))

target = g.get_vertex(target)
path = [target.get_id()]
shortpath(target, path)
print 'The shortest path : %s' %(path[::-1])

ptsLine = [vertices[p] for p in path]
shortestLine = rs.AddCurve(ptsLine)
print Line
