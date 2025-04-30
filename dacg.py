
class Node:
    def __init__(self, name: str, computation_fn):
        self._name = name
        self._computation_fn = computation_fn

    @property
    def name(self) -> str:
        """
        Get the node name
        Returns: node name (str)

        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """

        Set the node name

        Args:
            value (str):  node name

        Returns: None

        """
        if not isinstance(value, str):
            raise ValueError("Node name must be a string")
        self._name = value

    @property
    def computation_fn(self):
        """

        Get the computation function

        Returns: computational function (object)

        """
        return self._computation_fn

    @computation_fn.setter
    def computation_fn(self, value):
        """
        Set the computation function

        Args:
            value (str):

        Returns:

        """

        if value is not None and not callable(value):
            raise ValueError("Computation function must be callable or None")
        self._computation_fn = value

    def compute(self, *args: object) -> object:
        """Execute the computation function with given arguments"""
        if not self._computation_fn:
            raise ValueError(f"Node {self._name} has no computation function")
        return self._computation_fn(*args)

    def __str__(self) -> str:
        return f"Node({self._name})"


class ComputationGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, list[str]] = {}

    @property
    def nodes(self) -> dict[str, Node]:
        """
        Returns: the nodes dictionary

        """
        return self._nodes.copy()

    @property
    def edges(self) -> dict[str, list[str]]:
        """

        Returns:the edges  dictionary

        """
        return {k: v.copy() for k, v in self._edges.items()}

    def add_node(self, name: str, computation_fn=None) -> Node:
        """

        Add a new node to the graph with optional computation function

        Args:
            name (str):
            computation_fn (object):
        Returns:  dict: node that is  added

        """
        if name not in self._nodes:
            self._nodes[name] = Node(name, computation_fn)
            self._edges[name] = []
        return self._nodes[name]

    def add_edge(self, node_name: str, dependency_name: str) -> None:
        """
        Add a dependency edge between two nodes

        Args:
            node_name (str):
            dependency_name (str):

        Returns: None

        """
        if node_name not in self._nodes or dependency_name not in self._nodes:
            raise ValueError("Both nodes must exist in the graph")
        if dependency_name not in self._edges[node_name]:
            self._edges[node_name].append(dependency_name)

    def get_edges(self, node_name: str) -> list[str]:
        """

        Get list of edges names for a node

        Args:
            node_name (str):

        Returns:  List[str]  of edges for specific node

        """
        return self._edges.get(node_name, []).copy()

    def get_node(self, name: str) -> Node | None:
        """Get a node by name"""
        return self._nodes.get(name)

    def get_dependent_nodes(self, node_name: str) -> list[str]:
        dependents: list[str] = []
        for node, deps in self._edges.items():
            if node_name in deps:
                dependents.append(node)
        return dependents

    def __str__(self) -> str:

        result: list[str] = []
        for node_name, node in self._nodes.items():
            deps = self._edges[node_name]
            result.append(f"Node({node_name}, deps={deps})")
        return "\n".join(result)


def compute(graph: ComputationGraph, inputs: dict[str, object], outputs: list[str]) -> dict[str, object]:
    """

    Args:
        graph: The computation graph
        inputs: Dictionary mapping node names to their input values
        outputs: List of node names

    Returns:
        dict: Dictionary mapping requested output nodes to their computed values

    Raises:
        ValueError: If inputs are insufficient to compute any of the outputs
    """
    # Validate inputs and outputs
    for node_name in inputs:
        if node_name not in graph.nodes:
            raise ValueError(f"Input node {node_name} does not exist in graph")

    for node_name in outputs:
        if node_name not in graph.nodes:
            raise ValueError(f"Output node {node_name} does not exist in graph")

    computed: dict[str, object] = inputs.copy()
    visited: set[str] = set()

    def dfs(node_name_: str) -> object:
        """
            Compute Node value  using depth-first search.

        Args:
            node_name_(str):
        Returns:
            dict: The computed value of the node.



        """
        if node_name_ in computed:
            return computed[node_name_]

        if node_name_ in visited:
            raise ValueError(f"Cycle detected in  graph at node {node_name_}")
        visited.add(node_name_)

        node = graph.get_node(node_name_)
        edges: list[object] = []
        for dep in graph.get_edges(node_name_):
            try:
                edges.append(dfs(dep))
            except ValueError as e:
                raise ValueError(f"Can't compute {node_name_}: {str(e)}")
        try:
            value = node.compute(*edges)
            computed[node_name_] = value
            visited.remove(node_name_)
            return value
        except ValueError:
            raise ValueError(f"No input value provided for {node_name_} and it has no computation function")

    return {output: dfs(output) for output in outputs}
