-- ============================================================
-- SISTEMA DE ENCOMENDAS - Script SQL Completo
-- Banco de Dados: PostgreSQL 15+
-- Gerado em: 2026-06-12
-- ============================================================

-- Remove tabelas existentes (ordem inversa por dependência)
DROP TABLE IF EXISTS encomendas CASCADE;
DROP TABLE IF EXISTS funcionarios CASCADE;
DROP TABLE IF EXISTS transportadoras CASCADE;
DROP TABLE IF EXISTS marketplaces CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- ============================================================
-- TABELA: usuarios
-- Descrição: Armazena os usuários do sistema com controle de
--            perfil (administrador ou usuario)
-- ============================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    login VARCHAR(80) NOT NULL UNIQUE,
    senha_hash VARCHAR(256) NOT NULL,
    perfil VARCHAR(20) NOT NULL DEFAULT 'usuario'
        CHECK (perfil IN ('administrador', 'usuario')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE usuarios IS 'Usuários do sistema com controle de acesso';
COMMENT ON COLUMN usuarios.perfil IS 'Perfil de acesso: administrador ou usuario';
COMMENT ON COLUMN usuarios.senha_hash IS 'Senha criptografada com pbkdf2_sha256';

-- ============================================================
-- TABELA: marketplaces
-- Descrição: Cadastro de marketplaces (ex: Mercado Livre, 
--            Amazon, Shopee)
-- ============================================================
CREATE TABLE marketplaces (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    nome_conta VARCHAR(100),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE marketplaces IS 'Cadastro de marketplaces de e-commerce';
COMMENT ON COLUMN marketplaces.nome_conta IS 'Identificador ou nome da conta no marketplace';

-- ============================================================
-- TABELA: transportadoras
-- Descrição: Cadastro de transportadoras com valor padrão 
--            de frete
-- ============================================================
CREATE TABLE transportadoras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    valor_padrao DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE transportadoras IS 'Cadastro de transportadoras e seus valores de frete';
COMMENT ON COLUMN transportadoras.valor_padrao IS 'Valor padrão de frete em R$';

-- ============================================================
-- TABELA: funcionarios
-- Descrição: Cadastro de funcionários responsáveis pelas 
--            encomendas
-- ============================================================
CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE funcionarios IS 'Cadastro de funcionários da operação';

-- ============================================================
-- TABELA: encomendas
-- Descrição: Registro de movimentações de encomendas (envios 
--            e devoluções) com rastreamento de quem registrou
-- ============================================================
CREATE TABLE encomendas (
    id SERIAL PRIMARY KEY,
    tipo_movimento VARCHAR(20) NOT NULL
        CHECK (tipo_movimento IN ('Envio', 'Devolução')),
    marketplace_id INTEGER NOT NULL,
    transportadora_id INTEGER NOT NULL,
    funcionario_id INTEGER NOT NULL,
    quantidade_caixas INTEGER NOT NULL CHECK (quantidade_caixas > 0),
    data_envio DATE NOT NULL,
    observacoes TEXT,
    usuario_id INTEGER NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Chaves estrangeiras
    CONSTRAINT fk_encomenda_marketplace
        FOREIGN KEY (marketplace_id)
        REFERENCES marketplaces (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_encomenda_transportadora
        FOREIGN KEY (transportadora_id)
        REFERENCES transportadoras (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_encomenda_funcionario
        FOREIGN KEY (funcionario_id)
        REFERENCES funcionarios (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_encomenda_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

COMMENT ON TABLE encomendas IS 'Registro de movimentações de encomendas';
COMMENT ON COLUMN encomendas.tipo_movimento IS 'Tipo: Envio ou Devolução';
COMMENT ON COLUMN encomendas.usuario_id IS 'Usuário que registrou a movimentação';
COMMENT ON COLUMN encomendas.quantidade_caixas IS 'Quantidade de caixas (mínimo 1)';

-- ============================================================
-- ÍNDICES
-- ============================================================

-- Índices para consultas e filtros de encomendas
CREATE INDEX idx_encomendas_data_envio ON encomendas (data_envio);
CREATE INDEX idx_encomendas_tipo_movimento ON encomendas (tipo_movimento);
CREATE INDEX idx_encomendas_marketplace_id ON encomendas (marketplace_id);
CREATE INDEX idx_encomendas_transportadora_id ON encomendas (transportadora_id);
CREATE INDEX idx_encomendas_funcionario_id ON encomendas (funcionario_id);
CREATE INDEX idx_encomendas_usuario_id ON encomendas (usuario_id);

-- Índice composto para consultas por período + tipo
CREATE INDEX idx_encomendas_periodo_tipo ON encomendas (data_envio, tipo_movimento);

-- ============================================================
-- DADOS INICIAIS (SEED)
-- ============================================================

-- Usuário administrador padrão
-- Senha: admin123 (hash gerado pelo Werkzeug pbkdf2_sha256)
-- NOTA: O hash real será gerado pelo script seed.py em Python.
-- Este INSERT é apenas referência SQL.
INSERT INTO usuarios (nome, login, senha_hash, perfil, ativo)
VALUES (
    'Administrador',
    'admin',
    'pbkdf2:sha256:600000$placeholder$placeholder',
    'administrador',
    TRUE
);
