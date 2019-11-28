import re

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


if __name__ == "__main__":
    with open("/home/mwc/Documents/TD_mapping/saida_exp.txt","r+") as archive:
        all_text = archive.read()
        inference_scores_list = getScoreList(all_text, "Inference Score")
        training_scores_list =  getScoreList(all_text, "Training Score")
        execution_times_list =  getExecutionTimes(all_text)


        map2InferenceScore = {
        }

        map2ExecutionScore = {
        }

        map2ExecutionTimes = {
        }

        with open("doe.csv", "r") as doe:
            mappings = doe.readlines()
            for mapping,score in zip(mappings,scoresList):
                data_mapping = mapping.split(",")[1]
                map2score[data_mapping].append(int(score))

        for key in map2score.keys():
            average = 0
            number_of_items =0
            for item in map2score[key]:
                average += item
                number_of_items += 1
            average = average / number_of_items
            map2score[key] = average

        print(map2score)

    with open("/home/mwc/Documents/TD_mapping/saida_exp.txt") as experimentArchives:
        experimentTxt = experimentArchives.read()

        getExecutionTimes(experimentTxt)


