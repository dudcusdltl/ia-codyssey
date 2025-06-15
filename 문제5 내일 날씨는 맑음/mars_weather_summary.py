import pandas as pd
import mysql.connector
from mysql.connector import Error

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df = df.rename(columns={'stom': 'storm'})  # CSV 오타 수정
        return df
    except Exception as e:
        print(f'CSV 파일 로딩 오류: {e}')
        return None

def insert_data_to_mysql(df, host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        for _, row in df.iterrows():
            query = '''
            INSERT INTO mars_weather (mars_date, temp, storm)
            VALUES (%s, %s, %s)
            '''
            values = (row['mars_date'], row['temp'], row['storm'])
            cursor.execute(query, values)
        conn.commit()
        print('✅ 데이터 입력 완료')
    except Error as e:
        print(f'❌ MySQL 오류: {e}')
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def main():
    file_path = 'mars_weathers_data.CSV'  # 로컬에 있는 파일 경로
    df = load_csv(file_path)
    if df is not None:
        insert_data_to_mysql(
            df,
            host='localhost',
            user='root',
            password='your_password',   # 비밀번호 입력
            database='mars_db'
        )

if __name__ == '__main__':
    main()
