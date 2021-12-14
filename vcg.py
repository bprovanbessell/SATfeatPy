import networkx as nx

# Create VCG
# Variable-Clause Graph features
# A variable-clause graph (VCG) is a bipartite graph with a node for each variable, a node for each clause,
# and an edge between them whenever a variable occurs in a clause


def create_vcg(clauses, c, v):
    vcg = nx.Graph()

    # Node for each variable
    # node for each clause

    # How to encode the variables and clauses, variables have numbers in cnf, clauses have distinct indexes.
    # Simple and easy way to do it, v in front of variable number, c in front of clause index

    for i, clause in enumerate(clauses):
        c_node = "c_" + str(i)

        for literal in clause:
            v_node = "v_" + str(abs(literal))

            vcg.add_edge(c_node, v_node)

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
