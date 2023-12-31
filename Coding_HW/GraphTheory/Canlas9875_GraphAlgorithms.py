import heapq

class Node:
    def __init__(self) -> None:
        self.dist_from_src = float('inf')
        self.parent = None
        self.visited = False

class Graph:
    def __init__(self, graph) -> None:
        self.graph = graph

    def singleSourceWeightedShortestPath(self, source):
        '''
        1.1 Please write a function, singleSourceWeightedShortestPath(), to find the shortest paths from vertex A to all other vertices. 
        Please modify Dijkastr's algorithm so that if there are more than one minimum path from v to w, the path with the fewest number of edges is chosen. 
        '''
        vertices = {}
        for vertex in self.graph:
            vertices[vertex]=Node()
        vertices[source].dist_from_src = 0
        vertices[source].parent = source

        queue = [(0, source)]
        while queue:
            distance, vertex = heapq.heappop(queue)
            if vertices[vertex].visited:
                continue

            vertices[vertex].visited = True
            for neighbor in self.graph[vertex]:
                if vertices[neighbor].visited:
                    continue

                new_distance = distance + self.graph[vertex][neighbor]
                if new_distance < vertices[neighbor].dist_from_src:
                    vertices[neighbor].dist_from_src = new_distance
                    vertices[neighbor].parent = vertex
                    heapq.heappush(queue, (new_distance, neighbor))

        print(f"Vertex \t Weighted Distance from {source} \t Parent")
        for vertex in self.graph:
            print(vertex, "\t", vertices[vertex].dist_from_src, "\t\t\t\t", vertices[vertex].parent)

    def singleSourceUnweightedShortestPath(self, source):
        '''
        1.2 Please write a function, singleSourceUnweightedShortestPath(), to find the unweighted shortest paths from vertex B to all other vertices. 
        '''
        vertices = {}
        for vertex in self.graph:
            vertices[vertex]=Node()
        vertices[source].dist_from_src = 0
        vertices[source].parent = source

        queue = [(0, source)]
        while queue:
            distance, vertex = heapq.heappop(queue)
            if vertices[vertex].visited:
                continue

            vertices[vertex].visited = True
            for neighbor in self.graph[vertex]:
                if vertices[neighbor].visited:
                    continue

                new_distance = distance + 1
                if new_distance < vertices[neighbor].dist_from_src:
                    vertices[neighbor].dist_from_src = new_distance
                    vertices[neighbor].parent = vertex
                    heapq.heappush(queue, (new_distance, neighbor))

        print(f"Vertex \t Unweighted Distance from {source} \t Parent")
        for vertex in self.graph:
            print(vertex, "\t", vertices[vertex].dist_from_src, "\t\t\t\t", vertices[vertex].parent)

    def minSpanningTree(self, source):
        '''
        2.1 Please write a function, minSpanningTree(), to print one minimum spanning tree (represented by a sequence of vertices) from vertex A, and the 
        total weight of the minimum spanning tree.
        '''
        vertices = {}
        for vertex in self.graph:
            vertices[vertex]=Node()
        vertices[source].dist_from_src = 0
        vertices[source].parent = source

        queue = {source: 0}
        mst = []
        mst_cost = 0
        while queue:
            vertex = min( queue, key=queue.get )
            distance = queue.pop(vertex)

            if vertices[vertex].visited:
                continue

            vertices[vertex].visited = True
            mst.append(vertex)
            mst_cost += distance
            for neighbor in self.graph[vertex]:
                if vertices[neighbor].visited:
                    continue
                
                # Only update distance from source and parent if the neighboring vertex is smaller than what's already in the queue
                if neighbor in queue and queue[neighbor] < self.graph[vertex][neighbor]:
                    continue

                vertices[neighbor].dist_from_src = self.graph[vertex][neighbor]
                vertices[neighbor].parent = vertex
                queue[neighbor] = self.graph[vertex][neighbor]

        print(f"Minimum spanning tree: {mst}")
        print(f"Minimum spanning tree total weight: {mst_cost}")

    def maxSpanningTree(self, source):
        '''
        2.2 Please write a function, maxSpanningTree(), to print one maximum spanning tree (represented by a sequence of vertices) from vertex A, and the 
        total weight of the maximum spanning tree.  
        '''
        vertices = {}
        for vertex in self.graph:
            vertices[vertex]=Node()
        vertices[source].dist_from_src = 0
        vertices[source].parent = source

        queue = {source: 0}
        mst = []
        mst_cost = 0
        while queue:
            vertex = max( queue, key=queue.get )
            distance = queue.pop(vertex)

            if vertices[vertex].visited:
                continue

            vertices[vertex].visited = True
            mst.append(vertex)
            mst_cost += distance
            for neighbor in self.graph[vertex]:
                if vertices[neighbor].visited:
                    continue
                
                # Only update distance from source and parent if the neighboring vertex is smaller than what's already in the queue
                if neighbor in queue and queue[neighbor] > self.graph[vertex][neighbor]:
                    continue

                vertices[neighbor].dist_from_src = self.graph[vertex][neighbor]
                vertices[neighbor].parent = vertex
                queue[neighbor] = self.graph[vertex][neighbor]

        print(f"Maximum spanning tree: {mst}")
        print(f"Maximum spanning tree total weight: {mst_cost}")

    def DFS(self, visited, vertex):
        '''
        # 3.1 Applying one of the topology sorting strategies we discussed in class, please find a topological ordering of graph G3. 
        # I am going to use depth-first search.
        '''
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            for neighbor in graph[vertex]:
                self.DFS(visited=visited, vertex=neighbor)


# Test cases
# Problem 1
graph = {
        'A': {'B': 5, 'C': 3},
        'B': {'E': 1, 'F': 3, 'C': 2},
        'C': {'F': 7, 'D': 7},
        'D': {'A': 2, 'G': 6},
        'E': {'F': 2},
        'F': {'G': 1, 'D': 2},
        'G': {},
        }

graph_class = Graph(graph=graph)

# 1.1 singleSourceWeightedShortestPath
print("Testing singleSourceWeightedShortestPath...")
graph_class.singleSourceWeightedShortestPath(source='A')
print("\n")

# 1.2 singleSourceUnweightedShortestPath
print("Testing singleSourceUnweightedShortestPath...")
graph_class.singleSourceUnweightedShortestPath(source='B')
print("\n")


# Problem 2
graph = {
        'A': {'B': 3, 'E': 4, 'D': 4},
        'B': {'A': 3, 'E': 3, 'F': 2, 'C': 10},
        'C': {'B': 10, 'F': 6, 'G': 1},
        'D': {'A': 4, 'E': 5, 'H': 6},
        'E': {'D': 5, 'A': 4, 'B': 3, 'F': 11, 'I': 1, 'H': 2},
        'F': {'E': 11, 'B': 2, 'C': 6, 'G': 2, 'J': 11, 'I': 3},
        'G': {'C': 1, 'F': 2, 'J': 8},
        'H': {'D': 6, 'E': 2, 'I': 4},
        'I': {'H': 4, 'E': 1, 'F': 3, 'J': 7},
        'J': {'I': 7, 'F': 11, 'G': 8},
        }

graph_class = Graph(graph=graph)

# 2.1 minSpanningTree
print("Testing minSpanningTree...")
graph_class.minSpanningTree(source='A')
print("\n")

# 2.2 maxSpanningTree
print("Testing maxSpanningTree...")
graph_class.maxSpanningTree(source='A')
print("\n")

# Probelm 3
graph = {
        'A': ['B', 'F'],
        'B': ['C'],
        'C': ['H'],
        'D': ['A', 'E', 'I'],
        'E': ['A', 'F'],
        'F': ['C', 'G', 'K'],
        'G': ['C', 'H'],
        'H': [],
        'I': ['E', 'F', 'J'],
        'J': ['F', 'K'],
        'K': ['G', 'H'],
        }

graph_class = Graph(graph=graph)

# 3.1 DFS
print("Testing DFS...")
print("Depth-first search result:")
visited = set()
graph_class.DFS(visited=visited, vertex='D')
