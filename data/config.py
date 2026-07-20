import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="alkindifrequence",
        user="postgres",
        password="E94L72assal"
    )
    return conn