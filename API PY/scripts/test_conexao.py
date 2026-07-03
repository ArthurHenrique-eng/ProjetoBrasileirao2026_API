from conectar.funcaoConectar import conectar

conn = conectar()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM Serie_A")
print('Serie_A count:', cur.fetchone()[0])
conn.close()