import psycopg2

con = psycopg2.connect(
    database='upromo_main',
    user="postgres",
    password="Zxcvbnm0+",
    host="127.0.0.1",
    port="5432"
)

cur = con.cursor()


"""
нужна дата обновления и туда и туда
нужна ссылка на канал
"""

cur.execute('''CREATE TABLE PROMOS  
     (LINK TEXT PRIMARY KEY NOT NULL,
     UPDATE_DATE DATE,
     RELEASE_DATE DATE,
     CHANNEL TEXT,
     PROMO TEXT NOT NULL
     FULL_PROMO TEXT NOT NULL);''')

cur.execute('''CREATE TABLE CH_LIST  
     (LINK TEXT PRIMARY KEY NOT NULL,
     UPLOAD_DATE DATE
     UPDATE_DATE DATE);''')

con.commit()
con.close()
