import random

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
        """환경 값을 랜덤으로 설정"""
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_time(self):
        """🌟 실행할 때마다 랜덤하게 시간이 증가"""
        mars_day = 1 + self.mars_minutes_passed // (24 * 60)
        mars_hour = (self.mars_minutes_passed // 60) % 24
        mars_minute = self.mars_minutes_passed % 60
        return f"화성일 {mars_day} - {mars_hour:02d}:{mars_minute:02d}"

    def get_env(self):
        """환경 값을 반환하고 로그 파일에 한 줄씩 기록"""
        log_file = 'mars_env_log.txt'
        data = self.env_values
        mars_time = self.get_time()

        log_entry = f"[{mars_time}] Log Entry #{self.log_count} | 내부온도: {data['mars_base_internal_temperature']}°C | "
        log_entry += f"외부온도: {data['mars_base_external_temperature']}°C | 내부습도: {data['mars_base_internal_humidity']}% | "
        log_entry += f"외부광량: {data['mars_base_external_illuminance']}W/m² | CO₂: {data['mars_base_internal_co2']}% | "
        log_entry += f"O₂: {data['mars_base_internal_oxygen']}%\n"

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                is_empty = f.read() == ''
        except FileNotFoundError:
            is_empty = True

        with open(log_file, 'a', encoding='utf-8') as f:
            if is_empty:
                f.write("=== 화성 기지 환경 로그 ===\n")
                f.write("시간 | 로그 번호 | 내부온도(°C) | 외부온도(°C) | 내부습도(%) | 외부광량(W/m²) | CO₂(%) | O₂(%)\n")
                f.write("-" * 100 + "\n")
            f.write(log_entry)

        self.log_count += 1  
        self.mars_minutes_passed += random.randint(1, 10)  # ✅ 🌟 1~10분 사이에서 랜덤 증가
        return data

# ✅ 실행 예시 (랜덤 시간 증가)
ds = DummySensor()

ds.set_env()
print(ds.get_env())  # 디버그 1번 실행

ds.set_env()
print(ds.get_env())  # 디버그 2번 실행 (랜덤 시간 증가)

ds.set_env()
print(ds.get_env())  # 디버그 3번 실행 (랜덤 시간 증가)
