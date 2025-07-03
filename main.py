import pandas as pd
import psycopg2
import openpyxl

#1. Create 'students' table in your PosrgreSQL database in python script.
# It must have id which is PK and auto incremented.

conn = psycopg2.connect(database="new_db",
                        user="postgres",
                        password="gohome25",
                        host="localhost",
                        port=5432)
df = pd.read_excel("students.xlsx")
df['phone number'] = df['phone number'].apply(
    lambda x: str(int(float(x))) if pd.notna(x) else ''
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        student_name VARCHAR(64),
        age INT,
        average_mark FLOAT,
        gender CHAR(1),
        phone_number VARCHAR(64)
    );
""")

#2. Collect data from students.xlsx and write it into the text format file (.txt/.csv).

with open("textfile.txt", "w", encoding="utf-8") as f:
    f.write(df.to_string())

#3. Remove rows where 'average mark' is missing.

new_df = df.dropna()
print(new_df.to_string())

#4. Separate 'student name' into 'first name' and 'second name'.

df[['first_name', 'second_name']] = df['student name'].str.split(' ', n=1, expand=True)

#5. Database name, table name, file path and other constant variables ought
# to be stored in separate .json or .yaml file.

import yaml

data = {
    'db_name': 'new_db',
    'table name': 'students',
    'file_path': 'PycharmProjects\PythonProject7\Python_task\students.xlsx',
    'server_name': 'katet'
}

with open('data.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


#6. Insert data into the 'students' table in your DB.
cur.execute("""
    ALTER TABLE students
    ADD COLUMN first_name VARCHAR(64),
    ADD COLUMN second_name VARCHAR(64);
""")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO students (student_name, age, average_mark, gender, phone_number, first_name, second_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['student name'], row['age'], row['average mark'], row['gender'], row['phone number'], row['first_name'], row['second_name']))

conn.commit()

#7. Count number of male students with 'average mark' > 5 and female students with 'average mark' > 5
# and select this data from DB. Write this data into DataFrame data type varibale and print it.

cur.execute('''SELECT gender, COUNT(*) AS gender_count
               FROM students
               WHERE average_mark > 5
               GROUP BY gender''')

results = cur.fetchall()
df_gender_count = pd.DataFrame(results, columns=['gender', 'gender_count'])
print(df_gender_count)