package com.example;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.SparkConf;
import org.apache.spark.sql.SparkSession;

public class App {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("SparkJob").setMaster("local");
        JavaSparkContext sc = new JavaSparkContext(conf);
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        JavaRDD<String> input = sc.textFile("data/input.txt");

        JavaRDD<String> processedData = input.map(String::toUpperCase);

        processedData.saveAsTextFile("data/processed.txt");

        sc.close();
    }
}