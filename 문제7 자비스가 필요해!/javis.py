import os
import sounddevice as sd
from scipy.io.wavfile import write
import datetime


class Recorder:
    def __init__(self):
        self.fs = 44100
        self.duration = 5  # seconds
        self.records_dir = 'records'
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)

    def record_voice(self):
        print('녹음 시작...')
        recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2)
        sd.wait()
        filename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(self.records_dir, filename)
        write(filepath, self.fs, recording)
        print(f'녹음 완료: {filepath}')

    def list_records_by_date(self, start_date, end_date):
        try:
            files = os.listdir(self.records_dir)
            for f in sorted(files):
                try:
                    date_str = f.split('.')[0]
                    file_date = datetime.datetime.strptime(date_str, '%Y%m%d-%H%M%S')
                    if start_date <= file_date <= end_date:
                        print(f)
                except Exception:
                    continue
        except FileNotFoundError:
            print('records 폴더가 없습니다.')


def main():
    recorder = Recorder()
    recorder.record_voice()

    # 보너스: 날짜 범위별 녹음 파일 보기
    user = input('녹음 파일 날짜 범위 보기를 원하십니까? (y/n): ')
    if user.lower() == 'y':
        try:
            start = input('시작 날짜 (YYYYMMDD): ')
            end = input('종료 날짜 (YYYYMMDD): ')
            start_dt = datetime.datetime.strptime(start, '%Y%m%d')
            end_dt = datetime.datetime.strptime(end, '%Y%m%d') + datetime.timedelta(days=1)  # 종료일까지 포함
            recorder.list_records_by_date(start_dt, end_dt)
        except Exception as e:
            print(f'날짜 형식 오류: {e}')


if __name__ == '__main__':
    main()
