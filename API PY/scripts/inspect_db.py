import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "BancoDados", "campeonato_brasileiro_2026.db")
print("Usando DB:", db_path)
if not os.path.exists(db_path):
    print("Arquivo de banco não encontrado:", db_path)
    raise SystemExit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name, type, sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name;")
rows = cur.fetchall()
if not rows:
    print("Nenhuma tabela ou view encontrada no banco.")
else:
    for r in rows:
        name = r[0]
        print(f"Tabela: {name}")
        try:
            cur.execute(f"SELECT COUNT(*) FROM {name}")
            cnt = cur.fetchone()[0]
            print(f"  registros: {cnt}")
        except Exception as e:
            print(f"  não foi possível contar registros: {e}")
conn.close()