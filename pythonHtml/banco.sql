CREATE DATABASE escolas;

USE DATABASE escolas;

CREATE TABLE alunos(
    ID_aluno INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    idade int,
    CPF VARCHAR(11),
    telefone VARCHAR(11)
);