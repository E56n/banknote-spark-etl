# Importamos pytest para definir fixtures y tests
import pytest

# Importamos SparkSession para crear sesiones de Spark en los tests
from pyspark.sql import SparkSession

# Importamos col para referenciar columnas en nuestras transformaciones y filtros
from pyspark.sql.functions import col

@pytest.fixture(scope="module")
def spark():
    """
    Fixture de PyTest que inicializa una SparkSession compartida
    para todos los tests de este módulo.

    scope="module" asegura que la sesión se cree una sola vez
    y se reutilice en cada test, optimizando el arranque.
    """
    return (
        SparkSession
        .builder
        .master("local[*]")       # Ejecuta Spark local con tantos hilos como núcleos
        .appName("TestETL")       # Nombre de la aplicación para identificar logs
        .getOrCreate()            # Crea o reutiliza la sesión existente
    )

def test_cast_and_filter(spark):
    """
    Verifica que:
      1. Al filtrar 'variance' nula, solo quede la fila válida.
      2. El tipo de dato de 'variance' en la fila resultante sea float.
    """
    # Datos de muestra: 
    # - Primera tupla con variance válido (1.2)
    # - Segunda tupla con variance None (debe eliminarse)
    data = [
        (1.2, 2.3, 0.5,  -1.2, 0),
        (None, 3.4, 1.1,  0.2, 1)
    ]

    # Creamos un DataFrame con nombres de columna explícitos
    df = spark.createDataFrame(
        data,
        ["variance", "skewness", "curtosis", "entropy", "class"]
    )

    # Aplicamos filtro para eliminar filas donde 'variance' sea null
    df2 = df.filter(col("variance").isNotNull())

    # Assert 1: Solo debe quedar una fila después del filtro
    assert df2.count() == 1

    # Recuperamos la única fila resultante
    row = df2.first()

    # Assert 2: Comprobamos que 'variance' ya sea float, no None ni otro tipo
    assert isinstance(row["variance"], float)
