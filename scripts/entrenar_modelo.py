import pandas as pd
import mysql.connector
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# CONFIGURACIÓN DE RUTAS RELATIVAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Definimos dónde se guardarán los archivos en la carpeta 'models'
ruta_modelo = os.path.join(BASE_DIR, '..', 'models', 'modelo_fraude_final.pkl')
ruta_scaler = os.path.join(BASE_DIR, '..', 'models', 'escalador_fraude.pkl')

try:
    # 1. Carga y preparación
    print("Conectando a MySQL para entrenamiento tradicional...")
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='deteccion_fraude')
    df = pd.read_sql("SELECT * FROM transacciones", conn)
    conn.close()

    X = df.drop(['id', 'clase'], axis=1)
    y = df['clase']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # El Random Forest requiere escalado de datos para funcionar óptimamente
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- MODELO 1: Random Forest Estándar ---
    print("\n--- Entrenando Random Forest Estándar (CPU) ---")
    rf_base = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # n_jobs=-1 usa todos los núcleos del CPU
    rf_base.fit(X_train_scaled, y_train)
    y_pred_base = rf_base.predict(X_test_scaled)

    print("Resultados Estándar:")
    print(classification_report(y_test, y_pred_base))

    # --- MODELO 2: Random Forest + SMOTE ---
    print("\n--- Aplicando SMOTE y entrenando Modelo con Balanceo ---")
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train_scaled, y_train)

    rf_smote = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_smote.fit(X_train_res, y_train_res)
    y_pred_smote = rf_smote.predict(X_test_scaled)

    print("Resultados con SMOTE:")
    print(classification_report(y_test, y_pred_smote))

    print("\nMatriz de Confusión (SMOTE):")
    print(confusion_matrix(y_test, y_pred_smote))

    # 2. Guardar el modelo y el escalador en la carpeta 'models'
    joblib.dump(rf_smote, ruta_modelo)
    joblib.dump(scaler, ruta_scaler)

    print(f"\n¡Éxito!")
    print(f"Modelo guardado en: {os.path.abspath(ruta_modelo)}")
    print(f"Escalador guardado en: {os.path.abspath(ruta_scaler)}")

except Exception as e:
    print(f"Error en el entrenamiento de CPU: {e}")