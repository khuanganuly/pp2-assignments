def get_connection():
    import psycopg2
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="dar_postgre08"
    )