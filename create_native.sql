CREATE OR REPLACE TABLE `datacafeplayground.airbnb_bkk_warehouse.native_listing_cluster` 
CLUSTER BY host_id AS (
  SELECT * FROM `datacafeplayground.airbnb_bkk_warehouse.external_listing`
);



CREATE OR REPLACE TABLE `datacafeplayground.airbnb_bkk_warehouse.native_calendar`
PARTITION BY DATE_TRUNC(date, MONTH)
CLUSTER BY listing_id AS (
  SELECT listing_id,date,available FROM `datacafeplayground.airbnb_bkk_warehouse.external_calendar`
);


CREATE OR REPLACE TABLE `datacafeplayground.airbnb_bkk_warehouse.native_review`
PARTITION BY DATE_TRUNC(date, MONTH)
CLUSTER BY listing_id AS (
  SELECT * FROM `datacafeplayground.airbnb_bkk_warehouse.external_review`
);