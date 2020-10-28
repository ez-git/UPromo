
import psycopg2

db_name = 'upromo_main'

    con = psycopg2.connect(
        database=db_name,
        user="postgres",
        password="Zxcvbnm0+",
        host="127.0.0.1",
        port="5432"
    )

cur.execute('''CREATE TABLE PROMOS  
     (LINK TEXT PRIMARY KEY NOT NULL,
     DATE DATE,
     PROMO TEXT NOT NULL);''')

cur.execute('''CREATE TABLE CHLIST  
     (LINK TEXT PRIMARY KEY NOT NULL);''')

con.commit()
con.close()
