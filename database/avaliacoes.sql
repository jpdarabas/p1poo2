CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
    comentario TEXT,
    reserva_id INTEGER NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id)
);