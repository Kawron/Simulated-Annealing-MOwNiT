if __name__=="__main__":
    from zad2 import main
    from multiprocessing import *

    for i in range(1,6):
        p = Process(target=main, args=(i,))
        p.start()