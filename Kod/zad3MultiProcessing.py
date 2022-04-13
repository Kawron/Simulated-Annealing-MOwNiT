if __name__=="__main__":
    from zad3 import main
    from multiprocessing import *

    for i in range(0,5):
        p = Process(target=main, args=(i,))
        p.start()