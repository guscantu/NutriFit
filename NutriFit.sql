

CREATE DATABASE NutriFitBanco;
USE NutriFitBanco;


CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    peso FLOAT NOT NULL,
    altura FLOAT NOT NULL,
    objetivo ENUM('perder peso', 'ganhar massa muscular', 'manter peso') NOT NULL,
    restricoes TEXT
);

CREATE TABLE Dica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objetivo ENUM('perder peso','ganhar massa muscular','manter peso') NOT NULL,
    texto TEXT NOT NULL
);


CREATE TABLE Produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco FLOAT,
    link_compra VARCHAR(255)
);


CREATE TABLE Progresso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    dataprogresso DATE NOT NULL,
    peso FLOAT NOT NULL, -- peso registrado no dia
    imc FLOAT,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

CREATE TABLE RestricaoAlimentar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Usuario_Restricao (
    usuario_id INT NOT NULL,
    restricao_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (restricao_id) REFERENCES RestricaoAlimentar(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, restricao_id)
);

CREATE TABLE FaixaPeso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faixa_min FLOAT NOT NULL,
    faixa_max FLOAT NOT NULL
);

CREATE TABLE FaixaAltura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faixa_min FLOAT NOT NULL,
    faixa_max FLOAT NOT NULL
);

CREATE TABLE FaixaIdade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faixa_min INT NOT NULL,
    faixa_max INT NOT NULL
);

CREATE TABLE DietaPersonalizada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faixa_peso_id INT NOT NULL,
    faixa_altura_id INT NOT NULL,
    faixa_idade_id INT NOT NULL,
    objetivo ENUM('perder peso', 'ganhar massa muscular', 'manter peso') NOT NULL,
    restricao TEXT, -- opcional
    descricao TEXT NOT NULL,
    FOREIGN KEY (faixa_peso_id) REFERENCES FaixaPeso(id) ON DELETE CASCADE,
    FOREIGN KEY (faixa_altura_id) REFERENCES FaixaAltura(id) ON DELETE CASCADE,
    FOREIGN KEY (faixa_idade_id) REFERENCES FaixaIdade(id) ON DELETE CASCADE
);

CREATE TABLE RefeicaoPersonalizada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dieta_personalizada_id INT NOT NULL,
    tipo ENUM('café da manhã', 'almoço', 'lanche', 'jantar') NOT NULL,
    alimentos TEXT NOT NULL,
    FOREIGN KEY (dieta_personalizada_id) REFERENCES DietaPersonalizada(id) ON DELETE CASCADE
);

CREATE TABLE SubstituicaoAlimento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restricao_id INT NOT NULL,
    alimento_original VARCHAR(100) NOT NULL,
    alimento_substituto VARCHAR(100) NOT NULL,
    FOREIGN KEY (restricao_id) REFERENCES RestricaoAlimentar(id) ON DELETE CASCADE
);
