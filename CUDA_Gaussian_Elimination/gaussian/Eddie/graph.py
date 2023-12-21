'''
This is my homemade ADT for graphs.
Chandler Welch
2022.08.06
CS2420
'''
import math as meth

class Graph:
    '''This is my adt class for a graph. this will make a graph obj.'''

    def __init__(self):
        '''This is my constructor that will initiate the obj.'''
        self._edges = []
        self._vertex = []
        self._edge_attr = []
        self._vert_attr = []


    def __str__(self):
        '''Produce a string representation of the graph that can be used
        with print().'''
        counter = 0
        string = 'digraph G {\n'
        for v in range(len(self._vertex)):
            string += ('''   {} [shape="{}"]\n'''.format(self._vertex[v], self._vert_attr[v]))
        for edge in self._edges:
            if edge is not meth.inf:
                first_v = counter // len(self._vertex)
                second_v = counter % len(self._vertex)
                string += ('''   {} -> {} [label="{}",weight="{}", style="{}", arrowhead="none"];\n'''.format(\
                 self._vertex[first_v], self._vertex[second_v],edge,edge, self._edge_attr[counter]))
            counter+=1
        string += '}\n'
        return string


    def add_vertex(self, label, shape='circle'):
        '''add a vertex with the specified label. Return the graph. label must
        be a string or raise ValueError '''
        if label is None or not isinstance(label, str):
            raise ValueError('please enter the name of the new lable')
        if label not in self._vertex:
            temp = []
            temp_edge = []
            prev_max_edges = len(self._vertex)
            self._vertex.append(label)
            self._vert_attr.append(shape)
            for i in range(prev_max_edges):
                # this will get each vertexes edges
                individual = self._edges[(i)*prev_max_edges:((i+1)*prev_max_edges)]
                individual.append(meth.inf)
                temp_indiv = self._edge_attr[(i)*prev_max_edges:((i+1)*prev_max_edges)]
                temp_indiv.append(meth.inf)
                #temp_vert = self._edge_attr[(i)*prev_max_edges:((i+1)*prev_max_edges)]
                #temp_vert.append(meth.inf)
                temp_edge = temp_edge + temp_indiv
                #temp_attr = temp_attr + temp_vert
                temp = temp + individual
            self._edges = temp + [meth.inf] * (prev_max_edges+1)
            self._edge_attr = temp_edge + [meth.inf] * (prev_max_edges+1)
            #self._vert_attr = temp_vert + [meth.inf] * (prev_max_edges+1)
            return self


    def add_edge(self, src, dest, w, style="solid"):
        '''add an edge from vertex src to vertex dest with weight w. Return
        the graph. validate src, dest, and w: raise ValueError if not valid.'''
        try:
            w = float(w)
        except:
            pass
        if dest in self._vertex and src in self._vertex and isinstance(w, float):
            row = self._vertex.index(src)
            column = self._vertex.index(dest)
            location = row*len(self._vertex) + column
            self._edges[location] = w
            self._edge_attr[location] = style
            #print(location, self._edges)
            return self
        raise ValueError('Vertex or edge value error.')
    

    def get_weight(self, src, dest) -> float:
        '''Return the weight on edge src-dest (math.inf if no path exists,
        raise ValueError if src or dest not added to graph).'''
        if dest in self._vertex and src in self._vertex:
            row = self._vertex.index(src)
            column = self._vertex.index(dest)
            location = row*len(self._vertex) + column
            return self._edges[location]
            print(location, self._edges)
        raise ValueError('Vertex not in graph')


    def dfs(self, starting_vertex):
        '''Return a generator for traversing the graph in depth-first
        order starting from the specified vertex. Raise a ValueError if
         the vertex does not exist.'''
        temp = []
        depth_first = []
        if starting_vertex in self._vertex:
            depth_first.append(starting_vertex)
            start = self._vertex.index(starting_vertex)*len(self._vertex)
            for i in range(len(self._vertex)):
                place = self._edges[i+start]
                if place is not meth.inf and self._vertex[i] not in depth_first:
                    temp.append(self._vertex[i])
                    depth_first.append(self._vertex[i])
                while len(temp)>0:
                    vertex = temp.pop()
                    n_squared = self._vertex.index(vertex)*len(self._vertex)
                    for n in range(len(self._vertex)):
                        spot = self._edges[n+n_squared]
                        if spot is not meth.inf and self._vertex[n] not in depth_first:
                            temp.append(self._vertex[n])
                            depth_first.append(self._vertex[n])
            return depth_first


    def bfs(self, starting_vertex):
        '''Return a generator for traversing the graph in breadth-first
        order starting from the specified vertex. Raise a ValueError if
        the vertex does not exist.'''
        temp = []
        bredth_first = []
        if starting_vertex in self._vertex:
            bredth_first.append(starting_vertex)
            start = self._vertex.index(starting_vertex)*len(self._vertex)
            for i in range(len(self._vertex)):
                place = self._edges[i+start]
                if place is not meth.inf and self._vertex[i] not in bredth_first:
                    temp.append(self._vertex[i])
                    bredth_first.append(self._vertex[i])
            while len(temp) > 0:
                vertex = temp[0]
                temp.remove(vertex)
                n_squared = self._vertex.index(vertex)*len(self._vertex)
                for n in range(len(self._vertex)):
                    spot = self._edges[n+n_squared]
                    if spot is not meth.inf and self._vertex[n] not in bredth_first:
                        temp.append(self._vertex[n])
                        bredth_first.append(self._vertex[n])
            return bredth_first


    def dsp(self, src, dest) -> list:
        '''Return a tuple (path length , the list of vertices on the path
        from dest back to src). If no path exists, return the tuple
        (math.inf,  empty list.)'''
        least = {}
        my_que = self.bfs(src)
        temp = []
        path = {}
        for vert in my_que:
            if vert == src:
                least[vert]=0.00
                path[vert] = [src]
            else:
                least[vert] = meth.inf
                path[vert] = [src]

        i=0
        while len(my_que)>0:
            current_vertex = my_que[i]
            my_que.remove(current_vertex)
            for node in self._vertex:
                try:
                    current_weight = self.get_weight(current_vertex,node)
                except:
                    current_weight = meth.inf
                if current_weight is not meth.inf:
                    if least[current_vertex] + current_weight < least[node]:
                        least[node] = least[current_vertex] + current_weight
                        path[node] = path[current_vertex] + [node]
        try:
            return (least[dest], path[dest])
        except:
            return (meth.inf, [])


    def dsp_all(self, src) -> dict:
        '''Return a dictionary of the shortest weighted path between src
        and all other vertices using Dijkstra's Shortest Path algorithm.
        In the dictionary, the key is the the destination vertex label,
        the value is a list of vertices on the path from src to dest
        inclusive.'''
        least = {}
        my_que = self.dfs(src)
        temp = []
        path = {}
        for vert in self._vertex:
            if vert == src:
                least[vert]=0.00
                path[vert] = [src]
            else:
                least[vert] = meth.inf
                path[vert] = []

        i=0
        while len(my_que)>0:
            current_vertex = my_que[i]
            my_que.remove(current_vertex)
            for node in self._vertex:
                try:
                    current_weight = self.get_weight(current_vertex,node)
                except:
                    current_weight = meth.inf
                if current_weight is not meth.inf:
                    if least[current_vertex] + current_weight < least[node]:
                        least[node] = least[current_vertex] + current_weight
                        path[node] = path[current_vertex] + [node]
        return path


def main():
    g = Graph()
    g.add_vertex("A", shape='square')
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_vertex("E")
    g.add_vertex("F")

    g.add_edge("A", "B", 2, style='dashed')
    g.add_edge("A", "F", 9, style='dotted')

    g.add_edge("B", "F", 6, style="dashed")
    g.add_edge("B", "D", 15)
    g.add_edge("B", "C", 8)

    g.add_edge("C", "D", 1)

    g.add_edge("E", "C", 7)
    g.add_edge("E", "D", 3)

    g.add_edge("F", "B", 6)
    g.add_edge("F", "E", 3)
    with open('Graph_image.dot', 'w') as source:
        print(g, file=source)


if __name__ == "__main__":
    main()

#https://pyeda.readthedocs.io/en/latest/bdd.html