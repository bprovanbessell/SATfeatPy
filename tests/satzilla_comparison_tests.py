import os

stream = os.popen('./../SAT-features-competition2012/features basic.cnf')
output = stream.read()

output = output.split("\n")

results_names = output[-2]
results = output[-1]

print(results_names)
print(results)
