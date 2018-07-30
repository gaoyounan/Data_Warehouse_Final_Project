def load_stop_word():
    file = "data/scikitlearn_stopword.txt"
    file = open(file)
    stop_list = list()
    for l in file.readlines():
        stop_list.append(l.split("\n")[0])
    return stop_list