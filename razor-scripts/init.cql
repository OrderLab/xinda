-- Drop if the keyspace/table exists
DROP TABLE IF EXISTS ycsb.usertable;
DROP KEYSPACE IF EXISTS ycsb;

-- Create keyspace/table
CREATE KEYSPACE ycsb WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};
USE ycsb ;
CREATE TABLE usertable (y_id VARCHAR PRIMARY KEY, field0 VARCHAR, field1 VARCHAR, field2 VARCHAR, field3 VARCHAR, field4 VARCHAR, field5 VARCHAR, field6 VARCHAR, field7 VARCHAR, field8 VARCHAR, field9 VARCHAR);
