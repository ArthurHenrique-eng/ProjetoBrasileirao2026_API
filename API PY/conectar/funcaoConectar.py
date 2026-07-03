import sqlite3
import os
from pathlib import Path


def conectar():
    base = Path(__file__).resolve().parents[1]
    db_path = base / "BancoDados" / "campeonato_brasileiro_2026.db"
    if not db_path.exists():
        # listar arquivos presentes para ajudar diagnóstico
        files = os.listdir(base / "BancoDados") if (base / "BancoDados").exists() else []
        raise FileNotFoundError(f"Arquivo de banco não encontrado: {db_path}. Arquivos em BancoDados: {files}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn