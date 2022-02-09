import networkx as nx
import math
import community as community_louvain
import powerlaw
"""
Graph features from Structure features for SAT instances classification (Ansotegui)
------
The scale free structure (based on variable occurrences) (estimation computed by method of maximum likelihood)

exponent of the Power law distribution of variable occurrences
compute the function f_v(k), which is the number of variables that have a number of occurrences equal to k, divided by the number of variables n.
# Assuming that this function follows a power-law distribution (f_v(k) roughly = ck^-a_v), we can estimate the exponent a_v of the power law distribution that bes fits this collection of points.
This estimation is computed by the method of maximum likelihood

-Compute for all numbers k, f_v(k) = var(k)/n
-for this series, estimate the power law exponent with maximum likelihood (ask/research more about this), also the plfit package

alpha = 1 + n[sum(ln(x_i/x_min)]^-1
--------

Variable incidence graph (VIG)

Clause variable incidence graph (CVIG)

Methods for creating the VIG and CVIG should be alright


Following details on formula and calculations still unclear
Then the fractal dimension of both the VIG and CVIG are calculated
by computing the function N(r) . can compute the degree d (fractal dimension) that best fits the function N(r). 
This value is estimated by linear regression interpolating the points log N(r) vs log r

------
And the Modularity Q of the VIG is calculated
The modularity of a graph is the maximal modularity for any possible partition Q(C)  = max{Q(G,C) | C}
We can find this maximum partition with the community package (uses louvain method), we just need to find out how to get the 
modularity of that partition 
----  


Steps and features
1. Create VIG and CVIG graphs (should be alright)
2. Calculate the scale free structure based on variable occurrences (Figure it out?)
3. Calculate self-similiar structure for VIG and CVIG
4. Get the modularity Q (We can find the best partition, it is just left to get the modularity from that partition - Read more into what this is, and how to extract it from the partition.

"""


def variable_occurrences(clauses, c, v):
    # variable count is needed
    variable_count = [0] * (v + 1)

    for clause in clauses:
        for literal in clause:
            variable_count[abs(literal)] += 1

    # compute the function f_v(k), which is the number of variables that have a number of occurrences equal to k, divided by the number of variables n.
    f_v_k = [0] * (v + 1)

    for count in variable_count:
        f_v_k[count] += 1

    # divide by number of variables
    f_v_k = [x/v for x in f_v_k]

    return f_v_k


def estimate_power_law_alpha(data):
    # Assuming that this function follows a power-law distribution (f_v(k) roughly = ck^-a_v),
    # we can estimate the exponent a_v of the power law distribution that bes fits this collection of points.
    # Use maximum likelihood estimator

    # use pwerlaw package, results with 0 are removed... Not sure on a theoretical level if they should be replaced with something or...
    data = [x for x in data if x > 0]

    results = powerlaw.Fit(data)

    return results.power_law.alpha


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
    vig = nx.Graph()

    for k, clause in enumerate(clauses):

        # 1/ (|c| choose 2)
        weight = 1 / math.comb(len(clause), 2)

        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                v_node_i = "v_" + str(abs(clause[i]))
                v_node_j = "v_" + str(abs(clause[j]))

                # get the weight of the edge if there is already an edge, otherwise 0 is the start of the sum
                edge_weight = vig.get_edge_data(v_node_i, v_node_j, default={'weight': 0})['weight']

                edge_weight += weight
                vig.add_edge(v_node_i, v_node_j, weight=edge_weight)

    # node_degrees = []
    #
    # for n in vg.nodes:
    #     degree = len(nx.edges(vg, n))
    #     node_degrees.append(degree)
    #
    # return node_degrees
    return vig


def compute_modularity_q(graph):
    # get the best partition
    partition = community_louvain.best_partition(graph)

    # calculate the modularity of the partition
    modularity = community_louvain.modularity(partition, graph)

    return modularity

