import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# CONFIGURACIÓN DE RUTAS RELATIVAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Sube un nivel y entra a 'data'
ruta_csv = os.path.join(BASE_DIR, '..', 'data', 'creditcard.csv')

try:
    # Conexión a XAMPP (MySQL)
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='deteccion_fraude'
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
        print(f"Leyendo archivo en: {os.path.abspath(ruta_csv)}")
        data = pd.read_csv(ruta_csv)
        
        # Cargamos las primeras 50,000 filas para optimizar espacio en SQL
        df = data.head(50000) 
        print(f"Cargando {len(df)} registros en la base de datos...")

        for i, row in df.iterrows():
            sql = """INSERT INTO transacciones (tiempo, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, 
                     v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, 
                     v26, v27, v28, monto, clase) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql, tuple(row))
        
        connection.commit()
        print("¡Éxito! Los datos se han cargado correctamente en MySQL.")

except Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")