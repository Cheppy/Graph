from dacg import ComputationGraph, compute


def connect_graph(graph: ComputationGraph, adj_list: list):
    for node, dependency_node in adj_list:
        if node not in graph.nodes.keys():
            raise ValueError(f"Node '{node}' not present in the graph {graph}.")
        graph.add_edge(node, dependency_node)


def main():
    graph = ComputationGraph()

    # COMPUTE EXAMPLES

    def compute_b(a):
        return a + 1

    def compute_c(a):
        return a * 2

    def compute_d(a, b, c):
        return a + b + c

    def compute_e(c, d):
        return c * d + 99

    ##
    graph.add_node('A', )
    graph.add_node('B', compute_b)
    graph.add_node('C', compute_c)
    graph.add_node('D', compute_d)
    graph.add_node('E', compute_e)

    adj_list = [
        ('B', 'A'),
        ('C', 'A'),
        ('D', 'A'),
        ('E', 'A'),
        ('D', 'B'),
        ('D', 'C'),
        ('E', 'C'),
        ('E', 'D'),
    ]

    connect_graph(graph, adj_list)

    inputs_outputs = [
        ({'A': 5}, ['D', 'E']),
        ({'A': 5, 'B': 10}, ['D']),
        ({'A': 5}, ['B']),
    ]

    for inputs, outputs in inputs_outputs:
        print(f"\nTest case: inputs={inputs}, outputs={outputs}")
        try:
            result = compute(graph, inputs, outputs)
            print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
