Create database opendict_iceberg;
USE ROLE ACCOUNTADMIN;
USE ROLE TRAINING_ROLE;

-- Setting up and external volume to azure: https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-external-volume-azure
ALTER DATABASE opendict_iceberg SET CATALOG = 'AZURE_CATALOG';
CREATE or replace EXTERNAL VOLUME AZURESTORAGEVOL
  STORAGE_LOCATIONS =
    (
      (
        NAME = 'polarisstorageacc'
        STORAGE_PROVIDER = 'AZURE'
        STORAGE_BASE_URL = 'azure://polarisstorageacc.blob.core.windows.net/polarisbucket/warehouse'
        AZURE_TENANT_ID = 'bea229b6-7a08-4086-b44c-71f57f716bdb'
      )
    );
DESC EXTERNAL VOLUME AZURESTORAGEVOL;
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('AZURESTORAGEVOL');



-- Setting up a Polaris catalog integration.
CREATE OR REPLACE CATALOG INTEGRATION AZURE_CATALOG
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://opendict.duckdns.org/api/catalog'
    CATALOG_NAME = 'AZURE_CATALOG'

  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = 'https://opendict.duckdns.org/api/catalog/v1/oauth/tokens'
    OAUTH_CLIENT_ID = '42635de75d261729'
    OAUTH_CLIENT_SECRET = '28643c4e26b9e6284fec7b8bda644fc8'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL')
  )
  ENABLED = TRUE;
SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('AZURE_CATALOG');


-- Create taxis iceberg table
CREATE or replace ICEBERG TABLE taxis
  CATALOG = 'AZURE_CATALOG'
  EXTERNAL_VOLUME='AZURESTORAGEVOL'
  CATALOG_NAMESPACE = 'nyc'
  CATALOG_TABLE_NAME = 'taxis'
  AUTO_REFRESH = TRUE;


-- 5. Snowflake DEMO
CREATE OR REPLACE CATALOG INTEGRATION AZURE_CATALOG...;
CREATE or replace EXTERNAL VOLUME AZURESTORAGEVOL...;
CREATE or replace ICEBERG TABLE taxis...;

-- 5.1. Show the synced function
show user functions;

-- 5.2. Examine datalake.
SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('AZURE_CATALOG');
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('AZURE_CATALOG', 'SYSTEM');
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('AZURE_CATALOG', 'nyc');

-- 5.3. Query the taxis table
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    usd_to_dkk(fare_amount)
FROM taxis limit 10;
