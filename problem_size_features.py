import cnfgen

with open("cnf_examples/basic.cnf") as f:
    for line in f:
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            sizes = line.split(" ")
            variables = int(sizes[2])
            clauses = int(sizes[3])
            ratio = clauses/variables

            print(clauses)
            print(variables)
            print(ratio)