# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from collections import defaultdict

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def solution(edges):
    vs = set()
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    g = Graph(len(vs))

    vs = list(vs)
    vsi = {}
    for i, v in enumerate(vs):
        vsi[v] = i

    for u, v in edges:
        g.addEdge(vsi[u], vsi[v])
    ret = ",".join(sorted([vs[i] for i in g.AP()]))
    if ret == "":
        ret = "-"
    return ret

class Graph:

    def __init__(self, vertices):
        self.V = vertices # No. of vertices
        self.graph = defaultdict(list) # default dictionary to store graph
        self.Time = 0

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    '''A recursive function that find articulation points
    using DFS traversal
    u --> The vertex to be visited next
    visited[] --> keeps track of visited vertices
    disc[] --> Stores discovery times of visited vertices
    parent[] --> Stores parent vertices in DFS tree
    ap[] --> Store articulation points'''
    def APUtil(self, u, visited, ap, parent, low, disc):

        # Count of children in current node
        children = 0

        # Mark the current node as visited and print it
        visited[u]= True

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if visited[v] == False :
                parent[v] = u
                children += 1
                self.APUtil(v, visited, ap, parent, low, disc)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                low[u] = min(low[u], low[v])

                # u is an articulation point in following cases
                # (1) u is root of DFS tree and has two or more children.
                if parent[u] == -1 and children > 1:
                    ap[u] = True

                #(2) If u is not root and low value of one of its child is more
                # than discovery value of u.
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True

                # Update low value of u for parent function calls
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])


    # The function to do DFS traversal. It uses recursive APUtil()
    def AP(self):

        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        visited = {k: False for k in self.graph}
        disc = {k: float("Inf") for k in self.graph}
        low = {k: float("Inf") for k in self.graph}
        parent = [-1] * (self.V)
        ap = [False] * (self.V) # To store articulation points

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range(self.V):
            if visited[i] == False:
                self.APUtil(i, visited, ap, parent, low, disc)

        for index, value in enumerate (ap):
            if value == True:
                yield index

def main():
    t = read_int()

    for i in range(t):
        n = read_int()
        edges = []
        for _ in range(n):
            edges.append(input().strip().split(","))
        s = solution(edges)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
