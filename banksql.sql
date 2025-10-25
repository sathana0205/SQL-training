create database bank_db;
use bank_db;
create table if not exists account(
id INT AUTO_INCREMENT PRIMARY KEY,
account_holder VARCHAR(100) NOT NULL ,
pin CHAR(4) NOT NULL,
balance DECIMAL(15,2)NOT NULL DEFAULT 0.00,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into account (account_holder,pin,balance)values('kani',7181,5000),
('prithi',8191,9087),
('mani',2002,8000),
('kani',2005,78900)
;

