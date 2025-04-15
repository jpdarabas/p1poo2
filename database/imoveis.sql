CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    endereco TEXT NOT NULL,
    valor_diaria REAL NOT NULL,
    locador_id INTEGER NOT NULL,
    FOREIGN KEY (locador_id) REFERENCES usuarios(id)
);