import pytest
from dacg import ComputationGraph, compute


@pytest.fixture
def sample_graph():
    """Create a sample computation graph for testing"""
    graph = ComputationGraph()

    # Define computation functions
    def compute_b(a): return a + 1

    def compute_c(a): return a * 2

    def compute_d(a, b, c): return a + b + c

    def compute_e(c, d): return c * d

    # Add nodes
    graph.add_node('A')  # Input node
    graph.add_node('B', compute_b)
    graph.add_node('C', compute_c)
    graph.add_node('D', compute_d)
    graph.add_node('E', compute_e)

    # Add dependencies
    dependencies = [
        ('B', 'A'),  # B depends on A
        ('C', 'A'),  # C depends on A
        ('D', 'A'),  # D depends on A
        ('D', 'B'),  # D depends on B
        ('D', 'C'),  # D depends on C
        ('E', 'C'),  # E depends on C
        ('E', 'D'),  # E depends on D
    ]

    for node, dependency_node in dependencies:
        graph.add_edge(node, dependency_node)

    return graph


@pytest.mark.computation
def test_simple_computation(sample_graph):
    """Test computing a single node with one dependency"""
    inputs = {'A': 5}
    outputs = ['B']
    result = compute(sample_graph, inputs, outputs)
    assert result == {'B': 6}  # B = A + 1


@pytest.mark.computation
def test_multiple_dependencies(sample_graph):
    """Test computing a node with multiple dependencies"""
    inputs = {'A': 5}
    outputs = ['D']
    result = compute(sample_graph, inputs, outputs)
    # D = A + B + C = 5 + 6 + 10 = 21
    assert result == {'D': 21}


@pytest.mark.computation
def test_multiple_outputs(sample_graph):
    """Test computing multiple output nodes"""
    inputs = {'A': 5}
    outputs = ['D', 'E']
    result = compute(sample_graph, inputs, outputs)
    # D = A + B + C = 5 + 6 + 10 = 21
    # E = C * D = 10 * 21 = 210
    assert result == {'D': 21, 'E': 210}


@pytest.mark.computation
def test_use_provided_value(sample_graph):
    """Test that provided values are used instead of computing them"""
    inputs = {'A': 5, 'B': 10}
    outputs = ['D']
    result = compute(sample_graph, inputs, outputs)
    # D = A + B + C = 5 + 10 + 10 = 25
    assert result == {'D': 25}


@pytest.mark.error_handling
def test_insufficient_inputs(sample_graph):
    """Test that computation fails when inputs are insufficient"""
    inputs = {'B': 1}
    outputs = ['D']
    with pytest.raises(ValueError, match="No input value provided for A"):
        compute(sample_graph, inputs, outputs)


@pytest.mark.computation
def test_compute_only_needed(sample_graph):
    """Test that only needed values are computed"""
    inputs = {'A': 5}
    outputs = ['B']
    result = compute(sample_graph, inputs, outputs)
    # Only B should be computed, C, D, E should not be computed
    assert result == {'B': 6}
    assert len(result) == 1


@pytest.mark.error_handling
@pytest.mark.parametrize("inputs,outputs,error_msg", [
    ({'X': 5}, ['B'], "Input node X does not exist"),
    ({'A': 5}, ['X'], "Output node X does not exist"),
])
def test_nonexistent_nodes(sample_graph, inputs, outputs, error_msg):
    """Test handling of nonexistent nodes"""
    with pytest.raises(ValueError, match=error_msg):
        compute(sample_graph, inputs, outputs)


@pytest.mark.computation
@pytest.mark.parametrize("inputs,outputs,expected", [
    ({}, [], {}),
    ({'A': 5}, ['B'], {'B': 6}),
    ({'A': 5}, ['C'], {'C': 10}),
    ({'A': 5}, ['D'], {'D': 21}),
])
def test_various_computations(sample_graph, inputs, outputs, expected):
    """Test various computation scenarios"""
    result = compute(sample_graph, inputs, outputs)
    assert result == expected


@pytest.mark.error_handling
def test_empty_inputs_outputs():
    """Test handling of empty inputs and outputs"""
    graph = ComputationGraph()
    result = compute(graph, {}, [])
    assert result == {}