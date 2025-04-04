import random
import time
import sys

# 윈도우 키 입력 감지용
import msvcrt

class DummySensor:
    log_count = 1  
    mars_minutes_passed = 0  

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

    def get_sensor_data(self):
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
        """Windows용 키 입력 감지"""
        print('5초 동안 키 입력 대기 중...')
        start = time.time()
        while time.time() - start < 5:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\r':  # 엔터 키
                    return True
            time.sleep(0.1)
        return False

# 인스턴스 생성
RunComputer = MissionComputer()
RunComputer.get_sensor_data()


