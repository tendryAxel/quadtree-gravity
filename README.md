# QuadTree

A simple implementation of a **QuadTree** designed specifically for computing gravitational forces in an **N-body simulation**.

This implementation is **not** intended to be a general-purpose spatial index. It exists solely to efficiently aggregate bodies and approximate gravitational interactions using a hierarchical spatial partitioning (Barnes–Hut style).

## Features

* QuadTree construction from simulation bodies.
* Mass and center-of-mass aggregation for each node.
* Efficient spatial subdivision for gravity calculations.
* Debug utilities for visualizing the tree structure.

## Scope

This project intentionally focuses on one use case:

* Computing gravitational forces in an N-body simulation.

It does **not** aim to provide generic QuadTree operations such as nearest-neighbor search, collision detection, range queries, or spatial indexing APIs.

## License

This project is provided as-is for educational and experimental purposes.
