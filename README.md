# 📌 Banknote Authentication ETL with PySpark & AWS (Free Tier)

## 📝 Descripción del Proyecto

Un pipeline ETL completo desarrollado con PySpark, que procesa datos del dataset **Banknote Authentication** (UCI / Kaggle) en un entorno profesional basado en AWS (nivel gratuito).  
El flujo incluye:

- Lectura desde **AWS S3**
- Limpieza y transformación de datos
- Entrenamiento de modelo de clasificación (Logistic Regression u otros)
- Almacenamiento de resultados en formato **Parquet**
- Consultas en **Athena**
- Pruebas automatizadas para garantizar calidad y rendimiento

---

## 🎯 Objetivo

Construir una solución técnica reproducible que demuestre dominio en:

- Procesamiento distribuido
- Modelado predictivo
- Orquestación en AWS
- Buenas prácticas de ingeniería de datos y software

---

## 🧰 Tecnologías utilizadas

- **PySpark (Spark 3.x)**: para ETL y Machine Learning
- **AWS Free Tier**:
  - Amazon S3
  - EMR (t2.micro o local)
  - Athena
  - CloudWatch
- **Parquet** como formato de salida
- **pytest** para validación y pruebas unitarias
- *(Opcional)* Great Expectations o PyDeequ para chequeo de calidad de datos
- *(Opcional)* EventBridge o Step Functions para orquestación

---

## 🚀 Flujo del pipeline

1. **Ingesta**: carga de `BankNoteAuthentication.csv` a `s3://<tu-bucket>/raw/`
2. **ETL Spark**:
   - Casteo de tipos
   - Filtrado de clases válidas
   - Ensamble de features
3. **Modelado ML**:
   - Pipeline con ensamblado, escalado y regresión logística
4. **Salida**: escritura de resultados curados en `s3://<tu-bucket>/curated/` en formato Parquet
5. **Consultas**: ejecución de SQL en Athena sobre los datos curados
6. **Monitoreo**: logs de ejecución con CloudWatch
7. **Automatización** *(opcional)*: EventBridge / Step Functions / Control-M
8. **Validación**: pruebas con PyTest y calidad con herramientas como Great Expectations

---
## 📈 Métricas y resultados esperados

- Precisión esperada del modelo > 95 %
- Conteos por clase y matriz de confusión consultables desde Athena
- Reportes de calidad: nulos, duplicados, rangos válidos
- Logs de ejecución y performance desde EMR/CloudWatch

---

## 🧾 ¿Por qué incluir este proyecto en tu portafolio?

- Demuestra experiencia en **PySpark**, **AWS S3/EMR/Athena**
- Caso real de **ETL + ML** de inicio a fin
- Incluye pruebas, validaciones y automatización
- Base sólida para despliegue en producción
- Enfatiza habilidades clave requeridas por **Bluetab**:
  - Interpretación de datos
  - Arquitectura distribuida
  - Calidad, testing, CI/CD y documentación clara
