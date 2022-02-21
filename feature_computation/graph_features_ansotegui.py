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

Then the fractal dimension of both the VIG and CVIG are calculated
by computing the function N(r) (Computing by burning node degrees approximation algorithm). 
This is an estimate of the minimum number of circles with radius r that can cover the graph.
This value is estimated by linear regression interpolating the points log N(r) vs log r, as N(r) ~ r^-d.

------
And the Modularity Q of the VIG is calculated
The modularity of a graph is the maximal modularity for any possible partition Q(C)  = max{Q(G,C) | C}
We can find this maximum partition with the community package (uses louvain method), and the result is the modularity of the best partition.
----  

"""


def estimate_power_law_alpha(clauses, c, v):
    """
    Estimates the power law alpha (Code adapted from Ansotegui implementation)
    :param clauses:
    :param c:
    :param v:
    :return: best fit estimated alpha
    """
    X, Y, Sylogx, Syx = variable_occurrences(clauses, c, v)
    alpha = most_likely(X, Y, Sylogx, Syx)

    return alpha


def variable_occurrences(clauses, c, v):
    """
    Computes the number of occurrences of each variable, and extra values based on these occurrences needed to estimate the power law fit
    :param clauses:
    :param c:
    :param v:
    :return:
    """
    # variable count is needed
    # index of the variable will contain the number of times it occurs in the cnf formula (in all clauses)
    variable_count = [0] * (v + 1)

    for clause in clauses:
        for literal in clause:
            variable_count[abs(literal)] += 1

    # compute the function f_v(k), which is the number of variables that have a number of occurrences equal to k, divided by the number of variables n.
    f_v_k = [0] * (c + 1)

    # there is no variable 0
    for count in variable_count[1:]:
        f_v_k[count] += 1
    count_occurrences = [(count, occurrences) for count, occurrences in enumerate(f_v_k) if occurrences != 0]
    f_v_k = [x for x in f_v_k if x>0]

    # should be the number or literal occurrences
    Sy = sum([occurrences for (count, occurrences) in count_occurrences])
    # x is also used

    n = len(f_v_k)
    X = [count for (count, occurrences) in count_occurrences]
    Y = [0] * (n+1)

    Syx = [0] * (n + 1)
    Sylogx = [0] * (n+1)

    for i in range(n-1, -1, -1):
        Y[i] = Y[i+1] + count_occurrences[i][1] / Sy

        Sylogx[i] = Sylogx[i+1] + count_occurrences[i][1] / Sy * math.log(X[i])
        Syx[i] = Syx[i + 1] + count_occurrences[i][1] / Sy * X[i]

    return X, Y, Sylogx, Syx


def most_likely(X, Y, sylogx, syx, maxxmin=10, verbose=False):
    """
    Fits the data to a powerlaw
    :param X:
    :param Y:
    :param sylogx:
    :param syx:
    :param maxxmin:
    :param verbose:
    :return: The best alpha
    """

    best_alpha = 0
    best_x_min_a = 0
    best_diff_a = 1

    best_ind_a = 0
    where_a = 0

    n = len(X)

    for ind in range(1, maxxmin + 1):
        if ind < n-3:

            xmin = X[ind]
            alpha = -1 - (1 / ((sylogx[ind] / Y[ind]) - math.log((xmin - 0.5))))

            # beta = math.log(1 / (syx[ind] / Y[ind] - xmin) + 1)

            #model powerlaw
            worst_diff = -1
            worst_x = -1

            for j in range(ind+1, n):
                aux = abs(Y[j]/Y[ind] - pow_law_c(X[j], xmin, alpha))

                if aux >= best_diff_a:
                    worst_diff = aux
                    worst_x = X[j]
                    break
                elif aux >= worst_diff:
                    worst_diff = aux
                    worst_x = X[j]

            for j in range(ind, n-1):
                if X[j] + 1 < X[j+1]:
                    aux = abs(Y[j+1]/Y[ind] - pow_law_c(X[j] + 1, xmin, alpha))

                    if aux >= best_diff_a:
                        worst_diff = aux
                        worst_x = X[j]+1
                        # finish search of worst difference
                        break
                    elif aux >= worst_diff:
                        worst_diff = aux
                        worst_x = X[j]+1

            if worst_diff < best_diff_a:
                best_alpha = alpha
                best_x_min_a = xmin
                best_diff_a = worst_diff
                best_ind_a = ind
                where_a = worst_x

    if verbose:
        print("alpha: ", -best_alpha)
        print("min: ", best_x_min_a)
        print("error ", best_diff_a, " in ", where_a)
    return -best_alpha


def pow_law_c(x, xmin, alpha):
    """
    Computes sum_{i = x} ^ {\infty} x ^ {alpha} / sum_{i = xmin} ^ {\infty} x ^ {alpha}
    or approximates it as (x / xmin) ^ (alpha + 1)
    :param x:
    :param xmin:
    :param alpha:
    :return:
    """

    assert (alpha < -1)
    assert (xmin <= x)

    max_iterations = 10000

    num = 0
    den = 0

    i = xmin

    if xmin < 25:
        while i < x:
            den += math.pow(i, alpha)
            i += 1

        p_old = -2
        p = -1
        n = 0

        while abs(p - p_old) > 0.00000001 and n < max_iterations:
            den += math.pow(i, alpha)
            num += math.pow(i, alpha)

            i += 1
            n += 1
            p_old = p
            p = num/den

        if n < max_iterations:
            return p

    return math.pow(x / xmin, alpha + 1)


def estimate_power_law_alpha_lib(data):
    """
    Uses the powerlaw package to fit data, however this does not take into account missing data
    :param data:
    :return:
    """
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
        abs_clause = [abs(lit) for lit in clause]

        weight = 1/len(clause)

        c_node = c_nodes[i]

        # for the variable, not the literal
        for k, v_node in enumerate(v_nodes):

            var_num = k+1

            if var_num in abs_clause:
                # weight should be 1/ size of the clause
                cvig.add_edge(c_node, v_node, weight=weight)
            # else:
            #     # If the variable is not in the clause, then the weight should be 0
            #     cvig.add_edge(c_node, v_node, weight=0)

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
    """
    Compute the modularity of the best partition (as estimated by the louvain method, using the python-louvain package
    :param graph:
    :return: The modularit of the graph
    """
    # get the best partition
    partition = community_louvain.best_partition(graph)

    # calculate the modularity of the partition
    modularity = community_louvain.modularity(partition, graph)

    return modularity


def burning_by_node_degree(graph, n: int):
    """
    Burning by node degree algorithm, adapted from paper pseudocode and implementation
    :param graph:
    :param n:
    :return: N(r) estimated number of circles needed to cover the graph for each circle radius r
    """
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
    dmaxx = 16

    for i in range(1, min(dmaxx+1, len(N))):
        if N[i - 1] > num_connected_components:
            burned = [False] * (n + 1)
            burned[0] = True

            # if any member in burned is still false
            while not all(burned):
                c = highest_degree_unburned_node(node_degrees, burned)
                # for every possible node c.
                S = circle(c, i-1, graph) # circle with centre c and radius i

                # print("nodes in circle", S)
                for x in S:

                    burned[x] = True

                N[i] += 1

    return N


def highest_degree_unburned_node(node_degrees, burned):
    """
    Get the node with the highest degree that is still unburned
    :param node_degrees:
    :param burned:
    :return:
    """
    # nodes are pre sorted in terms of their degree, does not change
    for (node, degree) in node_degrees:
        if not burned[node]:
            return node


def circle(centre, radius, graph):
    """
    Get the nodes within the circle with centre and radius
    :param centre:
    :param radius:
    :param graph:
    :return:
    """
    # circle with centre c and radius i
    # centre is a node
    # A circle of centre c and radius r is a subset of nodes of G
    # such that the distance (just in terms of how many nodes away from the center) between any of them and the node c, is smaller than r
    subgraph = networkx.generators.ego_graph(G=graph, n=centre, radius=radius)

    # return the nodes in the graph
    return subgraph.nodes


def linear_regression_fit(data):
    """
    Fit data with a linear regression and interpolation, adapted from code for ansotegui
    :param data:
    :return:
    """
    data = [x for x in data if x>0]
    # trim data to have no leading or trailing 0s

    poly_regression_X = [math.log(x) for x in range(1, len(data) + 1)]
    poly_regression_Y = [math.log(x) for x in data]
    exp_regression_X = [x for x in range(1, len(data) + 1)]
    exp_regression_Y = poly_regression_Y

    poly = regression(poly_regression_X, poly_regression_Y)
    exp = regression(exp_regression_X, exp_regression_Y)

    # estimate with linear regression interpolating points log N(r) vs log r

    return -poly[0], -exp[0]


def regression(X, Y):
    """
    Perform the regression
    :param X:
    :param Y:
    :return:
    """
    # given list of points, computes the alpha abd beta of a regression, translated from paper
    Sx = sum(X)
    Sy = sum(Y)
    Sxx = sum([x*x for x in X])
    Syy = sum([y*y for y in Y])
    Sxy = sum([x * y for (x, y) in zip(X, Y)])

    try:
        alpha = (Sx * Sy - len(X) * Sxy)/(Sx * Sx - len(X) * Sxx)
        beta = Sy / len(X) - alpha * Sx / len(X)
    except ZeroDivisionError:
        alpha = 1
        beta = 1

    return alpha, beta
