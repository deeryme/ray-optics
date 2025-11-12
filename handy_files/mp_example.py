# Example of using mp library
from multiprocessing import Pool
import time 

def my_str_fn(idx, val):
    return f"IDX = {idx}, VAL = {val}"

if __name__ == '__main__':
    names = ['Abe', 'Ben', 'Cal', 'Dan', 'Emi']
    start_t = time.perf_counter()
    names_list = list(enumerate(names))
    # print(names_list)
    with Pool() as pool:
        results = pool.starmap(my_str_fn, names_list)
    end_t = time.perf_counter()
    print(f"Elapsed time: {end_t-start_t:.6f} seconds")
    print(f"Results (len={len(results)}):")
    print(results)
