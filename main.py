print('Hello Mars')

file_path = r"C:\Users\min99\Downloads\mission_computer_main.log"

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())