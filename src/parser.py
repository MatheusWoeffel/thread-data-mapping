import re
import doe

def getScoreList(experimentTXT, scoreDescriptor):
    """

    :param experimentTXT: Path do arquivo txt contendo os experimentos
    :param scoreDescriptor: String que define o nome do score
    :return: Lista com sequência de scores encontrados no arquivo experimentTXT
    """
    scoresList = []

    index = experimentTXT.find(scoreDescriptor)
    while index != -1:
        firstScoreIndex = index + len(scoreDescriptor)
        lastScoreIndex = firstScoreIndex + 3
        new_score = experimentTXT[firstScoreIndex:lastScoreIndex]
        scoresList.append(new_score)

        experimentTXT = experimentTXT[lastScoreIndex:]
        index = experimentTXT.find(scoreDescriptor)

    return scoresList


def getExecutionTimes(experimentTXT):
    execution_times_regex = "\d+[.]\d+.*[s]"
    execution_times_lines =  re.findall(execution_times_regex,experimentTXT)

    execution_times = []
    for execution_time_line in execution_times_lines:
        index_of_time_start = execution_time_line.find(": ")
        index_of_time_end = execution_time_line.find(" ±")
        execution_time = execution_time_line[index_of_time_start+1:index_of_time_end] 
        execution_times.append(execution_time)

    return execution_times


def populateDictionaryWithMappings(dictionary, data_mappings, thread_mappings):
    """

    :param dictionary: Dicionário a ser populado
    :param data_mappings: Lista contendo os mapeamentos de dados utilizados
    :param thread_mappings: Lista contendo os mapeamentos de threads utilizados
    :return: Null. A função apenas popula o dicionário passado como argumento
    """
    dictionary.clear()

    for thread_mapping in thread_mappings:
        for data_mapping in data_mappings:
            new_key = thread_mapping + "," + data_mapping 
            dictionary[new_key] = []


if __name__ == "__main__":
    experiments_output = input("Path of the results: ")
    machine_name = input("Machine Name: ")
    n_rounds = int(input("Number of Rounds: "))
    with open(experiments_output,"r+") as archive:
        all_text = archive.read()
        inference_scores_list = getScoreList(all_text, "Inference Score: ")
        training_scores_list =  getScoreList(all_text, "Training Score: ")
        execution_times_list =  getExecutionTimes(all_text)


        map2InferenceScore = {
        }

        map2TrainingScore = {
        }

        map2ExecutionTimes = {
        }

        populateDictionaryWithMappings(map2InferenceScore, doe.data_mappings, doe.thread_mappings)
        populateDictionaryWithMappings(map2TrainingScore, doe.data_mappings, doe.thread_mappings)
        populateDictionaryWithMappings(map2ExecutionTimes, doe.data_mappings, doe.thread_mappings)

        with open("doe.csv", "r") as doe:
            mappings = doe.readlines()
            #Remove the \n from the end of the mappings strings
            for i in range(len(mappings)):
                mappings[i] = mappings[i].rstrip("\n") #remove the \n

            for mapping,inferenceScore, trainingScore in zip(mappings,inference_scores_list, training_scores_list):
                map2InferenceScore[mapping].append(inferenceScore)
                map2TrainingScore[mapping].append(trainingScore)

            exec_times_per_run = 42
            i = 0
            for index, execution_time  in zip(range(len(execution_times_list)), execution_times_list):
                offset_index = index - (i * 42)
                if ((offset_index % 42) == 0) and offset_index != 0:
                    i+= 1
                
                mapping_used = mappings[i]
                map2ExecutionTimes[mapping_used].append(execution_time)


    results_path = "results_" + machine_name + "_" + str(n_rounds) + ".txt"
    
    applications_list = ["MobileNet-V2,inference", "MobileNet-V2,training",
                           "Inception-V3,inference", "Inception-V3,training",
                            "Inception-V4,inference", "Inception-V4,training",
                            "Inception-ResNet-V2,inference", "Inception-ResNet-V2,training",
                            "ResNet-V2-50,inference", "ResNet-V2-50,training",
                            "ResNet-V2-152,inference", "ResNet-V2-152,training",
                            "VGG-16,inference", "VGG-16,training",
                            "SRCNN-9-5-5,inference", "SRCNN-9-5-5,inference2", "SRCNN-9-5-5,training",
                            "VGG-19-Super-Res,inference", "VGG-19-Super-Res,inference2", "VGG-19-Super-Res,training",
                            "ResNet-SRGAN,inference", "ResNet-SRGAN,inference2", "ResNet-SRGAN,training",
                            "ResNet-DPED,inference", "ResNet-DPED,inference2", "ResNet-DPED,training",
                            "U-Net,inference", "U-net,inference2", "U-net,training",
                            "Nvidia-SPADE,inference", "Nvidia-SPADE,training",
                            "ICNet,inference", "ICNet,training",
                            "PSPNet,inference", "PSPNet,training",
                            "DeepLab,inference", "DeepLab,training",
                            "Pixel-RNN,inference", "Pixel-RNN,training",
                            "LSTM-Sentiment,inference", "LSTM-Sentiment,training", "GNMT-Translation"
                        ]

    with open(results_path, "w") as result_archive:
        for key in map2ExecutionTimes:
            execution_times_per_key = map2ExecutionTimes[key]
            for application_name, time in zip(applications_list, execution_times_per_key):
                result_per_application = "{machine_name},{mappings_used},{app_name},{time}".format(machine_name=machine_name,mappings_used=key,app_name=application_name,time=time)
                result_archive.write(result_per_application)
    

            
           

   


