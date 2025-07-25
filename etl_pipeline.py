# Importamos SparkSession para trabajar con DataFrames y Spark SQL
from pyspark.sql import SparkSession

# Importamos col para referenciar columnas en transformaciones
from pyspark.sql.functions import col

def main(input_path, output_curated, output_model=None):
    """
    Parámetros:
      input_path      -- Ruta al CSV de entrada (en S3, HDFS o local)
      output_curated  -- Ruta donde guardaremos los datos limpios en formato Parquet
      output_model    -- (Opcional) Ruta donde se guardará el modelo entrenado
    """

    # Creamos (o recuperamos) la sesión de Spark con nombre de aplicación "BanknoteETL"
    spark = SparkSession.builder \
        .appName("BanknoteETL") \
        .getOrCreate()

    # Leemos el archivo CSV con encabezado; devuelve un DataFrame de cadenas
    df = spark.read \
        .option("header", "true") \
        .csv(input_path)

    # Iniciamos la limpieza y conversión de tipos
    df_clean = (
        df
        # Convertimos cada columna numérica de string a tipo double o integer
        .withColumn("variance", col("variance").cast("double"))
        .withColumn("skewness", col("skewness").cast("double"))
        .withColumn("curtosis", col("curtosis").cast("double"))
        .withColumn("entropy", col("entropy").cast("double"))
        .withColumn("class",   col("class").cast("integer"))
        # Eliminamos filas donde variance sea null
        .filter(col("variance").isNotNull())
        # Filtramos solo las clases 0 y 1
        .filter((col("class") == 0) | (col("class") == 1))
    )

    # Escribimos el DataFrame limpio en formato Parquet, sobrescribiendo si existe
    df_clean.write \
        .mode("overwrite") \
        .parquet(output_curated)

    # ------------------------------
    # Sección opcional: entrenamiento
    # ------------------------------

    # Importamos clases de ML dentro de la función para acelerar el arranque
    from pyspark.ml.classification import LogisticRegression
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml import Pipeline

    # Preparamos un ensamblador de características: agrupa columnas en un vector
    assembler = VectorAssembler(
        inputCols=["variance", "skewness", "curtosis", "entropy"],
        outputCol="features"
    )

    # Definimos una regresión logística
    lr = LogisticRegression(
        featuresCol="features",
        labelCol="class",
        maxIter=10         # Número máximo de iteraciones
    )

    # Encadenamos ensamblador y regresión en un pipeline
    pipeline = Pipeline(stages=[assembler, lr])

    # Entrenamos el modelo usando el DataFrame limpio
    model = pipeline.fit(df_clean)

    # Si se especificó una ruta de salida para el modelo, lo guardamos en disco/S3
    if output_model:
        model.write().overwrite().save(output_model)

    # Cerramos la sesión de Spark para liberar recursos
    spark.stop()

# Punto de entrada cuando se ejecuta el script desde la línea de comandos
if __name__ == "__main__":
    import sys

    # sys.argv[1] → input_path
    # sys.argv[2] → output_curated
    # sys.argv[3] → output_model (opcional)
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None
    )
