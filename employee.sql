show databases;
use sathana;
create table employees(
emp_id INT PRIMARY KEY,
emp_name VARCHAR(255),
emp_age INT,
emp_dept VARCHAR(255)
);
create table Emp_salar(
emp_sal_id INT,
emp_id INT PRIMARY KEY,
emp_salary VARCHAR(255),
FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
select
e.emp_id,
e.emp_name,
e.emp_age,
e.emp_dept,
(select s.emp_salary from Emp_salar s where s.emp_id = e.emp_id) emp_salary from employees e;





