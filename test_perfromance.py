import random
from quadtree import QuadTree, Vector2D
from timeit import Timer
import matplotlib.pyplot as plt


def insertion_test(tree: QuadTree) -> None:
    tree.add(Vector2D(random.random() * tree.size, random.random() * tree.size), 1)

if __name__ == "__main__":
    tree = QuadTree(10)
    timer = Timer(lambda: insertion_test(tree))

    repeat, number = 10, 100_000
    times = timer.repeat(repeat=repeat, number=number)

    print(f"Runs         : {repeat} × {number}")
    print(f"Best         : {min(times):.6f} s")
    print(f"Average/run  : {min(times) / 10 * 1e3:.3f} ms")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        times,
        marker="o",
        linewidth=2,
        markersize=5,
    )

    ax.set_title("Execution Time per Repeat")
    ax.set_xlabel("Repeat")
    ax.set_ylabel("Time (s)")

    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()
