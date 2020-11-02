import psycopg2

con = psycopg2.connect(
    database='upromo_main',
    user="postgres",
    password="Zxcvbnm0+",
    host="127.0.0.1",
    port="5432"
)

cur = con.cursor()

cur.execute('''CREATE TABLE PROMOS  
     (LINK TEXT PRIMARY KEY NOT NULL,
     RELEASE_DATE FLOAT,
     PROMO TEXT NOT NULL);''')

cur.execute('''CREATE TABLE CH_LIST  
     (LINK TEXT PRIMARY KEY NOT NULL,
     UPDATE_DATE FLOAT );''')

con.commit()
con.close()
