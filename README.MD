# 💳 Detección de Fraude en Tarjetas de Crédito con IA

Este proyecto implementa un sistema de clasificación binaria para detectar transacciones fraudulentas, optimizado mediante aceleración por hardware (GPU) y técnicas de tratamiento de datos desbalanceados.

## 🚀 Características Técnicas
- **Algoritmo:** XGBoost (eXtreme Gradient Boosting).
- **Aceleración:** Entrenamiento ejecutado en GPU NVIDIA RTX 4060 (CUDA).
- **Tratamiento de Datos:** Aplicación de SMOTE (Synthetic Minority Over-sampling Technique) para resolver el desequilibrio de clases.
- **Base de Datos:** Conexión directa con MySQL (XAMPP) para la extracción de datos.

## 📊 Resultados del Modelo
El modelo alcanzó un rendimiento excepcional en las métricas de negocio más críticas:
- **Recall (Clase 1):** 97% (Casi todos los fraudes son detectados).
- **Precisión (Clase 1):** 83%.
- **Falsos Negativos:** Solo 1 caso de fraude no detectado en el set de prueba.

## 🛠️ Instalación y Uso
1. Clonar el repositorio.
2. Crear entorno virtual: `python -m venv env`.
3. Activar entorno: `.\env\Scripts\Activate.ps1`.
4. Instalar dependencias: `pip install -r requirements.txt`.
5. Ejecutar predicción: `python scripts/prediccion_vuelo.py`.

## 📁 Estructura del Proyecto
- `/scripts`: Scripts de carga, entrenamiento y predicción.
- `/models`: Modelos serializados (.pkl).
- `/data`: Dataset original (vía Kaggle).