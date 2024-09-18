
create database if not exists `db_banco`;
use `db_banco`;

create table usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)

