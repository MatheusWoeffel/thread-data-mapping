import os
import sys
from doe import generateDoeCSV
import csv


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
    """ python3 run_experiments.py machine_name start_index n_rounds
    """ 
    dir_path = "/home/users/mwcamargo/td_mapping/"
    machine_name = sys.argv[1]
    start_index = int(sys.argv[2])
    n_rounds = int(sys.argv[3])
    
    #Generate a doe corresponding to some round and them reads it to pick up the mappings corresponding to the round
    for i in range(start_index, start_index + n_rounds):
        generateDoeCsv(dir_path +"doe_"+ machine_name + "_{number}.csv".format(number=i))
        
        with open(dir_path + "doe_" + machine_name + "_{number}.csv".format(number=i), "r") as doe:
            doe_csv = csv.reader(doe) 

            for row  in doe_csv:
                thread_mapping = row[2]
                data_mapping = row[3]
                app = row[0]
                mode = row[1]

               time_script =  """/run {mode} {app} > /tmp/out 2> /dev/null
                    TIME=`grep "Time:" /tmp/out | awk {'print $2'}
                    echo {app},{mode},{thread},{data}$TIME >> {time_archive}                  
                """.format(time_archive=dir_path + machine_name + ".time", app = app, 
                        mode = mode, thread = thread_mapping, data = data_mapping)
                change_data_mapping(row[3])
                change_thread_mapping(row[2])
                os.system(time_script)

            

