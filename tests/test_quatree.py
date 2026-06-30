from quadtree import QuadTree, Vector2D


def test_create_tree():
    tree = QuadTree(10)
    assert tree.size == 10
    tree.add(Vector2D(1, 1), 1)


def test_add_1_element():
    tree = QuadTree(10)
    position = Vector2D(1, 1)
    mass = 1

    tree.add(position, mass)
    
    assert len(tree.nodes) == 1
    
    first_node = tree.nodes[0]
    assert first_node is not None
    assert first_node.center_mass == position
    assert first_node.mass == mass


def test_add_2_element():
    tree = QuadTree(10)
    position = Vector2D(1, 1)
    other_position = Vector2D(9, 1)
    mass = 1

    tree.add(position, mass)
    tree.add(other_position, mass)
    
    assert len(tree.nodes) == 5
    
    first_node = tree.nodes[0]
    assert first_node is not None
    assert first_node.center_mass == (position + other_position) / 2
    assert first_node.mass == mass * 2

    null_nodes = tree.nodes[3], tree.nodes[4]
    assert all(null_node is None for null_node in null_nodes)

def test_populate_space_uniformly_three_levels():
    """
    Populate every cell of an 8x8 grid (3 subdivision levels).

    Every final quadrant should contain exactly one body.
    """
    tree = QuadTree(8)

    positions = [
        Vector2D(x + 0.5, y + 0.5)
        for y in range(8)
        for x in range(8)
    ]

    for p in positions:
        tree.add(p, 1)

    root = tree.nodes[0]

    assert root is not None
    assert root.mass == 64

    expected_center = Vector2D(4.0, 4.0)
    assert root.center_mass == expected_center

    # All inserted points should exist as leaves.
    leaves = [
        node
        for node in tree.nodes
        if node is not None and node.mass == 1
    ]

    assert len(leaves) == 64

def test_add_points_on_border():
    """
    Insert points located exactly on the borders of the simulation area.

    Border handling is a common source of off-by-one bugs.
    """
    tree = QuadTree(10)

    border_points = [
        Vector2D(0, 0),
        Vector2D(5, 0),
        Vector2D(10, 0),
        Vector2D(10, 5),
        Vector2D(10, 10),
        Vector2D(5, 10),
        Vector2D(0, 10),
        Vector2D(0, 5),
        Vector2D(0, 3),
        Vector2D(10, 7),
    ]

    for point in border_points:
        tree.add(point, 1)

    root = tree.nodes[0]

    assert root is not None
    assert root.mass == len(border_points)

    expected_center = sum(border_points[1:], border_points[0]) / len(border_points)
    assert root.center_mass == expected_center

    leaves = [
        node
        for node in tree.nodes
        if node is not None and node.mass == 1
    ]

    assert len(leaves) == len(border_points)

def test_add_very_close_points_recursive_split():
    tree = QuadTree(1024)

    p1 = Vector2D(100.0, 100.0)
    p2 = Vector2D(100.125, 100.125)

    tree.add(p1, 1)
    tree.add(p2, 1)

    root = tree.nodes[0]

    assert root is not None
    assert root.mass == 2
    assert root.center_mass == (p1 + p2) / 2

    expected_depth = 13
    expected_node_count = 1 + expected_depth * 4

    assert len(tree.nodes) == expected_node_count

    leaves = [
        node
        for node in tree.nodes
        if node is not None and node.mass == 1
    ]

    internal = [
        node
        for node in tree.nodes
        if node is not None and node.mass == 2
    ]

    empty = [node for node in tree.nodes if node is None]

    assert len(leaves) == 2
    assert len(internal) == expected_depth
    assert len(empty) == expected_node_count - len(leaves) - len(internal)
    assert len(empty) == 38

    assert len(leaves) == 2
    assert leaves[0].center_mass == p1
    assert leaves[1].center_mass == p2
