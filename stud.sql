show databases;
create database janani;
use janani;
 show databases;
 
create table if not exists stud(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100)NOT NULL,
age INT 
);

insert into stud values(1,'mani',20),
(2,'kani',21),
(3,'prithi',18),
(4,'sahana',19)
;
