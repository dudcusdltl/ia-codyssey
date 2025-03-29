import random
from datetime import datetime

class DummySensor:
    def __init__(self):
        # 환경 값 저장을 위한 사전 객체 생성
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        # 주어진 범위 내에서 랜덤 값 설정
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        # 현재 시간 추가
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 값 출력
        print(f'\n[{current_time}] 환경 값:')
        for key, value in self.env_values.items():
            print(f'{key}: {value:.2f}')
        
        # 로그 파일 저장
        with open('mars_mission_log.txt', 'a', encoding='utf-8') as f:
            log_entry = f'{current_time}, ' + ', '.join(f'{value:.2f}' for value in self.env_values.values()) + '\n'
            f.write(log_entry)

        return self.env_values

# 인스턴스 생성
ds = DummySensor()

# 값 설정 및 출력
ds.set_env()
env = ds.get_env()
