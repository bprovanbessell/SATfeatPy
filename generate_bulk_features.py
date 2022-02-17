import sat_instance.sat_instance
from sat_instance.sat_instance import SATInstance
import glob

path_to_cnfs = "/projects/satdb/dataset_final/"

# for each file, we need to create a sat_instance for it
file_list = glob.glob(path_to_cnfs)

for file_name in file_list:
    sat_inst = SATInstance(file_name)

    sat_inst.gen_basic_features()
    sat_inst.gen_dpll_probing_features()
    # linux only
    # sat_inst.gen_local_search_probing_features()
    sat_inst.gen_ansotegui_features()