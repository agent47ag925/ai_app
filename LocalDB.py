import mariadb
import pandas as pd

# 데이터베이스 연결 정보
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "7496",
    "database": "EZEN",
    "local_infile": True  # 반드시 추가해야 함
}

#DB를 채움
#table : 
#data : 
def load_csv_with_infile(csv_file, table):
    conn = mariadb.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # CSV 파일 읽기
    # skiprows=1, # 첫 번째 행은 헤더이므로 건너뜀
    # hearer = None #따로 열이름 지정하지 않는다
    #encoding에 문제가 있으실 경우 cp949, UTF-8 등으로 값을 변경해서 써 보세요.
    df = pd.read_csv(csv_file, encoding='UTF-8', delimiter=',')  
    column_names = ','.join([x for x in df.columns])
    print(df)

    command = ''
    for i in range(len(df.columns)):
        type = df.iloc[:][df.columns[i]].dtypes

        try:
            if 'int' in str(type).lower():
                command += str(df.columns[i]) + ' INT'
            
            elif 'float' in str(type).lower():
                command += str(df.columns[i]) + ' FLOAT'
            
            elif 'date' in df.columns[i] :
                command += str(df.columns[i]) + ' DATE'

            else:
                command += str(df.columns[i]) + ' VARCHAR(100)'

        finally:
            if i == len(df.columns)-1:
                command += ''
            else:
                command += ', \n'


    repeat = '('
    repeat += ','.join(['%s' for x in range(len(df.columns))])
    repeat += ')'
    print(repeat)

    try:
        #데이터 삽입
        #테이블 명이 이미 있으면 동작하지 않음음
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table}
        ({command});""")
        
        for _, row in df.iterrows():
            cur.execute(f"""
                INSERT INTO {table} ({column_names}) VALUES {repeat};""", tuple(row))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ 데이터 삽입 완료!")
    except mariadb.Error as e:
        cur.close()
        conn.close()
        print(f"❌ 삽입 실패: {e}")


#database 안에 있는 하나의 테이블의 데이터를 조회할 수 있다.
def show_data(table):
    conn = None
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 데이터 조회
        cur.execute(f"SELECT * FROM {table}")
        columns = [x[0] for x in cur.description]
        #print(columns)
        #print(len(columns))

        rows = cur.fetchall()
        #print(str(rows[0]))
        result = []

        datetime_indexes = [i for i, value in enumerate(rows[0]) if isinstance(value, (datetime.date, datetime.datetime))]
        if datetime_indexes:
            datetime_columns = [(columns[i], i) for i in datetime_indexes]

        if rows != None:
            for r in rows:
                new_row = []
                for j, v in enumerate(r):
                    if j == 9:
                        val = v.strftime("%Y:%m:%d")
                        #print(val)
                    else:
                        val = v
                
                    new_row.append(val)
                result.append(new_row)
        
        result = pd.DataFrame(result, columns=columns)
        return result

    except mariadb.Error as e:
        print(f"❌ 데이터 조회 실패: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == '__main__':
    #여기에 다운로드받은 sql_into_input.csv 파일의 경로를 입력해줌
    #csv_file, table, data
    #csv_file은 csv 파일 경로
    #table은 데이터베이스의 테이블 이름 -> 겹치는 이름이 있으면 안됨됨
    #data는 비워놓아도 됨됨
    path = 'C:/Users/jeong/Desktop/temp/sql_auto_input.csv'
    load_csv_with_infile(path, 'temp_data')