import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "clinica.db")

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row      # permite acessar coluna pelo nome
    return conn


def criar_banco():
    conn = conectar()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            data_nascimento TEXT
        );

        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT,
            observacao TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        );

        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER DEFAULT 0,
            validade TEXT
        );
    """)
    conn.commit()
    conn.close()


# ---------------- PACIENTES ----------------

def listar_pacientes():
    conn = conectar()
    dados = conn.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
    conn.close()
    return dados


def inserir_paciente(nome, telefone, nascimento):
    conn = conectar()
    conn.execute("INSERT INTO pacientes (nome, telefone, data_nascimento) VALUES (?,?,?)",
                 (nome, telefone, nascimento))
    conn.commit(); conn.close()


def atualizar_paciente(pid, nome, telefone, nascimento):
    conn = conectar()
    conn.execute("UPDATE pacientes SET nome=?, telefone=?, data_nascimento=? WHERE id=?",
                 (nome, telefone, nascimento, pid))
    conn.commit(); conn.close()


def excluir_paciente(pid):
    conn = conectar()
    conn.execute("DELETE FROM consultas WHERE paciente_id=?", (pid,))
    conn.execute("DELETE FROM pacientes WHERE id=?", (pid,))
    conn.commit(); conn.close()


# ---------------- CONSULTAS (JOIN + WHERE + ORDER BY) ----------------

def listar_consultas():
    conn = conectar()
    dados = conn.execute("""
        SELECT c.id, p.nome AS paciente, c.data, c.horario, c.observacao
        FROM consultas c
        JOIN pacientes p ON p.id = c.paciente_id
        ORDER BY c.data, c.horario
    """).fetchall()
    conn.close()
    return dados


def inserir_consulta(paciente_id, data, horario, obs):
    conn = conectar()
    conn.execute("""INSERT INTO consultas (paciente_id, data, horario, observacao)
                    VALUES (?,?,?,?)""", (paciente_id, data, horario, obs))
    conn.commit(); conn.close()


def excluir_consulta(cid):
    conn = conectar()
    conn.execute("DELETE FROM consultas WHERE id=?", (cid,))
    conn.commit(); conn.close()


# ---------------- MEDICAMENTOS ----------------

def listar_medicamentos():
    conn = conectar()
    dados = conn.execute("SELECT * FROM medicamentos ORDER BY nome").fetchall()
    conn.close()
    return dados


def inserir_medicamento(nome, quantidade, validade):
    conn = conectar()
    conn.execute("INSERT INTO medicamentos (nome, quantidade, validade) VALUES (?,?,?)",
                 (nome, quantidade, validade))
    conn.commit(); conn.close()


def excluir_medicamento(mid):
    conn = conectar()
    conn.execute("DELETE FROM medicamentos WHERE id=?", (mid,))
    conn.commit(); conn.close()
