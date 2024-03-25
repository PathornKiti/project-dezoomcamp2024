from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.functions import col, udf,month,when
from pyspark.sql.types import BooleanType,StringType

def get_season(month):
    if month in range(3, 7):  # March to June: Summer
        return 'Summer'
    elif month in range(7, 11):  # July to October: Monsoon
        return 'Monsoon'
    else:  # November to February: Winter
        return 'Winter'


def main():
    spark = SparkSession \
            .builder \
            .appName('spark-bigquery') \
            .getOrCreate()
    bucket = "dataproc-staging-asiasoutheast1-626484338807-1lyhkan9"
    spark.conf.set('temporaryGcsBucket', bucket)
    #Get Data
    cal = spark.read.format('bigquery') \
            .option('table', 'airbnb_bkk_warehouse.native_cal') \
            .load()
    review = spark.read.format('bigquery') \
            .option('table', 'airbnb_bkk_warehouse.native_review') \
            .load()
    list = spark.read.format('bigquery') \
        .option('table', 'airbnb_bkk_warehouse.native_list') \
        .load()
    neighbour = spark.read.csv("neighbour_data.csv", header=True)

    #Transform
    review = review.drop('__index_level_0__')
    joined= review.join(neighbour, 'listing_id', how='left')


    get_season_udf = udf(get_season, StringType())
    cal = cal.withColumn('month', month('date'))
    cal = cal.withColumn('season', get_season_udf(col('month')))

    conditions = [
                (list["price"] < 500, "<500"),
                ((list["price"] >= 500) & (list["price"] <= 1000), "500-1000"),
                ((list["price"] > 1000) & (list["price"] <= 2500), "1000-2500"),
                ((list["price"] > 2500) & (list["price"] <= 5000), "2500-5000"),
                (list["price"] > 5000, ">5000")
                ]

    values = ["<500", "500-1000", "1000-2500", "2500-5000", ">5000"]
    list = list.withColumn("price_range", when(conditions[0][0], values[0])
                                  .when(conditions[1][0], values[1])
                                  .when(conditions[2][0], values[2])
                                  .when(conditions[3][0], values[3])
                                  .when(conditions[4][0], values[4])
                                  .otherwise(None))


    #Export
    joined.write.format('bigquery') \
                .option('table', 'airbnb_bkk_analysis.review_analysis') \
                .save()
    
    cal.write.format('bigquery') \
                .option('table', 'airbnb_bkk_analysis.cal_analysis') \
                .save()
    
    list.write.format('bigquery') \
                .option('table', 'airbnb_bkk_analysis.list_analysis') \
                .save()



if __name__ == "__main__":
    main()
    spark.stop()
