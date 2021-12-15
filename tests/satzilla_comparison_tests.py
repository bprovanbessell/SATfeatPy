import os

os.chdir("../SAT-features-competition2012/")
stream = os.popen('./features basic.cnf')
output = stream.read()

output = output.split("\n")

results_names = output[-2]
results = output[-1]

print("feature names: ", results_names)
print("features: ", results)
