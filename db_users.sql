create database users;
use users;
create table Users
(
	id int primary key not null,
	name varchar(200) not null,
    email varchar(120) not null,
    data_added datetime not null
);