import os

os.chdir("../SAT-features-competition2012/")
stream = os.popen('./features basic.cnf')
output = stream.read()

output = output.split("\n")

features_names = output[-3].split(',')
features = map(float, output[-2].split(','))

features_dict = dict(zip(features_names, features))

print("feature names: ", features_names)
print("features: ", features)
print(features_dict)
