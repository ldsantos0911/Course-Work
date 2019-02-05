Caltech CS2 Assignment 5: Graphs



Part 0: Debugging

This algorithm works for directed graphs which do not loop back on themselves.
However, if a loop is presented or if the graph is undirected, the algorithm
will run indefinitely. There is no way of checking if a node has already been
visited, and it is dependent on there being no loop or cycle for the search to
get caught in. A simple example is one node which points to two nodes, one of
which points directly back to the original node. Therefore, the function would
be called on the same nodes repeatedly. I would fix this by keeping track of
visited nodes (perhaps with an unordered map) and only visiting unvisited ones.


Part 1: Minimum Spanning Tree

The three most essential properties of an MST are that it contains all of the
vertices of a graph, contains a subset of the edges, and that the sum of its
edge weights is minimal. In terms of a graph, an MST connects each vertex in a
graph with the minimum total weight of the graph edges.

If we start with one node and are looking to add an adjacent one, we should add
the one with the minimum edge weight, which is not already in the tree, since the
overall objective is to create a tree with the minimum total edge weight.

The next node we pick should always be the one not in the current tree but which
is attached to a node currently in the tree with the minimum edge weight of all
possible edges adjacent to the tree. We know that we are finished when there
are no more possible edges to add.

At each step, we should pick the edge which connects two trees with the minimum
edge weight. This way, we construct the tree with minimum total edge weight in
small sections. We know we are finished when there is only one total tree, i.e.
when there are no mere nodes from separate trees to be added.


Part 2: Single-Source Shortest-Path

It makes sense to first investigate the neighbor that is closest in calculated
distance (not tentative).

It makes sense to, at each step, investigate the node which has current Shortest
distance from the start node and has not already been investigated. In addition
to investigating, we should set the previous attribute of nodes we visit to the
node we are investigating. Thus, if we investigate the node with the smallest
distance each time, we will eventually investigate the node with the smallest
distance which connects to the destination node. This will yield the shortest
possible path to the destination.

We know that we are done when the node being investigated is the end node. We
derive the path we want by using the previous attribute and drawing an edge
between each node and its previous node, starting at the destination and ending
at the start.
