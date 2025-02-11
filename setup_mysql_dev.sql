-- Create database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create user and grant privileges
CREATE USER IF NOT EXISTS hbnb_dev@localhost IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO hbnb_dev@localhost;
GRANT SELECT ON performance_schema.* TO hbnb_dev@localhost;
