import networkx as nx
from math import comb
import community as community_louvain
"""
Graph features from Structure features fro SAT instances classification (Ansotegui)

Variable incidence graph (VIG)

Clause variable incidence graph (CVIG)

Then the fractal dimension of both the VIG and CVIG are calculated
And the Modularity Q of the VIG is calculated

The modularity of a graph is the maximal modularity for any possible partition Q(C)  = max{Q(G,C) | C}
Can be done using the community package

The other feature is the scale free structure (based on variable occurrences) (estimation computed by method of maximum likelihood)

"""


def create_cvig(clauses, c, v):
    """
    Create a Clause Variable incidence graph
    Set of vertices is the set of variables and set of clauses,
    with weight function w(x, c) = 1/|c| if x elem c, else 0

    :param clauses:
    :param c:
    :param v:
    :return: Variable node degrees and clause node degrees
    """
    vcg = nx.Graph()

    # Node for each variable
    # node for each clause

    # create the variable and clause nodes
    v_nodes = ['v_' + str(i) for i in range(1, v+1)]
    c_nodes = ['c_' + str(i) for i in range(0, c)]

    for i, clause in enumerate(clauses):

        weight = 1/len(clause)

        c_node = c_nodes[i]

        # for the variable, not the literal
        for k, v_node in enumerate(v_nodes):

            var_num = k+1

            if var_num in clause:
                # weight should be 1/ size of the clause
                vcg.add_edge(c_node, v_node, weight=weight)
            else:
                # If the variable is not in the clause, then the weight should be 0
                vcg.add_edge(c_node, v_node, weight=0)

    v_node_degrees = []
    c_node_degrees = []
    # get node statistics
    for i in range(c):
        degree = len(nx.edges(vcg, "c_" + str(i)))
        c_node_degrees.append(degree)

    for i in range(1, v+1):
        degree = len(nx.edges(vcg, "v_" + str(i)))
        v_node_degrees.append(degree)

    return v_node_degrees, c_node_degrees


def create_vig(clauses, c, v):
    """
    Create a Variable incidence graph
    Set of vertices is the set of variables,
    with weight function w(x, y) = sum( 1/ (|c| choose 2)) for x, y elem of c, for c elem F

    :param clauses:
    :param c:
    :param v:
    :return: Variable node degrees and clause node degrees
    """

    # we need to make sure that we avoid the duplicates within a clause
    vg = nx.Graph()

    for k, clause in enumerate(clauses):

        # 1/ (|c| choose 2)
        weight = 1 / comb(len(clause), 2)

        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                v_node_i = "v_" + str(abs(clause[i]))
                v_node_j = "v_" + str(abs(clause[j]))

                # get the weight of the edge if there is already an edge, otherwise 0 is the start of the sum
                edge_weight = vg.get_edge_data(v_node_i, v_node_j, default={'weight': 0})['weight']

                edge_weight += weight
                vg.add_edge(v_node_i, v_node_j, weight=edge_weight)

    node_degrees = []

    for n in vg.nodes:
        degree = len(nx.edges(vg, n))
        node_degrees.append(degree)

    return node_degrees


def compute_modularity_Q(graph):
    partition = community_louvain.best_partition(graph)


