import os

os.chdir("../SAT-features-competition2012/")
stream = os.popen('./features basic.cnf')
output = stream.read()

output = output.split("\n")

results_names = output[-3]
results = output[-2]

print("feature names: ", results_names)
print("features: ", results)
