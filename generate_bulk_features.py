from sat_instance.sat_instance import SATInstance
import glob

path_to_cnfs = "/projects/satdb/dataset_final/"

# for each file, we need to create a sat_instance for it
file_list = glob.glob(path_to_cnfs)

for file_name in file_list:
    