import os
from doe import *


def change_num_threads(num_threads):
    os.environ["OMP_NUM_THREADS"] = str(num_threads)

def change_data_mapping(data_mapping_policy):
    os.system("sysctl kernel.numaBalancing=0 &> /dev/null")

    if data_mapping_policy == "intALL":
        os.environ["NCTL"]= "numactl -i all"
    elif data_mapping_policy == "memALL":
        os.environ["NCTL"] = "numactl -m all"
    elif data_mapping_policy == "numaBalancing":
        os.system("sysctl kernel.numaBalancing=1 &> /dev/null")
        os.environ["NCTL"] = ""

def change_thread_mapping(thread_mapping_policy):
    if thread_mapping_policy == "rr":
        os.system("unset -v KMP_AFFINITY")
        os.system("export GOMP_CPU_AFFINITY=0-87")
    else:
        os.system("unset -v GOMP_CPU_AFFINITY")
        os.system("export KMP_AFFINITY={policy}".format(policy=thread_mapping_policy))



if __name__ == "__main__":
    generateDefaultDoeCSV()
    #opens the default doe csv
    with open("doe.csv", "r") as doe:
        experiment_rounds = doe.readlines()
        for experiment_round in experiment_rounds:
            mappings = experiment_round.split(",")
            thread_mappings = mappings[0]
            data_mappings =   mappings[1]
