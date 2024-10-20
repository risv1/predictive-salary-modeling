from pyspark.sql import SparkSession
import os
import glob

output_dir = "/app/output"

def check_directory_contents(path, level=0):
    """Recursively check directory contents"""
    indent = "  " * level
    print(f"{indent}Checking directory: {path}")
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"{indent}- DIR: {item}")
                check_directory_contents(item_path, level + 1)
            else:
                print(f"{indent}- FILE: {item}")
    else:
        print(f"{indent}Directory does not exist: {path}")

print("Initial directory check:")
check_directory_contents(output_dir)

spark = SparkSession.builder \
    .appName("HDFS Connector") \
    .master("spark://spark:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.hadoop.dfs.namenode.rpc-address", "namenode:9870") \
    .config("spark.hadoop.dfs.namenode.servicerpc-address", "namenode:9870") \
    .config("spark.hadoop.ipc.client.connect.timeout", "60000") \
    .config("spark.hadoop.ipc.client.connect.max.retries", "10") \
    .getOrCreate()

try:
    input_path = "hdfs://namenode:9000/user/root/input.csv"
    print(f"Reading from input path: {input_path}")
    
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    print("Successfully read the dataframe:")
    df.show()
    print(f"Number of rows in dataframe: {df.count()}")
    
    df.createOrReplaceTempView("employee_data")
    
    output_path1 = os.path.join(output_dir, "data.csv")
    output_path2 = os.path.join(output_dir, "backup")
    
    print(f"\nAttempting write method 1 - Direct to CSV file:")
    df.coalesce(1) \
      .write \
      .mode("overwrite") \
      .option("header", "true") \
      .option("delimiter", ",") \
      .csv(output_path1)
    
    print(f"\nAttempting write method 2 - To backup directory:")
    df.coalesce(1) \
      .write \
      .mode("overwrite") \
      .option("header", "true") \
      .option("delimiter", ",") \
      .format("csv") \
      .save(output_path2)
    
    print("\nChecking for generated files:")
    check_directory_contents(output_dir)
    
    print("\nChecking for hidden directories and files:")
    for root, dirs, files in os.walk(output_dir):
        for d in dirs:
            print(f"Found directory: {os.path.join(root, d)}")
        for f in files:
            print(f"Found file: {os.path.join(root, f)}")
            
    print("\nAttempting to read back written files:")
    try:
        written_files = glob.glob(f"{output_dir}/**/*.csv", recursive=True)
        print(f"Found CSV files: {written_files}")
        if written_files:
            test_df = spark.read.csv(written_files[0], header=True)
            print("Successfully read back the data:")
            test_df.show(5)
    except Exception as e:
        print(f"Error reading back files: {str(e)}")
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
finally:
    spark.stop()

print(f"\nScript completed. Check the output at {output_dir}")