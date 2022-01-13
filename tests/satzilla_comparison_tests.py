import os
import unittest


class SatzillaComparisonTest(unittest.TestCase):
    """
    Satzilla and satelite only run on linux unfortunately
    """
    def test_basic(self):
        os.chdir("../SAT-features-competition2012/")

        stream = os.system('./features --all ../SAT-features/basic.cnf output.cnf')
        output = stream.read()

        output = output.split("\n")

        features_names = output[-3].split(',')
        features = map(float, output[-2].split(','))

        features_dict = dict(zip(features_names, features))

        print("feature names: ", features_names)
        print("features: ", features)
        print(features_dict)


os.chdir("../SAT-features-competition2012/")
stream = os.popen('./features --base basic.cnf')
output = stream.read()

output = output.split("\n")

features_names = output[-3].split(',')
features = map(float, output[-2].split(','))

features_dict = dict(zip(features_names, features))

print("feature names: ", features_names)
print("features: ", features)
print(features_dict)
