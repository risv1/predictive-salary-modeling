from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HDFS Connector") \
    .master("spark://spark:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.hadoop.dfs.namenode.rpc-address", "namenode:9870") \
    .config("spark.hadoop.dfs.namenode.servicerpc-address", "namenode:9870") \
    .config("spark.hadoop.ipc.client.connect.timeout", "60000") \
    .config("spark.hadoop.ipc.client.connect.max.retries", "10") \
    .getOrCreate()

input_path = "hdfs://namenode:9000/user/root/input.csv"

df = spark.read.csv(input_path, header=True, inferSchema=True)
df.show()