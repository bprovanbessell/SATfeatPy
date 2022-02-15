import networkx as nx


def create_vg(clauses):
    """
    A variable graph (VG) has a node for each variable, and an edge between variables that occur together in at least
    one clause

    :param clauses:
    :return: The degree of each node in the variable graph
    """

    # for each literal in a clause, for all the other literals in that clause and the weight for each edge
    vg = nx.Graph()

    for k, clause in enumerate(clauses):

        for i in range(len(clause)):
            k = 0
            for j in range(i + 1, len(clause)):
                v_node_i = "v_" + str(abs(clause[i]))
                v_node_j = "v_" + str(abs(clause[j]))
                k += 1
                vg.add_edge(v_node_i, v_node_j, weight=pow(2, -k))

    node_degrees = []
    weights = []

    for n in vg.nodes:
        degree = len(nx.edges(vg, n))
        node_degrees.append(degree)
        for weight in vg.edges.data("weight", n):
            weights.append(weight[2])

    return node_degrees, weights


def create_cg(clauses):
    """
    A clause graph (CG) has a node for each clause, and an edge between clauses that have the same literal

    :param clauses:
    :return: The degree of each node in the variable graph and the weight for each edge
    """

    cg = nx.Graph()

    c_node = []

    for i, clause in enumerate(clauses):
        c_n = "c_" + str(i)
        c_node.append(c_n)

    for i, clause in enumerate(clauses):
        for literal in clause:
            weight = 0
            for j, clause_next in enumerate(clauses[i + 1:]):
                if literal in clause_next:
                    weight += 1
                    cg.add_edge(c_node[i], c_node[i + 1 + j], weight=weight)

    node_degrees = []
    weights = []

    for n in cg.nodes:
        degree = len(nx.edges(cg, n))
        for weight in cg.edges.data("weight", n):
            weights.append(weight[2])
        node_degrees.append(degree)

    return cg, node_degrees, weights


def create_rg(clauses):
    """
    A resolution graph (RG) has a node for each clause, and an edge between clauses if they produce a
    non-tautological resolvent

    :param clauses:
    :return: The degree of each node in the variable graph and the weight for each edge
    """

    rg = nx.Graph()

    c_node = []

    for i, clause in enumerate(clauses):
        c_n = "c_" + str(i)
        c_node.append(c_n)

    for i, clause in enumerate(clauses):
        for j, clause_next in enumerate(clauses[i + 1:]):
            if len(list(set(clause) & set(clause_next))) == 1:
                k = len(set(clause)) + len(set(clause_next))
                weight = pow(2, -(k - 2))
                rg.add_edge(c_node[i], c_node[i + 1 + j], weight=weight)

    node_degrees = []
    weights = []

    for n in rg.nodes:
        degree = len(nx.edges(rg, n))
        for weight in rg.edges.data("weight", n):
            weights.append(weight[2])
        node_degrees.append(degree)

    return node_degrees, weights


def create_big(clauses):
    """
    A binary implication graph (BIG) it's a directed graph that has a node for each literal, and an edge if
    there's an implication between the literals

    :param clauses:
    :return: The degree of each node in the variable graph and the weight of each edge
    """

    big = nx.DiGraph()

    for k, clause in enumerate(clauses):
        for i in range(len(clause)):
            v_node1 = "v_" + str(abs(clause[i]))
            v_node2 = "v_" + str(-abs(clause[i]))
            big.add_node(v_node1)
            big.add_node(v_node2)

    for clause in clauses:
        if len(clause) == 2:
            a = clause[0]
            b = clause[1]
            big.add_edge('v_' + str(-a), 'v_' + str(b), weight=1)
            big.add_edge('v_' + str(-b), 'v_' + str(a), weight=1)

    node_degrees = []
    weights = []

    for n in big.nodes:
        degree = len(nx.edges(big, n))
        for weight in big.edges.data("weight", n):
            weights.append(weight[2])
        node_degrees.append(degree)

    return big, node_degrees, weights

