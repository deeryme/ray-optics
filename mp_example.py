# Example of using mp library
from multiprocessing import Pool
import time 

def fn(names_list):
    for elem in enumerate(names_list):
        print(f"({elem[0]},{elem[1]})")

if __name__ == '__main__':
    names = ['Abe', 'Ben', 'Cal', 'Dan', 'Emi']
    start_t = time.perf_counter()
    names_list = list(enumerate(names))
    print(names_list)
    with Pool() as pool:
        pool.map(fn, names_list)
    end_t = time.perf_counter()
    print(f"Elapsed time: {end_t-start_t:.6f} seconds")