import random

thread_mappings = ["none", "rr", "scatter", "compact"]
data_mappings = ["none", "intALL", "memALL", "numaBalancing"]


def getListOfPossibleExperiments(thread_mappings, data_mappings):
    """
    :param data_mappings: List of all data_mappings(str) that may be used
    :param thread_mappings: List of all thread mappings(str) that may be used
    :return: List of all possible experiments that may be done, the list is made up of tuples in the following order
    ("threadMapping", "dataMapping)
    Example of calling: getListOfPossibleExperiments(["none"], ["intALL", "memALL"])
    """

    possibleExperiments = []
    for thread_mapping in thread_mappings:
        for data_mapping in data_mappings:
            newExperimentPair = (thread_mapping,data_mapping)
            possibleExperiments.append(newExperimentPair)

    return possibleExperiments


def randomizeListOfExperiments(experiments):
    """

    :param experiments: List containing the various tuples that forms the pair of data mapping and thread mapping of each
    possible experiment.
    :return: A randomized version of the list in experiments
    """

    random.shuffle(experiments)
    return experiments

def generateDoeCSV(list_of_experiments, doe_path):
    """
    This function generates a CSV file based on a list of experiments.

    :param list_of_experiments: Ordered list of pairs of data_mappings and thread_mappings that forms the each experiment.
    [("mapping1", "mapping2"), ...]
    :return: None
    """

    with open(doe_path,"w") as doe_archive:
        for pairOfMapping in list_of_experiments:
            new_line = "{thread_mapping},{data_mapping}\n".format(thread_mapping=pairOfMapping[0],data_mapping=pairOfMapping[1])
            doe_archive.write(new_line)

        doe_archive.close()

def generateDefaultDoeCSV():
    possibleExperiments = getListOfPossibleExperiments(thread_mappings,data_mappings)
    randomizedExperiments = randomizeListOfExperiments(possibleExperiments)
    generateDoeCSV(randomizedExperiments,"doe.csv")