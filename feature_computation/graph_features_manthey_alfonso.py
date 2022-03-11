import networkx as nx
import numpy as np
from scipy import stats


def create_vcg(clauses):
    """
    Create VCG
    Variable-Clause Graph features
    A variable-clause graph (VCG) is a bipartite graph with a node for each variable, a node for each clause,
    and an edge between them whenever a variable occurs in a clause

    :param clauses:
    :return: Variable node degrees and clause node degrees
    """
    vcgpos = nx.Graph()
    vcgneg = nx.Graph()

    # Node for each variable
    # node for each clause

    for i, clause in enumerate(clauses):
        c_node = "c_" + str(i)

        for literal in clause:
            if literal > 0:
                v_node = "v_" + str(literal)
                vcgpos.add_edge(c_node, v_node)
            elif literal < 0:
                v_node = "v_" + str(literal)
                vcgneg.add_edge(c_node, v_node)

    v_node_degrees_pos = []
    v_node_degrees_neg = []
    c_node_degrees_pos = []
    c_node_degrees_neg = []

    # get node statistics
    for i in vcgpos.nodes():
        if 'c' in i:
            degree = len(nx.edges(vcgpos, i))
            c_node_degrees_pos.append(degree)
        elif 'v' in i:
            degree = len(nx.edges(vcgpos, i))
            v_node_degrees_pos.append(degree)
    for i in vcgneg.nodes():
        if 'c' in i:
            degree = len(nx.edges(vcgneg, i))
            c_node_degrees_neg.append(degree)
        elif 'v' in i:
            degree = len(nx.edges(vcgneg, i))
            v_node_degrees_neg.append(degree)

    return v_node_degrees_pos, v_node_degrees_neg, c_node_degrees_pos, c_node_degrees_neg


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

    return node_degrees, weights


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


def neighbors_nodes(l, clauses):
    big, _, _ = create_big(clauses)
    neighbors = big.neighbors('v_' + str(l))
    return neighbors


def create_exo_and_band(clauses):
    """
        Full-AND, Blocked-AND and Exactly One Constraint Graphs

        :param clauses:
        :return: The degree of each node in the variable graph and the weight of each edge
    """

    andg = nx.Graph()
    bandg = nx.Graph()
    exog = nx.Graph()

    for k, clause in enumerate(clauses):
        for i in range(len(clause)):
            v_node1 = "v_" + str(abs(clause[i]))
            v_node2 = "v_" + str(-abs(clause[i]))
            andg.add_node(v_node1)
            andg.add_node(v_node2)
            bandg.add_node(v_node1)
            bandg.add_node(v_node2)
            exog.add_node(v_node1)
            exog.add_node(v_node2)

    for clause in clauses:
        if len(clause) > 2:
            exo = True
            for l0 in clause:
                k = 0
                rem_clause = clause[:]
                rem_clause.remove(l0)
                for l1 in rem_clause:
                    nodel1neg = 'v_' + str(-l1)
                    if nodel1neg not in neighbors_nodes(l0, clauses):
                        exo = False
                        break
                    k += 1
                    andg.add_edge('v_' + str(l1), 'v_' + str(-l0), weight=pow(2, -k))
                if not exo:
                    break

            if not exo:
                obv_block = True
                for l0 in clause:
                    k = 0
                    rem_clause = clause[:]
                    rem_clause.remove(l0)
                    for l1 in rem_clause:
                        if len(clause) > 3:
                            obv_block = False
                            break
                        k += 1
                        bandg.add_edge('v_' + str(l1), 'v_' + str(-l0), weight=pow(2, -k))
                    if not obv_block:
                        break
            elif exo:
                for l0 in clause:
                    rem_clause = clause[:]
                    rem_clause.remove(l0)
                    for l1 in rem_clause:
                        exog.add_edge('v_' + str(l1), 'v_' + str(l0), weight=1)

    return andg, bandg, exog


def get_degrees_weights(G):
    """
            Function to get node degrees and weights for Full-AND, Blocked-AND and Exactly One Constraint Graphs

            :param Graph:
            :return: The degree of each node in the variable graph and the weight of each edge
    """
    node_degrees = []
    weights = []

    for n in G.nodes:
        degree = len(nx.edges(G, n))
        for weight in G.edges.data("weight", n):
            weights.append(weight[2])
        node_degrees.append(degree)

    return node_degrees, weights


def get_graph_stats(name, node_degrees, weights=0):
    """
                Function to get statistics for different graphs

                :param node_degrees and weights:
                :return: dictionary with different stats
    """

    if not node_degrees:
        node_degrees = [0]
    if not weights:
        weights = [0]

    node_min = np.min(node_degrees)
    node_max = np.max(node_degrees)
    node_mode = stats.mode(node_degrees)[0][0]
    node_mean = np.mean(node_degrees)
    node_std = np.std(node_degrees)
    node_zeros = np.count_nonzero(node_degrees == 0)
    node_entropy = stats.entropy(node_degrees)
    node_quantiles = stats.mstats.mquantiles(node_degrees)
    node_val_rate = np.count_nonzero(node_degrees == node_mode) / len(node_degrees)
    node_stats = [node_min, node_max, node_mode, node_mean, node_std, node_zeros, node_entropy, node_quantiles[0],
                  node_quantiles[1], node_quantiles[2], node_val_rate]

    weights_min = np.min(weights)
    weights_max = np.max(weights)
    weights_mode = stats.mode(weights)[0][0]
    weights_mean = np.mean(weights)
    weights_std = np.std(weights)
    weights_zeros = np.count_nonzero(weights == 0)
    weights_entropy = stats.entropy(weights)
    weights_quantiles = stats.mstats.mquantiles(weights)
    weights_val_rate = np.count_nonzero(weights == weights_mode) / len(weights)
    weights_stats = [weights_min, weights_max, weights_mode, weights_mean, weights_std, weights_zeros, weights_entropy,
                     weights_quantiles[0], weights_quantiles[1], weights_quantiles[2], weights_val_rate]

    deg_names = ["node_min", "node_max", "node_mode", "node_mean", "node_std", "node_zeros", "node_entropy", "node_q1",
                 "node_q2", "node_q3", "node_val_rate"]

    weights_names = ["weights_min", "weights_max", "weights_mode", "weights_mean", "weights_std", "weights_zeros",
                     "weights_entropy", "weights_q1", "weights_q2", "weights_q3", "weights_val_rate"]

    deg_names = [name + x for x in deg_names]
    weights_names = [name + x for x in weights_names]

    stats_dict = dict(zip(deg_names, node_stats))
    stats_dict.update(dict(zip(weights_names, weights_stats)))

    return stats_dict
