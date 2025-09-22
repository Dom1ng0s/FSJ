-- Tabela PESSOA
CREATE TABLE PESSOA (
    id_pessoa INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(20) NOT NULL,
    documento VARCHAR(30) NOT NULL UNIQUE,
    contato VARCHAR(50)
);

-- Tabela VETERINARIO
CREATE TABLE VETERINARIO (
    id_pessoa INT PRIMARY KEY,
    CRMV INT NOT NULL,
    CONSTRAINT fk_veterinario_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa)
);

-- Tabela VENDEDOR
CREATE TABLE VENDEDOR (
    id_pessoa INT PRIMARY KEY,
    inscricao_estadual VARCHAR(30),
    CONSTRAINT fk_vendedor_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa)
);

-- Tabela COMPRADOR
CREATE TABLE COMPRADOR (
    id_pessoa INT PRIMARY KEY,
    categoria_cliente VARCHAR(50),
    CONSTRAINT fk_comprador_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa)
);

-- Tabela BOI
CREATE TABLE BOI (
    brinco INT PRIMARY KEY,
    raca VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    brinco_pai INT,
    brinco_mae INT,
    CONSTRAINT fk_boi_pai FOREIGN KEY (brinco_pai) REFERENCES BOI(brinco),
    CONSTRAINT fk_boi_mae FOREIGN KEY (brinco_mae) REFERENCES BOI(brinco)
);

-- Tabela COMPRA
CREATE TABLE COMPRA (
    id_compra INT PRIMARY KEY,
    data_compra DATE NOT NULL,
    id_vendedor INT,
    CONSTRAINT fk_compra_vendedor FOREIGN KEY (id_vendedor) REFERENCES VENDEDOR(id_pessoa)
);

-- Tabela VENDA
CREATE TABLE VENDA (
    id_venda INT PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_comprador INT,
    CONSTRAINT fk_venda_comprador FOREIGN KEY (id_comprador) REFERENCES COMPRADOR(id_pessoa)
);

-- Tabela COMPRA_BOI
CREATE TABLE COMPRA_BOI (
    id_compra INT,
    brinco INT,
    peso_compra DECIMAL(7,2),
    preco_compra DECIMAL(10,2),
    PRIMARY KEY (id_compra, brinco),
    CONSTRAINT fk_compra_boi_compra FOREIGN KEY (id_compra) REFERENCES COMPRA(id_compra),
    CONSTRAINT fk_compra_boi_boi FOREIGN KEY (brinco) REFERENCES BOI(brinco)
);

-- Tabela VENDA_BOI
CREATE TABLE VENDA_BOI (
    id_venda INT,
    brinco INT,
    peso_venda DECIMAL(7,2),
    preco_venda DECIMAL(10,2),
    PRIMARY KEY (id_venda, brinco),
    CONSTRAINT fk_venda_boi_venda FOREIGN KEY (id_venda) REFERENCES VENDA(id_venda),
    CONSTRAINT fk_venda_boi_boi FOREIGN KEY (brinco) REFERENCES BOI(brinco)
);

-- Tabela MEDICAMENTO
CREATE TABLE MEDICAMENTO (
    id_medicamento INT PRIMARY KEY,
    medicamento VARCHAR(100) NOT NULL
);

-- Tabela MEDICACAO
CREATE TABLE MEDICACAO (
    id_medicacao INT PRIMARY KEY,
    data DATE NOT NULL,
    dose VARCHAR(50),
    id_veterinario INT,
    id_medicamento INT,
    CONSTRAINT fk_medicacao_veterinario FOREIGN KEY (id_veterinario) REFERENCES VETERINARIO(id_pessoa),
    CONSTRAINT fk_medicacao_medicamento FOREIGN KEY (id_medicamento) REFERENCES MEDICAMENTO(id_medicamento)
);

-- Tabela DOSE_MEDICACAO
CREATE TABLE DOSE_MEDICACAO (
    id_medicacao INT,
    nro_dose INT,
    data_aplicacao DATE,
    observacoes VARCHAR(255),
    PRIMARY KEY (id_medicacao, nro_dose),
    CONSTRAINT fk_dose_medicacao FOREIGN KEY (id_medicacao) REFERENCES MEDICACAO(id_medicacao)
);

-- Tabela PASTO
CREATE TABLE PASTO (
    id_pasto INT PRIMARY KEY,
    nome_pasto VARCHAR(100) NOT NULL,
    localizacao VARCHAR(150)
);

-- Tabela MOVIMENTACAO
CREATE TABLE MOVIMENTACAO (
    id_estadia INT PRIMARY KEY,
    data_entrada DATE NOT NULL,
    data_saida DATE,
    brinco INT,
    id_pasto INT,
    CONSTRAINT fk_movimentacao_boi FOREIGN KEY (brinco) REFERENCES BOI(brinco),
    CONSTRAINT fk_movimentacao_pasto FOREIGN KEY (id_pasto) REFERENCES PASTO(id_pasto)
);

-- Tabela PESAGEM
CREATE TABLE PESAGEM (
    id_pesagem INT PRIMARY KEY,
    data DATE NOT NULL,
    peso DECIMAL(7,2) NOT NULL,
    brinco INT,
    CONSTRAINT fk_pesagem_boi FOREIGN KEY (brinco) REFERENCES BOI(brinco)
);

-- Tabela PARTO
CREATE TABLE PARTO (
    id_parto INT PRIMARY KEY,
    id_pai INT,
    id_mae INT,
    id_veterinario INT,
    id_nascido INT,
    data_parto DATE NOT NULL,
    CONSTRAINT fk_parto_pai FOREIGN KEY (id_pai) REFERENCES BOI(brinco),
    CONSTRAINT fk_parto_mae FOREIGN KEY (id_mae) REFERENCES BOI(brinco),
    CONSTRAINT fk_parto_veterinario FOREIGN KEY (id_veterinario) REFERENCES VETERINARIO(id_pessoa),
    CONSTRAINT fk_parto_nascido FOREIGN KEY (id_nascido) REFERENCES BOI(brinco)
);
