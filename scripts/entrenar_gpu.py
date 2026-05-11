import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib
import os

# CONFIGURACIÓN DE RUTAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(BASE_DIR, '..', 'models', 'modelo_fraude_gpu.pkl')

try:
    print("Conectando a MySQL...")
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='deteccion_fraude')
    df = pd.read_sql("SELECT * FROM transacciones", conn)
    conn.close()

    X = df.drop(['id', 'clase'], axis=1)
    y = df['clase']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Aplicando SMOTE...")
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    print("--- Entrenando con XGBoost en la GPU (RTX 4060) ---")
    model_gpu = XGBClassifier(
        tree_method='hist',
        device='cuda',
        n_estimators=100,
        random_state=42
    )

    model_gpu.fit(X_train_res, y_train_res)
    
    # GUARDAR EL MODELO EN LA CARPETA MODELS
    joblib.dump(model_gpu, ruta_modelo)
    print(f"Modelo guardado exitosamente en: {ruta_modelo}")

    y_pred = model_gpu.predict(X_test)
    print("\nReporte de Clasificación:\n", classification_report(y_test, y_pred))

except Exception as e:
    print(f"Error durante el entrenamiento: {e}")