import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CONFIGURACIÓN DE RUTAS RELATIVAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Opcional: Crear una carpeta para guardar las gráficas si quieres subirlas a GitHub
ruta_grafica = os.path.join(BASE_DIR, '..', 'distribucion_montos.png')

try:
    # 1. Conexión a la base de datos
    print("Conectando a MySQL para análisis exploratorio...")
    conn = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='', 
        database='deteccion_fraude'
    )

    # 2. Extracción de datos
    query = "SELECT * FROM transacciones"
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"Datos extraídos exitosamente: {len(df)} registros.")

    # 3. Visualización: ¿El monto influye en el fraude?
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='clase', y='monto', data=df)
    
    plt.title('Distribución de Montos: Legítimo (0) vs Fraude (1)')
    plt.xlabel('Clase (0: Legítimo, 1: Fraude)')
    plt.ylabel('Monto de la Transacción')
    
    # Limitamos el eje Y a 500 para evitar que los valores atípicos 
    # muy altos aplasten visualmente las "cajas"
    plt.ylim(0, 500) 

    # Guardar la imagen (útil para el README de tu GitHub)
    plt.savefig(ruta_grafica)
    print(f"Gráfica guardada en: {os.path.abspath(ruta_grafica)}")

    # Mostrar la gráfica en pantalla
    plt.show()

except Exception as e:
    print(f"Error en el análisis visual: {e}")