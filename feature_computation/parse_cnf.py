def parse_cnf(cnf_path):
    """
    Parse number of variables, number of clauses and the clauses from a standard .cnf file
    :param cnf_path:
    :return: clauses, number of clauses, and number of variables
    """

    with open(cnf_path) as f:

        clauses_list = []
        c = 0
        v = 0

        for line in f:
            stripped_line = line.strip()
            if not stripped_line or stripped_line[0] in {'c', 'p', '\n'}:
                continue

            # all following lines should represent a clause, so literals separated by spaces, with a 0 at the end,
            # denoting the end of the line.
            clause = [int(x) for x in stripped_line.split() if x != '0']
            clauses_list.append(clause)

        c = len(clauses_list)
        v = max([abs(l) for clause in clauses_list for l in clause])

    return clauses_list, c, v