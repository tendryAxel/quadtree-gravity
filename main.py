import random
from quadtree import QuadTree, Vector2D


def main():
    tree = QuadTree(10)
    for i in range(100_000):
        tree.add(Vector2D(random.random() * 10, random.random() * 10), 1)

if __name__ == "__main__":
    main()
