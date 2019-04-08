import langid                             #引入langid模块

def language_identification(st):
    i = langid.classify(st)
    return i[0]
