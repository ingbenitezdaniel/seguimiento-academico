CREATE DATABASE academic_tracking_test;

\connect academic_tracking_test

\i /docker-entrypoint-initdb.d/schema.sql