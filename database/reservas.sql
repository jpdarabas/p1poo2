CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    valor_total REAL NOT NULL,
    imovel_id INTEGER NOT NULL,
    locatario_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'confirmada')),
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id),
    FOREIGN KEY (locatario_id) REFERENCES usuarios(id)
);