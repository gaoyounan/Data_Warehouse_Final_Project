def load_stop_word():
    file = "data/scikitlearn_stopword.txt"
    file = open(file)
    return file.readlines()
