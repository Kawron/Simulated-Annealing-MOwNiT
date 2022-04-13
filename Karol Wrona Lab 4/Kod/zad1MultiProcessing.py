if __name__=="__main__":
    from zad1 import main
    from multiprocessing import *

    for i in range(1,4):
        p = Process(target=main, args=(i,))
        p.start()