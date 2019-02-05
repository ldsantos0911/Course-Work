/**
 * @file structs.hpp
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2018
 * @copyright This code is in the public domain.
 *
 * @brief Structs for representing Nodes, Edges, and Graphs
 */
#pragma once
#include <cmath>
#include <iostream>

using namespace std;


/**
 * @brief Struct representing the Nodes of a graph.
 *
 * The Node struct is a representation of a point in the (Euclidean)
 * 2-D plane which is part of a graph. The struct provides functionalities such
 * as calculate distance and combining Kruskal trees.
 *
 * Contains member variables for use in MST and Shortest Path calculations
 */
struct Node
{
    /**
     * @brief Represents the x-coordinate of the point
     */
    int x;

    /**
     * @brief Represents the y-coordinate of the point
     */
    int y;

    /**
     * @brief node id
     */
    int id;

    /**
     * @brief Initializes the struct
     *
     * @param id: first argument representing the id of node
     * @param x:  second argument representing the x-coordinate
     * @param y:  third argument representing the y-coordinate
     */
    Node(int id_, int x_, int y_)
        : x(x_)
        , y(y_)
        , id(id_)
    {}

	/**
	 * @brief Calculates distance from this node to another node
	 *
	 * @param a: Node to calculate distance to
	 * @return : Cartesian distance between two nodes in plane
	 */
    double distance (Node a) {
        return sqrt((x - a.x)*(x - a.x) + (y - a.y)*(y - a.y));
    }

    /**
     * @brief Change all nodes in a Kruskal tree to become part of
     * another Kruskal tree. Does this recursively by calling the
     * function on each of the connected nodes it has a Kruskal edge to
     *
     * @param new_tree_id: id of tree to change this node and its
     * 						connected nodes to
     */
    void kruskalFloodFill(int new_tree_id) {
		this->which_tree = new_tree_id;
		for (unsigned int i = 0; i < this->kruskal_edges.size(); i++) {
			Node *other = kruskal_edges[i];
			if (other->which_tree != new_tree_id) {
				other->kruskalFloodFill(new_tree_id);
			}
		}
	}

	/**
	 * @brief Adjacency list of all nodes that this node is connected
	 * 			through
	 */
    std::vector<Node *> edges;

    // extra variables for algorithms
    /**
	 * @brief Edges that a node is connected to within a Kruskal tree
	 * 		   Should be a subset of edges vector
	 */
	std::vector<Node *> kruskal_edges;

    /**
     * @brief For shortest path computation. Used to later backtrack and
     * 		  find path
     */
    Node * previous;

    /**
     * @brief For shortest path computation. Stores the distance from each
     * 		  node to the start node at each point in computation
     */
    double distance_to_start;

    /**
     * @brief For Kruskal's algorithm. Stores which of the Kruskal trees
     * 		  this node is in (trees are numbered from 0 to NPOINTS - 1)
     */
    int which_tree;
};

/**
 * @brief Struct representing the Edges of a graph.
 *
 * The Edge struct is a representation of an edge between two points
 * in the 2-D plane which is part of a graph.
 */
struct Edge
{
	/**
	 * @brief Stores references to the two nodes connected by the edge
	 */
    Node *a;
    Node *b;

    /**
     * @brief Stores id of an edge for uniqueness
     */
    int id;

	/**
	 * @brief Weight of an edge. In this case, we use the length of
	 * 	      the edge as the weight
	 */
    double weight;

	/**
     * @brief Initializes the struct
     *
     * @param id:     first argument representing the id of edge
     * @param a:      second argument representing the first node
     * @param b:      third argument representing the second node
     * @param weight: fourth argument representing weight of edge
     */
    Edge(int id_, Node *a_, Node *b_, double weight_)
        : a(a_)
        , b(b_)
        , id(id_)
        , weight(weight_)
    {}

};

/**
 * @brief Struct representing a graph.
 *
 * The Graph struct is a representation of a graph in the 2-D plane
 */
struct Graph
{
	/**
	 * @brief Nodes within a graph
	 */
    vector<Node *> nodes;

    /**
     * @brief Edges within a graph
     */
    vector<Edge *> edges;

    /**
     * @brief Initializes the struct
     *
     * @param nodes:  first argument representing the nodes of a graph
     * @param edges:  second argument representing the edges of a graph
     */
    Graph(vector<Node *> nodes_, vector<Edge *> edges_)
        : nodes(nodes_)
        , edges(edges_)
    {}
};
