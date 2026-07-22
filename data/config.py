import psycopg2

def get_connection():
    try:
        
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="alkindifrequence",
            user="postgres",
            password="E94L72assal"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None