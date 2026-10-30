-- Tables for the two synthetic CSVs in data/synthetic/.
-- Run by src/snowflake_load.py, which also uploads the files to the stage.
-- Every statement ends with a semicolon, so keep semicolons out of comments.

CREATE DATABASE IF NOT EXISTS FIRST_CALL;
CREATE SCHEMA IF NOT EXISTS FIRST_CALL.SYNTHETIC;
USE SCHEMA FIRST_CALL.SYNTHETIC;

CREATE FILE FORMAT IF NOT EXISTS CSV_HEADER
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    EMPTY_FIELD_AS_NULL = TRUE
    TIME_FORMAT = 'HH24:MI';

CREATE STAGE IF NOT EXISTS RAW_FILES FILE_FORMAT = CSV_HEADER;

-- One row per facility (82 rows). acpr_code joins to the 11 SA regions (401-411).
CREATE OR REPLACE TABLE FACILITIES (
    facility_id            VARCHAR PRIMARY KEY,
    facility_name          VARCHAR,
    facility_type          VARCHAR,
    services               VARCHAR,
    street_address         VARCHAR,
    suburb                 VARCHAR,
    postcode               NUMBER(4),
    state                  VARCHAR,
    full_address           VARCHAR,
    latitude               FLOAT,
    longitude              FLOAT,
    lga_code               NUMBER,
    lga_name               VARCHAR,
    sa3_code               NUMBER,
    sa3_name               VARCHAR,
    region_group           VARCHAR,
    phn_code               VARCHAR,
    phn_name               VARCHAR,
    acpr_code              NUMBER(3),
    acpr_name              VARCHAR,
    phone                  VARCHAR,
    email                  VARCHAR,
    website                VARCHAR,
    opening_hours          VARCHAR,
    booking_methods        VARCHAR,
    next_available         VARCHAR,
    upcoming_slots         VARCHAR,
    slots_next_14_days     NUMBER,
    wait_days_to_next      NUMBER,
    accepting_new_clients  VARCHAR,
    telehealth             VARCHAR,
    home_visits            VARCHAR,
    wheelchair_accessible  VARCHAR,
    languages              VARCHAR,
    billing_model          VARCHAR,
    price_item             VARCHAR,
    price_aud              NUMBER(8, 2),
    price_unit             VARCHAR,
    medicare_rebate_aud    NUMBER(8, 2),
    out_of_pocket_aud      NUMBER(8, 2),
    concession_price_aud   NUMBER(8, 2),
    price_notes            VARCHAR,
    is_synthetic           BOOLEAN,
    data_as_of             DATE
);

-- One row per open appointment slot (2,915 rows).
CREATE OR REPLACE TABLE APPOINTMENT_SLOTS (
    slot_id            VARCHAR PRIMARY KEY,
    facility_id        VARCHAR REFERENCES FACILITIES (facility_id),
    facility_name      VARCHAR,
    date               DATE,
    weekday            VARCHAR,
    start_time         TIME,
    end_time           TIME,
    duration_min       NUMBER,
    service            VARCHAR,
    practitioner_role  VARCHAR,
    mode               VARCHAR,
    fee_aud            NUMBER(8, 2),
    status             VARCHAR
);

COPY INTO FACILITIES FROM @RAW_FILES/sa_health_facilities_synthetic.csv.gz;
COPY INTO APPOINTMENT_SLOTS FROM @RAW_FILES/sa_appointment_slots_synthetic.csv.gz;

-- Open slots per facility with its region, ready for the app to read.
CREATE OR REPLACE VIEW FACILITY_AVAILABILITY AS
SELECT
    f.acpr_code,
    f.acpr_name,
    f.facility_id,
    f.facility_name,
    f.facility_type,
    f.suburb,
    f.phone,
    f.home_visits,
    f.telehealth,
    f.languages,
    COUNT(s.slot_id) AS open_slots,
    MIN(TIMESTAMP_NTZ_FROM_PARTS(s.date, s.start_time)) AS next_slot
FROM FACILITIES f
LEFT JOIN APPOINTMENT_SLOTS s
    ON s.facility_id = f.facility_id AND s.status = 'Available'
GROUP BY ALL;
