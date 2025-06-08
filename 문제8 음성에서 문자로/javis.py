import os
import speech_recognition as sr
import csv

# records 디렉토리 내의 모든 WAV 파일을 가져오는 함수
def get_recorded_files(directory='records'):
    return [f for f in os.listdir(directory) if f.endswith('.wav')]

# STT로 음성 파일을 텍스트로 변환하고 CSV로 저장하는 함수
def transcribe_and_save_to_csv(filepath):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(filepath)
    try:
        with audio_file as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        timestamp = '00:00:00'  # 단일 블록 인식일 경우 시간은 고정
        csv_filename = filepath.replace('.wav', '.csv')
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Recognized Text'])
            writer.writerow([timestamp, text])
        return csv_filename, text
    except Exception as e:
        return None, f'Error processing {filepath}: {e}'

# CSV 파일 내 텍스트에서 키워드를 검색하는 함수
def search_keyword_in_csvs(keyword, directory='records'):
    results = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            filepath = os.path.join(directory, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # skip header
                    for row in reader:
                        if keyword.lower() in row[1].lower():
                            results.append((file, row[0], row[1]))
            except Exception as e:
                results.append((file, 'Error', str(e)))
    return results

# 실행 예시
recorded_files = get_recorded_files()
stt_results = []
for file in recorded_files:
    full_path = os.path.join('records', file)
    csv_file, result = transcribe_and_save_to_csv(full_path)
    stt_results.append((csv_file, result))

print('\n--- STT 결과 요약 ---')
for row in stt_results:
    print(row)
