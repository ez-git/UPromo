
"""
Get URLs from DB
"""
def get_urls():
    con = psycopg2.connect(
        database="upromo_main",
        user="postgres",
        password="Zxcvbnm0+",
        host="127.0.0.1",
        port="5432"
    )

    return 'urls'
