import math
import time
import random
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor



# Kiểm tra số nguyên tố tuần tự
def is_prime(x):
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

# Hàm xử lý một nhóm số
def process_chunk(chunk):
    return [is_prime(x) for x in chunk]

# Hàm kiểm tra danh sách số song song
def check_primes_parallel(numbers):
    num_processes = 4  # Số tiến trình
    chunk_size = len(numbers) // num_processes  # Kích thước mỗi nhóm
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(is_prime, numbers))
    return results
    # return [item for sublist in results for item in sublist]  # Gộp kết quả

# Hàm kiểm tra danh sách số tuần tự
def check_primes_sequential(numbers):
    return [is_prime(x) for x in numbers]

# Chạy thử nghiệm
def main():
    test_sizes = [10, 20, 50, 100, 200, 500]  # Số lượng test case
    for test_size in test_sizes:
        print(f"Testing for number of test cases = {test_size}")
        
        # Sinh danh sách số ngẫu nhiên
        tests = [random.randint(10**9, 10**10) for _ in range(test_size)]

        # Kiểm tra tuần tự
        start_time = time.time()
        results_seq = check_primes_sequential(tests)
        seq_time = time.time() - start_time
        print(f"Tuan tu: Time = {seq_time:.6f}s")

        # Kiểm tra song song
        start_time = time.time()
        results_par = check_primes_parallel(tests)
        par_time = time.time() - start_time
        print(f"Song song: Time = {par_time:.6f}s")

        # Phần trăm tối ưu
        print(f"Phan tram toi uu: {seq_time / par_time:.2f}x\n")

if __name__ == "__main__":
    main()
