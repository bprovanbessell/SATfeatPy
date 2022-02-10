import networkx
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
    cvig = nx.Graph()

    # Node for each variable
    # node for each clause

    # create the variable and clause nodes
    v_nodes = [i for i in range(1, v+1)]
    c_nodes = [i for i in range(v+1, v+1+c)]

    for i, clause in enumerate(clauses):

        weight = 1/len(clause)

        c_node = c_nodes[i]

        # for the variable, not the literal
        for k, v_node in enumerate(v_nodes):

            var_num = k+1

            if var_num in clause:
                # weight should be 1/ size of the clause
                cvig.add_edge(c_node, v_node, weight=weight)
            else:
                # If the variable is not in the clause, then the weight should be 0
                cvig.add_edge(c_node, v_node, weight=0)

    return cvig


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
                # integer for node keys
                v_node_i = abs(clause[i])
                v_node_j = abs(clause[j])

                # get the weight of the edge if there is already an edge, otherwise 0 is the start of the sum
                edge_weight = vig.get_edge_data(v_node_i, v_node_j, default={'weight': 0})['weight']

                edge_weight += weight
                vig.add_edge(v_node_i, v_node_j, weight=edge_weight)

    return vig


def compute_modularity_q(graph):
    # get the best partition
    partition = community_louvain.best_partition(graph)

    # calculate the modularity of the partition
    modularity = community_louvain.modularity(partition, graph)

    return modularity


def burning_by_node_degree(graph, n: int):
    # order nodes according to their degree such that degree(vi) >= degree(vj) when i < j

    # n is number of nodes
    # pseudocode in thesis of jesus giraldez, page 67...
    # returns vector N(r), then fractal dimension d must be calculated from this...
    # Supposedly we can assume N(r) ~ r^-d
    # Use regression, and then interpolation to get d...
    N = [0] * (n)
    N[1] = n
    i = 2

    # Order the nodes in terms of their degree
    node_degrees = []
    for node in graph.nodes:
        degree = len(nx.edges(graph, node))
        node_degrees.append((node, degree))

    # sort in terms of the degree, descending
    node_degrees.sort(key=lambda x: x[1], reverse=True)

    num_connected_components = networkx.number_connected_components(graph)

    while N[i - 1] > num_connected_components:
        burned = [False] * (n + 1)
        burned[0] = True
        N[i] = 0

        # if any member in burned is still false
        while not all(burned):
        # while exists_unburned_Node(burned):
            c = highest_degree_unburned_node(node_degrees, burned)
            #
            # print(c)
            # print(burned)

            # for every possible node c.
            S = circle(c, i, graph) # circle with centre c and radius i

            print("nodes in circle", S)
            for x in S:

                burned[x] = True

            N[i] += 1

        i = i + 1

    return N


def highest_degree_unburned_node(node_degrees, burned):
    # change the node keys s.t. they are integers instead of strings


    for (node, degree) in node_degrees:
        if not burned[node]:
            return node
    # TODO
    # as the method says I guess??
    # get the node with the highest degree that is also unburned (burned[node] = False)
    # This should be done before, as the graph doesn't change
    # Order the nodes in terms of their degree


def circle(centre, radius, graph):
    # circle with centre c and radius i
    # centre is a node
    print("centre node", centre)
    print("radius", radius)


    # A circle of centre c and radius r is a subset of nodes of G
    # such that the distance between any of them and the node c, is smaller than r

    # what exactly is the distance here? number of edges from centre, or weight on the edges (I will assume number of edges??)

    # returns a list of all the nodes within the circle with centre and radius as stated...

    # can specify distance as the weight here... Confirm what the distance is
    subgraph = networkx.generators.ego_graph(G=graph, n=centre, radius=radius)
    # TODO: check for faster way to do it
    #  https://stackoverflow.com/questions/62843205/find-nodes-within-distance-in-networkx-and-python

    # return the nodes in the graph
    return subgraph.nodes


from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
def linear_regression_fit(data):

    data = data[1:]

    # remove trailing 0's
    Y_data = [x for x in data if x > 0]

    # should it be normalised? # Nnorm = N(r)/N(1)
    # 0 at the end, but ln(0) is undefined
    Y_data.append(0.000000001)
    X_data = [x for x in range(1, len(Y_data)+1)]
    # The assumption is that N(r) ~ r^-d for some value d (for self similar graphs)
    # So, we need to find d

    # again, seems to be powerlaw... So what are they on about with the interpolation

    # or, supposedly N(r) ~ e^-Br
    # how to do this interpolation?

    # This might also only be in some cases, e.g. these to formulas would not cover the structure of all SAT instances

    # r^-d = 1/r^d

    # We want to best fit the data (N(r)) that we have
    print(Y_data, X_data)

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [148,2,1,0])
    logged_Y = [math.log(x) for x in Y_data]
    logged_r = [math.log(x) for x in X_data]

    ax.scatter([1,2,3,4], logged_Y, label="logy")
    ax.scatter([1,2,3,4], logged_r, label="logx")

    plt.legend(loc='best')
    plt.show()
    # estimate with linear regression interpolating points log N(r) vs log r



    pass

