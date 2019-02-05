/**
 * @file
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2018
 * @copyright This code is in the public domain.
 *
 * @brief The MST and Shortest Path algorithms
 * (implementation).
 *
 */
#include "GraphAlgorithms.hpp"
#define INFTY 50000000

/**
 * TO STUDENTS: In all of the following functions, feel free to change the
 * function arguments and/or write helper functions as you see fit. Remember to
 * add the function header to GraphAlgorithms.hpp if you write a helper
 * function!
 *
 */

/**
 *
 * @brief Builds the MST of the given graph with Prim's algorithm
 *
 * @param g 	Graph object containing vector of nodes and edges
 * 				Definition for struct Graph in structs.hpp
 * @param app	Graphics application class
 * 				Class definition in GraphApp.hpp
 * 				You should not need to use this class other than passing app
 * 				as a parameter to drawEdge
 *
 * @attention 	Some hints for implementation and how to interact with our code
 * 				onMST and notOnMST are two vectors defined in
 *				GraphAlgorithms.hpp
 * 				that you can use to store which nodes are both in/not in the
 * 				MST. These are cleared at the start of the MST computation for
 * 				you. To access the nodes that a specific node connects to
 *				you, you can use the vector<Node *> edges which is part
 *				of the Node struct in structs.hpp
 * 				You can compare two nodes to see if they are the same by
 * 				comparing the id attribute of a Node.
 *				You can calculate distance from one node to another by calling
 * 				the double distance(Node a) function of the Node struct.
 * 				Whenever you decide to add an edge between two nodes
 *				to the MST, you can use the provided drawEdge function
 *				in GraphAlgorithms.cpp
 *
 * You can assume that the graph is completely connected. Also, we only use
 * existing edges for the MST.
 *
 * Add all Nodes but first one to notOnMST
 * Add first Node to onMST
 * WHILE size of MST < total # of nodes:
 *    min = INFTY
 *    FOR j = 0, j less than size of MST, j++:
 *        FOR k = 0, k < # of edges attached to current Node, k++:
 *            IF edges[k] of onMST[j] is not on MST:
 *                IF onMST[j] distance to edges[k] < min:
 *                    min = onMST[j] distance to edges[k]
 *                    min_key = edges[k] id
 *                    min_ind = j
 *    drawEdge between onMST[min_ind] and notOnMST[min_key]
 *    add notOnMST[min_key] to onMST
 *    remove notOnMST[min_key] from notOnMST
 *
 */

void buildMSTPrim(Graph g, GraphApp *app) {
    onMST.erase(onMST.begin(), onMST.end());
    notOnMST.erase(notOnMST.begin(), notOnMST.end());
    int min, min_key, min_ind;
    for(unsigned int i = 1; i < g.nodes.size(); i++)
    {
        notOnMST[g.nodes[i]->id] = g.nodes[i];
    }
    onMST.push_back(g.nodes[0]);
    while(onMST.size() != g.nodes.size())
    {
        min = INFTY;
        for(unsigned int j = 0; j < onMST.size(); j++)
        {
            for(unsigned int k = 0; k < onMST[j]->edges.size(); k++)
            {
                if(notOnMST.count(onMST[j]->edges[k]->id) > 0)
                {
                    if(onMST[j]->distance(*(onMST[j]->edges[k])) < min)
                    {
                        min = onMST[j]->distance(*(onMST[j]->edges[k]));
                        min_key = onMST[j]->edges[k]->id;
                        min_ind = j;
                    }
                }
            }
        }
        drawEdge(onMST[min_ind], notOnMST[min_key], g.edges, app, true);
        onMST.push_back(notOnMST[min_key]);
        notOnMST.erase(min_key);
    }
}

/**
 *
 * @brief Builds the MST of the given graph with Kruskal's algorithm
 *
 * @param g 	Graph object containing vector of nodes and edges
 * 				Definition for struct Graph in structs.hpp
 * @param app	Graphics application class
 * 				Class definition in GraphApp.hpp
 * 				You should not need to use this class other than
 *passing app
 * 				as a parameter to drawEdge
 *
 * @attention 	Some hints for implementation and how to interact with our code
 * 				You'll want to use a priority queue to determine which edges
 * 				to add first. We've created the priority queue for you
 * 				along with the compare function it uses. All you need to do
 * 				is call edge_queue.top(), edge_queue.pop(), edge_queue.push()
 * 				The data type that this priority queue stores, KruskalEdge
 *              is defined in GraphAlgorithms.hpp and is an edge between
 *              any two trees. Each Node has a kruskal_edges attribute to store
 *              all the nodes it connects to in the MST. Make sure to use this
 *				to be able to join trees later!
 * 				To know which tree a node is in, use the which_tree attribute.
 * 				You can still use the edges, distance, and id
 *				attributes of a Node.
 * 				When connecting trees, you can call the
 *				kruskalFloodFill function
 * 				defined in structs.hpp on a node to convert it and its
 * 				MST connected nodes to a different tree number recursively.
 *				As in Prim's algorith, call drawEdge to add a connection between
 * 				two nodes to the MST
 *
 * You can assume that the graph is completely connected. Also, we only use
 * existing edges for the MST.
 *
 * tree_edges = 0
 * Set all Nodes' which_tree attribute to different numbers
 * FOR edge in all edges in the graph:
 *    temp_k = new KruskalEdge
 *    Set endpoints of temp_k to endpoints of edge
 *    Set weight of temp_k to weight of edge
 *    push temp_k to edge_queue
 * WHILE tree_edges < total # of nodes - 1:
 *    Set next_edge to top of edge_queue
 *    pop from edge_queue
 *    IF u and v of edge_queue are in different trees:
 *        make u's tree part of v's tree
 *        add v and u to each other's set of kruskal_edges
 *        increment tree_edges
 *        drawEdge between u and v
 * clean up edge_queue
 *
 */
void buildMSTKruskal(Graph g, GraphApp *app) {
    auto compare_func = [](KruskalEdge *a, KruskalEdge *b) {
        return (a->weight > b->weight);
    };
    std::priority_queue<KruskalEdge *, std::vector<KruskalEdge *>,
                        decltype(compare_func)>
        edge_queue(compare_func);
    unsigned int tree_edges = 0;
    KruskalEdge * next_edge;
    for(unsigned int i = 0; i < g.nodes.size(); i++)
    {
        g.nodes[i]->which_tree = i;
    }
    for(Edge * temp : g.edges)
    {
        KruskalEdge * temp_k = new KruskalEdge;
        temp_k->u = temp->a;
        temp_k->v = temp->b;
        temp_k->weight = temp->weight;
        edge_queue.push(temp_k);
    }

    while(tree_edges < g.nodes.size() - 1)
    {
        next_edge = edge_queue.top();
        if(next_edge->u->which_tree != next_edge->v->which_tree)
        {
            next_edge->u->kruskalFloodFill(next_edge->v->which_tree);
            next_edge->u->kruskal_edges.push_back(next_edge->v);
            next_edge->v->kruskal_edges.push_back(next_edge->u);
            tree_edges++;
            drawEdge(next_edge->u, next_edge->v, g.edges, app, true);
        }
        edge_queue.pop();
        delete next_edge;
    }

    for(Node * n : g.nodes)
    {
        n->kruskal_edges.clear();
    }

    while(!edge_queue.empty())
    {
        next_edge = edge_queue.top();
        edge_queue.pop();
        delete next_edge;
    }

}

/**
 *
 * @brief Find the shortest path between start and end nodes with Djikstra's
 * 		  shortest path algorithm
 *
 * @param start	Index of start node of path to find
 * 				Can access the Node * element by using
 *				g.nodes[start]
 * @param end	Index of end node of path to find
 * 				Can access the Node * element by using g.nodes[end]
 * @param g 	Graph object containing vector of nodes and edges
 * 				Definition for struct Graph in structs.hpp
 * @param app	Graphics application class
 * 				Class definition in GraphApp.hpp
 * 				You should not need to use this class other than passing app
 * 				as a parameter to drawEdge
 *
 * @attention 	Some hints for implementation and how to interact with our code
 * 				You can use the distance_to_start attribute of the Node struct
 * 				in structs.hpp to keep track of what the distance from each
 * 				Node to the start node during computation
 * 				You can use the previous attribute of the Node struct
 *				in structs.hpp to keep track of the path you are taking to
 *				later backtrack.
 *				To access the nodes that a specific node connects to you, you
 * 				can use the vector<Node *> edges which is part of the Node struct
 * 				in structs.hpp
 *				Whenever you decide to add an edge between two nodes
 *				to the MST, you can use the provided drawEdge function in
 *				GraphAlgorithms.cpp
 *
 * Set all Nodes distance_to_start = INFTY
 * Set start Node distance_to_start to 0
 * Set start Node's previous to NULL
 * WHILE current is not end:
 *    Mark current as visited
 *    FOR edge in current Node's edges:
 *        IF edge's distance_to_start > current distance_to_start + distance
 *              between edge and start:
 *              set edge's previous to current
 *              set edge's distance_to_start to current_dist + destance between
 *              edge and start
 *    current_dist = INFTY
 *    FOR temp in all Nodes:
 *        IF temp distance_to_start < current_dist AND temp is unvisited:
 *            current = temp;
 *            current_dist = temp distance_to_start
 * WHILE previous is not NULL
 *    drawEdge between current and previous
 *    current = previous
 *
 */
void findShortestPath(int start, int end, Graph g, GraphApp *app) {
    unordered_map<int, Node*> visited;
    Node * current = g.nodes[start];
    int current_dist = 0;
    for(unsigned int i = 0; i < g.nodes.size(); i++)
    {
        g.nodes[i]->distance_to_start = INFTY;
    }
    g.nodes[start]->distance_to_start = 0;
    g.nodes[start]->previous = nullptr;
    while(current != g.nodes[end])
    {
        visited[current->id] = current;
        for(Node * edge : current->edges)
        {
            if(edge->distance_to_start > current_dist + current->distance(*edge)\
              && visited.count(edge->id) == 0)
            {
                edge->previous = current;
                edge->distance_to_start = current_dist + current->distance(*edge);
            }
        }
        current_dist = INFTY;
        for(Node * temp : g.nodes)
        {
            if(temp->distance_to_start < current_dist && visited.count(temp->id) == 0)
            {
                current = temp;
                current_dist = temp->distance_to_start;
            }
        }
    }
    while(current->previous != nullptr)
    {
        drawEdge(current, current->previous, g.edges, app, false);
        current = current->previous;
    }

}

/**
 * @brief Adds an edge to either the MST or the shortest path based on the
 * 			nodes to connect given. This is done by iterating through the edges
 * 			to find the correct edge given the nodes.
 *
 * @param pt1	One side of edge to draw
 * @param pt2	Other side of edge to draw
 * @param edges	Vector of edges in the graph
 * @param app	Graphics application class
 * @param mst	True if we are adding edge to MST, False if we are adding edge
 * 				to shortest path
 **/

void drawEdge(Node *pt1, Node *pt2, vector<Edge *> edges, GraphApp *app,
              bool mst) {
    for (unsigned int i = 0; i < edges.size(); i++) {
        if ((edges[i]->a == pt1 && edges[i]->b == pt2) ||
            (edges[i]->a == pt2 && edges[i]->b == pt1)) {
            if (mst)
                app->add_to_mst(edges[i]);
            else
                app->add_to_path(edges[i]);
            break;
        }
    }
    return;
}
