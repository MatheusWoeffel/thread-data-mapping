import random

thread_mappings = ["none", "rr", "scatter", "compact"]
data_mappings = ["none", "intALL", "memALL", "numaBalancing"]
applications = ["MobileNet-V2","Inception-V3","Inception-V4",
    "Inception-ResNet-V2", "ResNet-V2-50", "ResNet-V2-152",
    "VGG-16", "SRCNN-9-5-5", "VGG-19-Super-Res",
    "ResNet-SRGAN", "ResNet-DPED", "U-Net",
    "Nvidia-SPADE", "ICNet", "PSPNet",
    "DeepLab", "Pixel-RNN", "LSTM-Sentiment",
    "GNMT-Translation"]
execution_modes = ["training", "inference"]

"Doe line example= application,execution_mode,thread_mapping,data_mapping"

def getListOfPossibleExperiments(thread_mappings, data_mappings):
    """
    :param data_mappings: List of all data_mappings(str) that may be used
    :param thread_mappings: List of all thread mappings(str) that may be used
    :return: List of all possible experiments that may be done, the list is made up of tuples in the following order
    ("threadMapping", "dataMapping)
    Example of calling: getListOfPossibleExperiments(["none"], ["intALL", "memALL"])
    """

    possible_experiments = []
    for thread_mapping in thread_mappings:
        for data_mapping in data_mappings:
            for application in applications:
                for execution_mode in execution_modes:
                   new_experiment = (application, execution_mode, thread_mapping, data_mapping)
                   possible_experiments.append(new_experiment)

    return possible_experiments


def randomizeListOfExperiments(experiments):
    """

    :param experiments: List containing the various tuples that forms the pair of data mapping and thread mapping of each
    possible experiment.
    :return: A randomized version of the list in experiments
    """

    random.shuffle(experiments)
    return experiments

def generateDoeCsv(doe_path):
    """
    This function generates a CSV file based on a list of experiments.

    :param list_of_experiments: Ordered list of pairs of data_mappings and thread_mappings that forms the each experiment.
    [("mapping1", "mapping2"), ...]
    :return: None
    """
    possibleExperiments = getListOfPossibleExperiments(thread_mappings,data_mappings)
    randomizedExperiments = randomizeListOfExperiments(possibleExperiments)

    with open(doe_path,"w") as doe_archive:
        doe_archive.write("\n".join("{},{},{},{}".format(experiment[0],experiment[1],experiment[2],experiment[3]) 
            for experiment in randomizedExperiments))

if __name__ == "__main__":
    generateDoeCsv("./teste.csv")
