import random
import time
import platform
import os

try:
    import psutil
except ImportError:
    print('psutil 모듈이 설치되어 있지 않습니다. 시스템 부하 정보를 가져올 수 없습니다.')
    psutil = None

import msvcrt  # Windows 키 입력 감지용

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        return self.env_values

class MissionComputer:
    def __init__(self):
        self.sensor = DummySensor()
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.history = []
        self.save_system_info()  # ✅ 프로그램 실행 시 시스템 정보 저장

    def save_system_info(self):
        """시스템 정보를 setting.txt 파일에 저장"""
        try:
            with open('setting.txt', 'w', encoding='utf-8') as f:
                f.write('=== Mission Computer System Info ===\n')
                f.write(f'운영체제 = {platform.system()}\n')
                f.write(f'운영체제버전 = {platform.version()}\n')
                f.write(f'CPU타입 = {platform.processor()}\n')
                f.write(f'CPU코어수 = {os.cpu_count()}\n')
                if psutil:
                    memory_size = round(psutil.virtual_memory().total / (1024 ** 3), 2)
                    f.write(f'메모리크기 = {memory_size} GB\n')
                else:
                    f.write('메모리크기 = Unavailable (psutil not installed)\n')
        except Exception as e:
            print('setting.txt 파일에 시스템 정보를 저장하는 중 오류가 발생했습니다:', e)

    def get_sensor_data(self):
        """센서 데이터를 5초마다 가져와 출력하고 5분마다 평균 출력"""
        start_time = time.time()

        while True:
            self.sensor.set_env()
            sensor_data = self.sensor.get_env()

            for key in self.env_values:
                self.env_values[key] = sensor_data[key]

            print('{')
            for key, value in self.env_values.items():
                print(f'  "{key}": {value},')
            print('}')

            self.history.append(self.env_values.copy())

            if (time.time() - start_time) >= 300:
                self.print_average()
                self.history = []
                start_time = time.time()

            print('중지하려면 엔터를 누르세요. 계속하려면 아무것도 입력하지 말고 기다리세요.')
            if self.check_user_input():
                print('System stopped...')
                break

            time.sleep(5)

    def print_average(self):
        """5분 평균 출력"""
        if not self.history:
            return

        print('\n[5분 평균 환경 데이터]')
        avg_values = {}
        count = len(self.history)

        for key in self.env_values:
            total = sum(item[key] for item in self.history)
            avg = total / count
            avg_values[key] = avg

        print('{')
        for key, value in avg_values.items():
            print(f'  "{key}": {value:.2f},')
        print('}\n')

    def check_user_input(self):
        """Windows용 키 입력 대기"""
        print('5초 동안 키 입력 대기 중...')
        start = time.time()
        while time.time() - start < 5:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\r':
                    return True
            time.sleep(0.1)
        return False

    def get_mission_computer_info(self):
        """미션 컴퓨터 시스템 정보 출력"""
        print('\n[Mission Computer Info]')
        info = {}

        try:
            info['OS'] = platform.system()
            info['OS Version'] = platform.version()
            info['CPU'] = platform.processor()
            info['CPU Core Count'] = os.cpu_count()
            if psutil:
                info['Memory Size (GB)'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
            else:
                info['Memory Size (GB)'] = 'Unavailable (psutil not installed)'
        except Exception as e:
            print('시스템 정보를 가져오는 중 오류가 발생했습니다:', e)

        print('{')
        for key, value in info.items():
            if isinstance(value, str):
                print(f'  "{key}": "{value}",')
            else:
                print(f'  "{key}": {value},')
        print('}')

    def get_mission_computer_load(self):
        """미션 컴퓨터 부하 정보 출력"""
        print('\n[Mission Computer Load]')
        load = {}

        try:
            if psutil:
                load['CPU Usage (%)'] = psutil.cpu_percent(interval=1)
                load['Memory Usage (%)'] = psutil.virtual_memory().percent
            else:
                print('psutil 모듈이 없어 부하 정보를 가져올 수 없습니다.')
        except Exception as e:
            print('시스템 부하 정보를 가져오는 중 오류가 발생했습니다:', e)

        if load:
            print('{')
            for key, value in load.items():
                print(f'  "{key}": {value},')
            print('}')
        else:
            print('{}')

# 인스턴스 생성
runComputer = MissionComputer()

# 시스템 정보 출력
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()

