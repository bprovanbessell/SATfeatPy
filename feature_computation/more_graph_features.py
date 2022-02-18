import math
from feature_computation import array_stats
import networkx as nx
import scipy.stats


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


def neighbors_nodes(l, clauses):
    big, _, _ = create_big(clauses)
    neighbors = big.neighbors('v_' + str(l))
    return neighbors


def create_exo_and_band(clauses):
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
                    if l1 not in neighbors_nodes(l0, clauses):
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
                        exog.add_edge('v_' + str(l1), 'v_' + str(l0))

    return andg, bandg, exog


def return_degrees_weights(G):

    node_degrees = []
    weights = []

    for n in G.nodes:
        degree = len(nx.edges(G, n))
        for weight in G.edges.data("weight", n):
            weights.append(weight[2])
        node_degrees.append(degree)

    return node_degrees, weights


def recursive_weight_heuristic(max_clause_size, clauses, v):

    # Code translated from RISS... I am sure there are some errors in the original code, which have been translated to this python implementation

    assert(max_clause_size > 0)

    feat_dict = {}

    # current value for each literal
    # Might want to add +1 so we can use the literals as indices...
    this_data_pos = [0] * (v+1)
    this_data_neg = [0] * (v + 1)

    this_data = [this_data_pos, this_data_neg]
    last_data_pos = [1] * (v + 1)
    last_data_neg = [1] * (v + 1)

    last_data = [last_data_pos, last_data_neg]

    muh = 1
    gamma = 5
    max_double = 10e200

    all_sequences = []

    # for 3 interations
    for iteration in range(1, (3+1)):

        iteration_steps = 0
        this_iteration_sequence = []

        # how likely the remaining clauses will be falsified by the model
        for i in range(len(clauses)):

            clause = clauses[i]
            clause_len = len(clause)

            if (clause_len == 1): continue

            if max_clause_size < clause_len:
                exponent = 0
            else:
                exponent = max_clause_size - clause_len

            try:
                a1 = math.pow(gamma, exponent)
            except OverflowError:
                a1 = float("inf")
            try:
                a2 = math.pow(muh, clause_len - 1)
            except OverflowError:
                a2 = float("inf")
            clause_constant = a1 / a2

            found_zero = False
            clause_value = 1
            # calculate the constant for the clause
            for j in range(clause_len):
                curr_lit = clause[j]

                if curr_lit < 0:
                    comp_ind = 0
                else:
                    comp_ind = 1

                # tilde is complement
                if last_data[comp_ind][curr_lit] == 0:
                    found_zero = True
                    break

                clause_value = clause_value * last_data[comp_ind][curr_lit]
                iteration_steps += 1

            if not found_zero:
                # only if there is no non-zero literal inside, add the values
                clause_value = clause_value * clause_constant

                # for each literal, divide the clause value by the  value for the corresponding complement to fit the calculation formula
                for j in range(clause_len):
                    curr_lit = clause[j]

                    if curr_lit < 0:
                        comp_ind = 0
                    else:
                        comp_ind = 1

                    this_data[comp_ind][curr_lit] += clause_value / last_data[comp_ind][curr_lit]

        # sequence for iteration i
        muh = 0
        for num_v in range(1, v+1):
            for p in range(2):

                # basically for positive and negative literals
                val = this_data[p][v]
                if val > max_double:
                    this_iteration_sequence.append(max_double)
                else:
                    this_iteration_sequence.append(val)

                muh += val

            iteration_steps += 1

        muh = muh / 2 * v

        if muh < 1: muh = 1

        last_data = this_data
        this_data_pos = [0] * (v + 1)
        this_data_neg = [0] * (v + 1)

        this_data = [this_data_pos, this_data_neg]

        all_sequences.append(this_iteration_sequence)

    for i, s in enumerate(all_sequences):
        write_stats(s, "rwh_" + str(i), feat_dict)

    return feat_dict

def write_stats(l, name, features_dict):
    l_mean, l_coeff, l_min, l_max = array_stats.get_stats(l)

    features_dict[name + "_mean"] = l_mean
    features_dict[name + "_coeff"] = l_coeff
    features_dict[name + "_min"] = l_min
    features_dict[name + "_max"] = l_max
