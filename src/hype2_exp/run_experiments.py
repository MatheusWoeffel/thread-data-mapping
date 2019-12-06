import os
import sys
from doe import *
from ai_benchmark import AIBenchmark


def change_num_threads(num_threads):
    os.environ["OMP_NUM_THREADS"] = str(num_threads)
    os.system("export OMP_NUM_THREADS")
def change_data_mapping(data_mapping_policy):
    os.system("/scratch/mwcamargo/utils --numa-off")

    if data_mapping_policy == "intALL":
        os.environ["NCTL"]= "numactl -i all"
        os.system("export NCTL")
    elif data_mapping_policy == "memALL":
        os.environ["NCTL"] = "numactl -m all"
    elif data_mapping_policy == "numaBalancing":
        os.system("/scratch/mwcamargo/utils --numa-on")
        os.environ["NCTL"] = ""

def change_thread_mapping(thread_mapping_policy):
    os.system("unset -v GOMP_CPU_AFFINITY")
    if thread_mapping_policy == "rr":
        os.environ["KMP_AFFINITY"] = "verbose,explicit,granularity=fine,proclist=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]"
        os.system("export KMP_AFFINITY=verbose,explicit,granularity=fine,proclist=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]")
    else:
        os.environ["KMP_AFFINITY"] = "verbose,{policy}".format(policy=thread_mapping_policy)
        os.system("export KMP_AFFINITY=verbose,{policy}".format(policy=thread_mapping_policy))


if __name__ == "__main__":
    number_of_rounds = 10

    for i in range(0,number_of_rounds):
        generateDoeCSV("doe_{number}.csv".format(number=i))
        #opens the default doe csv
        with open("doe_{number}.csv".format(number=i), "r") as doe:
            experiment_rounds = doe.readlines()
            list_of_results = []

            for experiment_round in experiment_rounds:
                mappings = experiment_round.split(",")
                thread_mapping = mappings[0]
                data_mapping =   mappings[1]
                change_data_mapping(data_mapping)
                change_thread_mapping(thread_mapping)
                benchmark = AIBenchmark(use_CPU=True)
                current_result = benchmark.run()
                sys.stdout.flush() #Print the output when each run finishes
                list_of_results.append(current_result)
                #print(current_result)
            
