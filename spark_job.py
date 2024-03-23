from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.functions import col, udf,month
from pyspark.sql.types import BooleanType,StringType

def get_season(month):
    if month in range(3, 7):  # March to June: Summer
        return 'Summer'
    elif month in range(7, 11):  # July to October: Monsoon
        return 'Monsoon'
    else:  # November to February: Winter
        return 'Winter'


def main():
    bucket = "dataproc-staging-asiasoutheast1-626484338807-1lyhkan9"
    spark.conf.set('temporaryGcsBucket', bucket)
    spark = SparkSession \
            .builder \
            .appName('spark-bigquery') \
            .getOrCreate()
    #Get Data
    cal = spark.read.format('bigquery') \
            .option('table', 'airbnb_bkk_warehouse.native_cal') \
            .load()
    review = spark.read.format('bigquery') \
            .option('table', 'airbnb_bkk_warehouse.native_review') \
            .load()
    neighbour = spark.read.csv("neighbour_data.csv", header=True)

    #Transform
    review = review.drop('__index_level_0__')
    joined= review.join(neighbour, 'listing_id', how='left')


    get_season_udf = udf(get_season, StringType())
    cal = cal.withColumn('month', month('date'))
    cal = cal.withColumn('season', get_season_udf(col('month')))

    #Export
    joined.write.format('bigquery') \
                .option('table', 'airbnb_bkk_analysis.review_analysis') \
                .save()
    
    cal.write.format('bigquery') \
                .option('table', 'airbnb_bkk_analysis.cal_analysis') \
                .save()



if __name__ == "__main__":
    main()