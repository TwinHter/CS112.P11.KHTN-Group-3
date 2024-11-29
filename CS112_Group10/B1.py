import math
import time
import random
from multiprocessing import Pool, cpu_count

# Sinh danh sách số ngẫu nhiên
def generate_random_number(test_size):
    return [random.randint(10**9, 10**10) for _ in range(test_size)]

# Kiểm tra số nguyên tố tuần tự
def is_prime_sequential(x):
    if x <= 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(x)) + 1, 6):
        if x % i == 0 or x % (i + 2) == 0:
            return False
    return True

# Kiểm tra số nguyên tố song song (dừng sớm)
def is_prime_parallel(x):
    if x <= 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False

    sqrt_x = int(math.sqrt(x)) + 1
    num_processes = cpu_count()
    step = 1000  # Kích thước mỗi nhóm kiểm tra

    # Tạo các nhóm kiểm tra
    ranges = [(x, i, min(i + step, sqrt_x)) for i in range(5, sqrt_x, step)]

    with Pool(num_processes) as pool:
        for result in pool.imap_unordered(check_range, ranges):
            if not result:
                pool.terminate()
                return False
    return True

# Kiểm tra một đoạn nhỏ (song song hỗ trợ)
def check_range(args):
    x, start, end = args
    for i in range(start, end):
        if x % i == 0:
            return False
    return True

# Hàm chạy thử nghiệm
def main():
    # test_cases = [1000000000000091, 10000000000000099, 100000000000000049]
    # for x in test_cases:
    #     print(f"Testing for X = {x}")

    #     # Thực hiện tuần tự
    #     start_time = time.time()
    #     result_seq = is_prime_sequential(x)
    #     seq_time = time.time() - start_time
    #     print(f"Tuan tu: {result_seq}, Time: {seq_time:.6f}s")

    #     # Thực hiện song song
    #     start_time = time.time()
    #     result_par = is_prime_parallel(x)
    #     par_time = time.time() - start_time
    #     print(f"Song song: {result_par}, Time: {par_time:.6f}s")

    #     print(f"Phan tram toi uu: {seq_time / par_time:.2f}x\n")
    test_sizes = [10, 20, 50, 100, 200, 500]  # Số lượng test case
    for test_size in test_sizes:
        print(f"Testing for number of test cases = {test_size}")
        
        # Sinh danh sách số
        tests = generate_random_number(test_size)

        # Kiểm tra tuần tự
        start_time = time.time()
        results_seq = [is_prime_sequential(x) for x in tests]
        seq_time = time.time() - start_time
        print(f"Tuan tu: Time = {seq_time:.6f}s")

        # Kiểm tra song song (toàn bộ danh sách)
        start_time = time.time()
        with Pool(cpu_count()) as pool:
            results_par = pool.map(is_prime_sequential, tests)
        par_time = time.time() - start_time
        print(f"Song song: Time = {par_time:.6f}s")
        
        # Phần trăm tối ưu
        print(f"Phan tram toi uu: {seq_time / par_time:.2f}x\n")

if __name__ == "__main__":
    main()
