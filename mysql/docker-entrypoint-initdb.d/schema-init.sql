# Initialize a database on container build

CREATE SCHEMA IF NOT EXISTS `rdt`;

GRANT ALL PRIVILEGES ON *.* TO `root`@`%`;
GRANT ALL PRIVILEGES ON *.* TO `dbuser`@`%`;

FLUSH PRIVILEGES;

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
ALTER USER 'dbuser'@'%' IDENTIFIED WITH mysql_native_password BY 'dbuser';

SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''));