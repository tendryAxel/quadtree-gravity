from quadtree import QuadTree, Vector2D


def main():
    tree = QuadTree(10)
    tree.add(Vector2D(1, 1), 1)
    print(tree._grid_str())
    tree.add(Vector2D(2, 1), 1)
    print(tree._grid_str())
    tree.add(Vector2D(1, 2), 1)
    print(tree._grid_str())
    tree.add(Vector2D(9, 9), 1)
    print(tree._grid_str())

if __name__ == "__main__":
    main()
