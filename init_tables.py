
import psycopg2

db_name = 'upromo_main'
user

def get_urls():
    con = psycopg2.connect(
        database=db_name,
        user="postgres",
        password="Zxcvbnm0+",
        host="127.0.0.1",
        port="5432"
    )

    return 'urls'
