class Graph:

    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if self.adjacency_list.get(vertex) is not None:
            raise Exception('Such vertex already exist!')
        self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        self.adjacency_list[vertex1] = (self.adjacency_list.get(vertex1) or []) + [vertex2]
        self.adjacency_list[vertex2] = (self.adjacency_list.get(vertex2) or []) + [vertex1]

    def remove_edge(self, vertex1, vertex2):
        list1, list2 = self.adjacency_list.get(vertex1), self.adjacency_list.get(vertex2)
        if list1 is None or list2 is None:
            raise Exception('There is no such edge!')
        index1, index2 = list1.index(vertex2), list2.index(vertex1)
        if index1 == -1 or index2 == -1:
            raise Exception('There is no such edge!')
        list1.pop(index1)
        list2.pop(index2)

    def get_all_vertexes(self):
        return self.adjacency_list.keys()

    def get_vertex_environment(self, vertex):
        return self.adjacency_list.get(vertex)

    def is_adjacent_vertexes(self, vertex1, vertex2):
        vertex1_environment = self.get_vertex_environment(vertex1)
        if vertex1_environment is None:
            return False
        return vertex2 in vertex1_environment


if __name__ == '__main__':
    graph = Graph()
    graph.add_vertex(5)
    graph.add_vertex(1)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    print(graph.adjacency_list)
    graph.remove_edge(4, 3)
    print(graph.adjacency_list)
