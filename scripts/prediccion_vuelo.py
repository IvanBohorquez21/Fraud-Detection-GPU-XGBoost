import joblib
import numpy as np
import os

# CONFIGURACIÓN DE RUTAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(BASE_DIR, '..', 'models', 'modelo_fraude_gpu.pkl')

if not os.path.exists(ruta_modelo):
    print("Error: No se encontró el archivo del modelo en la carpeta 'models'.")
else:
    modelo = joblib.load(ruta_modelo)
    print("--- Sistema de Monitoreo Activo (Modelo Cargado) ---")

    def evaluar(datos):
        pred = modelo.predict(datos)
        prob = modelo.predict_proba(datos)
        if pred[0] == 1:
            print(f"⚠️ ALERTA: Fraude (Probabilidad: {prob[0][1]:.2%})")
        else:
            print(f"✅ Segura (Riesgo: {prob[0][1]:.2%})")

    # Prueba con datos aleatorios
    print("\nSimulando transacción entrante...")
    test_data = np.random.rand(1, 30)
    evaluar(test_data)