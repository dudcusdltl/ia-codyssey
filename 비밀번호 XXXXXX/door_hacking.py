import zipfile
import time
import string
import itertools
import multiprocessing


def attempt_password(pw_chunk, zip_path, result_queue):
    try:
        zip_file = zipfile.ZipFile(zip_path)
    except:
        result_queue.put(None)
        return

    for pw in pw_chunk:
        try:
            zip_file.extractall(pwd=bytes(pw, 'utf-8'))
            result_queue.put(pw)
            return
        except:
            continue
    result_queue.put(None)


def generate_passwords(charset, length):
    for pw_tuple in itertools.product(charset, repeat=length):
        yield ''.join(pw_tuple)


def unlock_zip():
    charset = string.digits + string.ascii_lowercase
    zip_path = 'emergency_storage_key.zip'
    output_file = 'password.txt'
    max_attempts_per_worker = 10000
    num_workers = multiprocessing.cpu_count()

    print('병렬로 암호 해제를 시작합니다...')
    start_time = time.time()
    attempts = 0

    pw_generator = generate_passwords(charset, 6)
    result_queue = multiprocessing.Queue()
    found = False

    while not found:
        chunk_list = []
        for _ in range(num_workers):
            chunk = list(itertools.islice(pw_generator, max_attempts_per_worker))
            if not chunk:
                break
            chunk_list.append(chunk)

        if not chunk_list:
            break

        processes = []
        for chunk in chunk_list:
            p = multiprocessing.Process(target=attempt_password, args=(chunk, zip_path, result_queue))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        while not result_queue.empty():
            result = result_queue.get()
            if result:
                elapsed = time.time() - start_time
                print(f'성공! 암호: {result}')
                print(f'걸린 시간: {elapsed:.2f}초')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                found = True
                break

        attempts += num_workers * max_attempts_per_worker
        print(f'{attempts}회 시도 중... 경과 시간: {time.time() - start_time:.2f}초')

    if not found:
        print('실패: 암호를 찾지 못했습니다.')


if __name__ == '__main__':
    unlock_zip()
