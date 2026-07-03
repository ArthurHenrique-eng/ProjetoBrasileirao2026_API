from flask import Blueprint, jsonify, request, abort
from conectar.funcaoConectar import conectar

serieD_bp = Blueprint("serie_D", __name__, url_prefix="/Serie_D")

#ROTAS PARA A TABELA SERIE D
##ROTA GET
##############################################

@serieD_bp.route("/", methods=["GET"])
def listar_serie_d():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Serie_D")
    dados = [
        {"idSerieD": row[0], "NomeClube": row[1], "PontosClube": row[2], "PosicaoClube": row[3],
         "JogosClube": row[4], "VitoriasClube": row[5], "EmpatesClube": row[6], "DerrotasClube": row[7],
         "GolsProClube": row[8], "GolsContraClube": row[9], "SaldoGolsClube": row[10]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

from flask import request, jsonify, abort
@serieD_bp.route("/", methods=["POST"])
def criar_clube_serie_d():
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
        "INSERT INTO Serie_D (NomeClube, PontosClube, PosicaoClube, JogosClube, VitoriasClube, "
        "EmpatesClube, DerrotasClube, GolsProClube, GolsContraClube, SaldoGolsClube) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (dados["NomeClube"], dados["PontosClube"], dados["PosicaoClube"], dados["JogosClube"],
         dados["VitoriasClube"], dados["EmpatesClube"], dados["DerrotasClube"],
         dados["GolsProClube"], dados["GolsContraClube"], dados["SaldoGolsClube"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    resposta = jsonify({"idSerieD": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_D/{novo_id}"
    return resposta


##ROTA UPDATE
#############################################

@serieD_bp.route("/<int:idSerieD>", methods=["PUT", "PATCH"])
def atualizar_clube_serie_d(idSerieD):
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

    valores.append(idSerieD)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Serie_D SET {', '.join(set_clauses)} WHERE idSerieD = ?", tuple(valores))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()
    return ("", 204)

##ROTA DELETE
#############################################
from flask import jsonify, abort

@serieD_bp.route("/<int:idSerieD>", methods=["DELETE"])
def deletar_clube_serie_d(idSerieD):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Serie_D WHERE idSerieD = ?", (idSerieD,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()
    return ("", 204)