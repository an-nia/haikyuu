from myLib import p1Settings2
import psycopg

def connect():
    conn= psycopg.connect(
        dbname=p1Settings2.POSTGRES_DB,
        user=p1Settings2.POSTGRES_USER,
        password=p1Settings2.POSTGRES_PASSWORD,
        host=p1Settings2.POSTGRES_HOST,
        port=p1Settings2.POSTGRES_PORT
        )
    print("Connected")
    return conn