/* debugging example */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <assert.h>
using namespace std;

class Node
{
    int value;
    int id;
    std::vector<Node*> edges;
public:
    void add_edge(Node * edge)
    {
        this->edges.push_back(edge);
    }
    Node(int value)
    {
        this->value = value;
    }
    bool dfs(int to_find, unordered_map<int, Node*> &visited);
};

// true indicates that the value was found, and false indicates that the value was not found.
bool Node::dfs(int to_find, unordered_map<int, Node*> &visited)
{
    if(this->value == to_find)
    {
        return true;
    }
    std::vector<Node*>::iterator i;
    for(i = this->edges.begin(); i != this->edges.end(); i++)
    {
        if(visited.count((*i)->id) > 0)
        {
            continue;
        }
        Node * n = *i;
        visited[n->id] = n;
        bool r = n->dfs(to_find, visited);
        if(r)
        {
            visited.clear();
            return r;
        }
    }
    visited.clear();
    return false;
}

int main(void)
{
    Node *node_1 = new Node(2), *node_2 = new Node(4), *node_3 = new Node(6), \
    *node_4 = new Node(8);
    unordered_map<int, Node*> visited;
    node_1->add_edge(node_2);
    node_1->add_edge(node_3);
    node_1->add_edge(node_4);
    node_2->add_edge(node_3);
    node_2->add_edge(node_4);
    node_3->add_edge(node_2);
    node_4->add_edge(node_2);

    assert(node_1->dfs(2, visited));
    assert(node_1->dfs(4, visited));
    assert(node_2->dfs(6, visited));
    assert(node_2->dfs(8, visited));
    assert(node_3->dfs(4, visited));
    assert(!node_2->dfs(2, visited));
    assert(!node_3->dfs(8, visited));

    delete node_1;
    delete node_2;
    delete node_3;
    delete node_4;
    return 0;

}
