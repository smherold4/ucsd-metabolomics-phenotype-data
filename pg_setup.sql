-- Database Setup
CREATE ROLE ucsd;
ALTER ROLE ucsd WITH SUPERUSER;
ALTER ROLE ucsd WITH login;
ALTER ROLE ucsd WITH PASSWORD '{password}';
create database metabolomics_phenotype;
grant all privileges on database metabolomics_phenotype to ucsd;
