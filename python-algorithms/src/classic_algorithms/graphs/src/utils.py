from graph_list import Graph
from copy import copy
from union_find import UnionFind
import heapq


def is_graph_connected(graph):
    return len(list(graph.breadth_first_search())) == graph.count_vertices()


def is_bipartite(graph):
    parts = {0: [], 1: []}
    visited_vertices = set()
    colors = {}
    start_vertex = graph.get_start_vertex()
    queue = [start_vertex]
    proper_color = {start_vertex: 0}
    while len(queue) > 0:
        vertex = queue.pop(0)
        current_color = proper_color[vertex]
        colors[vertex] = current_color
        parts[current_color].append(vertex)
        visited_vertices.add(vertex)
        for adjacent_vertex in graph.get_vertex_environment(vertex):
            if adjacent_vertex in visited_vertices and colors[vertex] == colors[adjacent_vertex]:
                return False, []
            elif adjacent_vertex not in visited_vertices and adjacent_vertex not in queue:
                queue.append(adjacent_vertex)
                proper_color[adjacent_vertex] = not current_color
    return True, [parts[1], parts[0]]


def prim(graph):
    total_cost = 0
    min_cost_tree = Graph()
    start_vertex = graph.get_start_vertex()
    vertices_queue = [(0, (start_vertex, start_vertex))]
    while vertices_queue:
        cost, (vertex, orig_vertex) = heapq.heappop(vertices_queue)
        if vertex not in min_cost_tree:
            total_cost += cost
            min_cost_tree.add_edge(vertex, orig_vertex)
            for adjacent_vertex in graph.get_vertex_environment(vertex):
                if adjacent_vertex not in min_cost_tree:
                    heapq.heappush(vertices_queue,
                                   (graph.get_edge_cost((vertex, adjacent_vertex)),
                                   (adjacent_vertex, vertex)))
    return total_cost, min_cost_tree


def kruskal(graph):
    total_cost = 0
    min_cost_tree = Graph()
    connected_components = UnionFind(graph.get_all_vertices())
    edges_queue = graph.get_all_edges()
    heapq.heapify(edges_queue)
    while edges_queue:
        cost, edge = heapq.heappop(edges_queue)
        if is_valid_edge(edge, min_cost_tree, connected_components):
            total_cost += cost
            min_cost_tree.add_edge(edge[0], edge[1], cost)
            connected_components.union(edge[0], edge[1])
    return total_cost, min_cost_tree


def is_valid_edge(edge, graph, components):
    if graph.is_edge_in_graph(edge) or components.find(edge[0]) == components.find(edge[1]):
        return False
    return True


def is_acyclic_graph(graph):
    if graph.count_vertices() <= 2:
        return True
    visited_vertices = set()
    vertices = list(graph.get_all_vertices())
    colors = {}
    previous_vertex = vertices[0]

    def is_acyclic_graph_helper(vertex):
        nonlocal previous_vertex
        colors[vertex] = True
        visited_vertices.add(vertex)
        for adjacent_vertex in graph.get_vertex_environment(vertex):
            if adjacent_vertex not in visited_vertices:
                previous_vertex = vertex
                return is_acyclic_graph_helper(adjacent_vertex)
            elif adjacent_vertex != previous_vertex and colors.get(adjacent_vertex):
                return False
        colors[vertex] = False
        return True

    return is_acyclic_graph_helper(vertices[0])


def find_euler_cycle(graph, start_vertex=None):
    if not _euler_cycle_exist(graph) or graph.count_vertices() == 0:
        return None
    copy_graph = copy(graph)
    start_vertex = start_vertex or graph.get_start_vertex()

    def find_euler_cycle_helper(vertex):
        euler_cycle = []
        stack = [vertex]
        while len(stack) > 0:
            peek_vertex = stack.pop()
            euler_cycle.append(peek_vertex)
            if copy_graph.get_vertex_degree(peek_vertex) > 0:
                peek_environment = copy_graph.get_vertex_environment(peek_vertex)
                next_vertex = peek_environment[0]
                copy_graph.remove_edge(peek_vertex, next_vertex)
                stack.append(next_vertex)
            else:
                for vertex in euler_cycle[1:]:
                    if copy_graph.get_vertex_degree(vertex) != 0:
                        euler_cycle = euler_cycle[0:1] + find_euler_cycle_helper(vertex) + euler_cycle[2:]
        return euler_cycle

    return find_euler_cycle_helper(start_vertex)


def _euler_cycle_exist(graph):
    return all(map(lambda vertex: graph.get_vertex_degree(vertex) % 2 == 0, graph.get_all_vertices()))


def _find_vertex_to_color_dsatur(graph, not_colored_vertices, adjacent_vertices_colors):
    vertex_to_color = next(iter(not_colored_vertices))
    for vertex in not_colored_vertices:
        greater_saturation = len(adjacent_vertices_colors[vertex]) > len(adjacent_vertices_colors[vertex_to_color])
        equal_saturation = len(adjacent_vertices_colors[vertex]) == len(adjacent_vertices_colors[vertex_to_color])
        greater_degree = graph.get_vertex_degree(vertex) > graph.get_vertex_degree(vertex_to_color)
        if greater_saturation or equal_saturation and greater_degree:
            vertex_to_color = vertex
    return vertex_to_color


def dsatur(graph):
    not_colored_vertices = set(graph.get_all_vertices())
    vertices_colors = {}
    adjacent_vertices_colors = {vertex: set() for vertex in not_colored_vertices}
    used_colors_length = 1
    while len(not_colored_vertices) != 0:
        vertex_to_color = _find_vertex_to_color_dsatur(graph, not_colored_vertices, adjacent_vertices_colors)
        color = min(set(range(used_colors_length + 1)) - adjacent_vertices_colors[vertex_to_color])
        used_colors_length = max(used_colors_length, color + 1)
        vertices_colors[vertex_to_color] = color
        not_colored_vertices.remove(vertex_to_color)
        for adjacent_vertex in graph.get_vertex_environment(vertex_to_color):
            adjacent_vertices_colors[adjacent_vertex].add(color)
    return vertices_colors, used_colors_length


def _get_potential_vertices_gis(not_colored_vertices, adjacent_vertices_colors, color):
    vertices = []
    for vertex in not_colored_vertices:
        if color not in adjacent_vertices_colors[vertex]:
            vertices.append(vertex)
    return vertices


def gis(graph):
    not_colored_vertices = set(graph.get_all_vertices())
    adjacent_vertices_colors = {vertex: set() for vertex in not_colored_vertices}
    last_color = 0
    vertices_colors = {}
    copy_graph = copy(graph)
    while len(not_colored_vertices) != 0:
        vertices = _get_potential_vertices_gis(not_colored_vertices, adjacent_vertices_colors, last_color)
        vertices_count = [(v, len(copy_graph.get_vertex_environment(v))) for v in vertices]
        for vertex, _ in sorted(vertices_count, key=lambda item: item[1]):
            if last_color not in adjacent_vertices_colors[vertex]:
                vertices_colors[vertex] = last_color
                not_colored_vertices.remove(vertex)
                for adjacent_vertex in copy_graph.get_vertex_environment(vertex).copy():
                    adjacent_vertices_colors[adjacent_vertex].add(last_color)
                    copy_graph.remove_edge(adjacent_vertex, vertex)
        last_color += 1
    return vertices_colors, last_color


def djkstra(graph, start_vertex, target_vertex):
    queue = [(0, [start_vertex])]
    marked_vertices = set()
    while queue:
        current_cost_path = heapq.heappop(queue)
        last_vertex = current_cost_path[1][-1]
        if last_vertex == target_vertex:
            return current_cost_path
        marked_vertices.add(last_vertex)
        not_marked_vertices = set(graph.get_vertex_environment(last_vertex)) - marked_vertices
        for vertex in not_marked_vertices:
            edge_cost = graph.get_edge_cost((last_vertex, vertex))
            heapq.heappush(queue, (current_cost_path[0] + edge_cost, current_cost_path[1] + [vertex]))
    return None


def tsp(graph: Graph):
    if len(graph) <= 3:
        return list(graph.get_all_vertices())
    best_cycle = list(graph.get_all_vertices())
    best_cycle_weight = graph.cycle_weight(best_cycle)
    i = 1
    improvement = True
    while improvement and i < len(graph):
        improvement = False
        current_cycle = best_cycle[:]
        for j in range(i + 2, len(graph) + i - 1):
            current_cycle[i], current_cycle[j % len(graph)] = current_cycle[j % len(graph)], current_cycle[i]
            if (new_length := graph.cycle_weight(current_cycle)) < best_cycle_weight:
                best_cycle = current_cycle[:]
                best_cycle_weight = new_length
                improvement = True
            current_cycle[j % len(graph)], current_cycle[i] = current_cycle[i], current_cycle[j % len(graph)]
        i += 1
    return best_cycle
