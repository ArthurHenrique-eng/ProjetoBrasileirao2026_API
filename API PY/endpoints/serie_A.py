from flask import Blueprint, jsonify, request, abort
from conectar.funcaoConectar import conectar

serieA_bp = Blueprint("serie_A", __name__, url_prefix="/Serie_A")

#ROTAS PARA A TABELA SERIE A
##ROTA GET
##############################################

@serieA_bp.route("/", methods=["GET"])
def listar_serie_a():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Serie_A")
    dados = [
        {"idSerieA": row[0], "NomeClube": row[1], "PontosClube": row[2], "PosicaoClube": row[3],
         "JogosClube": row[4], "VitoriasClube": row[5], "EmpatesClube": row[6], "DerrotasClube": row[7],
         "GolsProClube": row[8], "GolsContraClube": row[9], "SaldoGolsClube": row[10]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################


@serieA_bp.route("/", methods=["POST"])
def criar_clube_serie_a():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    campos_obrigatorios = {"NomeClube", "PontosClube", "PosicaoClube", "JogosClube",
                           "VitoriasClube", "EmpatesClube", "DerrotasClube",
                           "GolsProClube", "GolsContraClube", "SaldoGolsClube"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Serie_A (NomeClube, PontosClube, PosicaoClube, JogosClube, VitoriasClube, "
        "EmpatesClube, DerrotasClube, GolsProClube, GolsContraClube, SaldoGolsClube) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (dados["NomeClube"], dados["PontosClube"], dados["PosicaoClube"], dados["JogosClube"],
         dados["VitoriasClube"], dados["EmpatesClube"], dados["DerrotasClube"],
         dados["GolsProClube"], dados["GolsContraClube"], dados["SaldoGolsClube"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    resposta = jsonify({"idSerieA": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_A/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################

@serieA_bp.route("/<int:idSerieA>", methods=["PUT", "PATCH"])
def atualizar_clube_serie_a(idSerieA):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    if request.method == "PUT":
        campos_esperados = {"NomeClube", "PontosClube", "PosicaoClube", "JogosClube",
                            "VitoriasClube", "EmpatesClube", "DerrotasClube",
                            "GolsProClube", "GolsContraClube", "SaldoGolsClube"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    campos_validos = {"NomeClube", "PontosClube", "PosicaoClube", "JogosClube",
                      "VitoriasClube", "EmpatesClube", "DerrotasClube",
                      "GolsProClube", "GolsContraClube", "SaldoGolsClube"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerieA)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Serie_A SET {', '.join(set_clauses)} WHERE idSerieA = ?", tuple(valores))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()
    return ("", 204)

##ROTA DELETE
#############################################
from flask import jsonify, abort

@serieA_bp.route("/<int:idSerieA>", methods=["DELETE"])
def deletar_clube_serie_a(idSerieA):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Serie_A WHERE idSerieA = ?", (idSerieA,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()
    return ("", 204)