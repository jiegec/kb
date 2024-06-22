# Apache Spark

## Installation

Follow https://spark.apache.org/downloads.html, download and extract

## Usage

- REPL: pyspark(Python), spark-shell(Scala)
- Job submission: `spark-submit code.py/code.jar`
- Run example: `run-example SparkPi`, `spark-submit examples/src/main/python/pi.py`

### Initialize

Create SparkSession to use SQL interface: https://spark.apache.org/docs/latest/sql-programming-guide.html

```scala
SparkSession.builder.appName("SimpleApp").getOrCreate()
```

Old RDD interface uses SparkContext: https://spark.apache.org/docs/latest/rdd-programming-guide.html

### Read data

Get Dataset/DataFrame from files:

- spark.read.load(path): infer file type
- spark.read.text(path)
- spark.read.json(path)

Or run SQL on files directly:

```scala
val sqlDF = spark.sql("SELECT * FROM parquet.`examples/src/main/resources/users.parquet`")
```

See more on https://spark.apache.org/docs/latest/sql-data-sources.html

### Store data

Save Dataset/DataFrame to files:

- df.write.save(path)

### Dataset

Supports functional programming, the functions transforms Dataset in to a new one.

Actions: extract values from Dataset

- count()
- first()
- collect()

Supports caching in memory: cache()

Execute raw SQL queries: `spark.sql(query)`, https://spark.apache.org/docs/latest/api/sql/

Register a Dataset as a temporary view in SQL: `df.createOrReplaceTempView(name)`