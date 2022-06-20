# Importación del módulo
import os, psycopg2, config

def get_db_connection():
    conn = psycopg2.connect(
        user = os.getenv("DATABASE_USERNAME"),                                      
        password = os.getenv("DATABASE_PASSWORD"),                                 
        host = os.getenv("HOST"),                                            
        port = os.getenv("DATABASE_PORT"),                                          
        database = os.getenv("DATABASE_NAME"))
    return conn

'''
# Open a cursor to perform databse operations
cur = conn.cursor()

sql='SELECT * FROM usuario'
cur.execute(sql)

#PRUEBA
registro=cur.fetchall()
print(registro)

conn.commit()

cur.close()
conn.close()
'''


