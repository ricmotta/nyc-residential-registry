#!/bin/sh
# Runs once, on the first start of an empty data volume.
# Creates the project database (with PostGIS) and a separate database for Airflow's metadata.
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<SQL
CREATE ROLE ${REGISTRY_DB_USER} LOGIN PASSWORD '${REGISTRY_DB_PASSWORD}';
CREATE DATABASE ${REGISTRY_DB_NAME} OWNER ${REGISTRY_DB_USER};
CREATE ROLE ${AIRFLOW_DB_USER} LOGIN PASSWORD '${AIRFLOW_DB_PASSWORD}';
CREATE DATABASE ${AIRFLOW_DB_NAME} OWNER ${AIRFLOW_DB_USER};
SQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$REGISTRY_DB_NAME" <<SQL
CREATE EXTENSION IF NOT EXISTS postgis;
SQL
