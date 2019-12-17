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
    with open("../novos_resultados.txt","r+") as archive:
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

            print(map2ExecutionTimes)
            
           

   


