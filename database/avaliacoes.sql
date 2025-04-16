CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
    comentario TEXT,
    imovel_id INTEGER NOT NULL,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id)
);