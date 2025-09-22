-- Lista Todos os Veterinários Com CRMV --
CREATE VIEW vwVeterinarios AS
SELECT p.id_pessoa, p.nome, v.CRMV
FROM VETERINARIO v
JOIN PESSOA p ON v.id_pessoa = p.id_pessoa;

-- Lista todos os Compradores e seus dados --- 
CREATE VIEW vwCompradores AS
SELECT p.id_pessoa, p.nome, p.tipo_documento, p.documento, p.contato, c.categoria_cliente
FROM PESSOA p
JOIN COMPRADOR c ON p.id_pessoa = c.id_pessoa;


-- Lista todos os Vendedores e Seus Dados --

CREATE VIEW vwVendedores AS
SELECT p.id_pessoa, p.nome, p.tipo_documento, p.documento, p.contato, vd.inscricao_estadual
FROM PESSOA p
JOIN VENDEDOR vd ON p.id_pessoa = vd.id_pessoa;


---------------------------------------------------------------------------------------------------

-- Lista todos os bois e seu ultimo peso -- 

CREATE VIEW vwBoiPesoAtual AS
SELECT b.brinco, b.raca, b.status, p.peso, p.data
FROM BOI b
LEFT JOIN PESAGEM p ON b.brinco = p.brinco
WHERE p.data = (
    SELECT MAX(data)
    FROM PESAGEM p2
    WHERE p2.brinco = b.brinco
);

-- Lista o acomepanhamento da peso dos bois (Suporta até 3 pesagens, pois SQL não possui view dinâmica) ---- 
CREATE VIEW vwHistoricoPesagem AS
SELECT
    b.brinco,
    cb.peso_compra,
    p1.peso AS peso1,
    p2.peso AS peso2,
    p3.peso AS peso3,
    vb.peso_venda
FROM BOI b
LEFT JOIN COMPRA_BOI cb ON b.brinco = cb.brinco
LEFT JOIN (
    SELECT brinco, peso, ROW_NUMBER() OVER (PARTITION BY brinco ORDER BY data) AS rn
    FROM PESAGEM
) pesagem_ordenada ON pesagem_ordenada.brinco = b.brinco
LEFT JOIN PESAGEM p1 ON p1.brinco = b.brinco AND pesagem_ordenada.rn = 1
LEFT JOIN PESAGEM p2 ON p2.brinco = b.brinco AND pesagem_ordenada.rn = 2
LEFT JOIN PESAGEM p3 ON p3.brinco = b.brinco AND pesagem_ordenada.rn = 3
LEFT JOIN VENDA_BOI vb ON vb.brinco = b.brinco;

-- Lista a localização dos bois no pasto --- 
CREATE VIEW vwBoisNoPasto AS
SELECT 
    b.brinco,
    b.raca,
    b.status,
    p.nome_pasto,
    p.localizacao,
    m.data_entrada,
    m.data_saida
FROM MOVIMENTACAO m
JOIN BOI b ON m.brinco = b.brinco
JOIN PASTO p ON m.id_pasto = p.id_pasto
WHERE m.data_saida IS NULL;

-- Lista a medicação aplicada no boi --
CREATE VIEW vwMedicacoesPorBoi AS
SELECT
    b.brinco,
    b.raca,
    m.id_medicacao,
    md.medicamento,
    m.data,
    dm.nro_dose,
    dm.data_aplicacao,
    dm.observacoes,
    p.nome AS veterinario
FROM MEDICACAO m
JOIN BOI b ON m.brinco = b.brinco
JOIN DOSE_MEDICACAO dm ON dm.id_medicacao = m.id_medicacao
JOIN MEDICAMENTO md ON md.id_medicamento = m.id_medicamento
JOIN VETERINARIO v ON m.id_veterinario = v.id_pessoa
JOIN PESSOA p ON v.id_pessoa = p.id_pessoa;



--- 
