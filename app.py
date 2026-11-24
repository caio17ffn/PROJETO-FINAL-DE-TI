from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, abort
from datetime import date
import os
import banco, logica

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR, static_folder=None)
banco.criar_banco()          # cria o banco ao iniciar (funciona no Render tb)

# ---------------- ARQUIVOS ESTÁTICOS (só o CSS) ----------------

ARQUIVOS_PUBLICOS = {"style.css"}


# endpoint="static" mantém funcionando url_for('static', filename='style.css')
@app.route("/static/<path:filename>", endpoint="static")
def arquivo_estatico(filename):
    if filename not in ARQUIVOS_PUBLICOS:
        abort(404)
    return send_from_directory(BASE_DIR, filename)


# caso o HTML chame direto href="style.css" ou href="/style.css"
@app.route("/style.css")
def css():
    return send_from_directory(BASE_DIR, "style.css")


# ---------------- PÁGINAS ----------------

@app.route("/")
def home():
    return render_template(
        "home.html",
        consultas=banco.listar_consultas()[:5],
        total=len(banco.listar_pacientes()),
        total_consultas=len(banco.listar_consultas()),
        total_medicamentos=len(banco.listar_medicamentos()),
    )


@app.route("/pacientes")
def pagina_pacientes():
    ordem = request.args.get("ordem", "nome")
    lista = banco.listar_pacientes()                     # já vem do SQL
    pacientes = logica.bubble_sort_pacientes(lista, ordem)  # algoritmo UC30
    return render_template("pacientes.html", pacientes=pacientes, ordem=ordem)


@app.route("/consultas")
def pagina_consultas():
    filtro = request.args.get("data")
    if filtro:
        # busca binária em cima da lista ordenada (UC30)
        todas = sorted(banco.listar_consultas(), key=lambda c: c["data"])
        achada = logica.busca_binaria_por_data(todas, filtro)
        consultas = [achada] if achada else []
    else:
        consultas = banco.listar_consultas()
    return render_template("consultas.html",
                           consultas=consultas,
                           pacientes=banco.listar_pacientes(),
                           filtro=filtro)


@app.route("/medicamentos")
def pagina_medicamentos():
    return render_template("medicamentos.html",
                           medicamentos=banco.listar_medicamentos(),
                           hoje=str(date.today()))


# ---------------- CRUD PACIENTES ----------------

@app.route("/pacientes/novo", methods=["POST"])
def novo_paciente():
    banco.inserir_paciente(request.form["nome"],
                           request.form.get("telefone"),
                           request.form.get("nascimento"))
    return redirect(url_for("pagina_pacientes"))


@app.route("/pacientes/<int:pid>/editar", methods=["POST"])
def editar_paciente(pid):
    banco.atualizar_paciente(pid, request.form["nome"],
                             request.form.get("telefone"),
                             request.form.get("nascimento"))
    return redirect(url_for("pagina_pacientes"))


@app.route("/pacientes/<int:pid>/excluir")
def apagar_paciente(pid):
    banco.excluir_paciente(pid)
    return redirect(url_for("pagina_pacientes"))


# ---------------- CRUD CONSULTAS ----------------

@app.route("/consultas/nova", methods=["POST"])
def nova_consulta():
    banco.inserir_consulta(request.form["paciente_id"],
                           request.form["data"],
                           request.form.get("horario"),
                           request.form.get("observacao"))
    return redirect(url_for("pagina_consultas"))


@app.route("/consultas/<int:cid>/excluir")
def apagar_consulta(cid):
    banco.excluir_consulta(cid)
    return redirect(url_for("pagina_consultas"))


# ---------------- CRUD MEDICAMENTOS ----------------

@app.route("/medicamentos/novo", methods=["POST"])
def novo_medicamento():
    banco.inserir_medicamento(request.form["nome"],
                              request.form.get("quantidade"),
                              request.form.get("validade"))
    return redirect(url_for("pagina_medicamentos"))


@app.route("/medicamentos/<int:mid>/excluir")
def apagar_medicamento(mid):
    banco.excluir_medicamento(mid)
    return redirect(url_for("pagina_medicamentos"))


# ---------------- API JSON (UC33) ----------------

@app.route("/api/pacientes")
def api_pacientes():
    return jsonify([dict(p) for p in banco.listar_pacientes()])


@app.route("/api/consultas")
def api_consultas():
    return jsonify([dict(c) for c in banco.listar_consultas()])


@app.route("/api/medicamentos")
def api_medicamentos():
    return jsonify([dict(m) for m in banco.listar_medicamentos()])


if __name__ == "__main__":
    app.run(debug=True)
