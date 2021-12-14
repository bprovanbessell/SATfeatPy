

def parse_cnf(cnf_path):

    with open(cnf_path) as f:

        clauses_list = []
        c = 0
        v = 0
        cv_ratio = 0

        for line in f:
            if line[0] == 'c':
                continue
            if line[0] == 'p':
                sizes = line.split(" ")
                v = int(sizes[2])
                c = int(sizes[3])
                cv_ratio = c / v

                print("c: ", c)
                print("v: ", v)
                print("ratio: ", cv_ratio)

            else:
                # all following lines should represent a clause, so literals separated by spaces, with a 0 at the end,
                # denoting the end of the line.
                clauses_list.append([int(x) for x in line.split(" ")[:-1]])

    return clauses_list, c, v
