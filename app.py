from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import db
import io
from datetime import datetime
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    # para pedir /api/creditos y stats
    return render_template("index.html")


#------ Rutas CRUD -----

#---- REGISTRAR NUEVO ------
@app.route("/api/creditos", methods=["POST"])
def api_crear():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON requerido"}), 400
    
    cliente = data.get("cliente", "").strip()
    try:
        monto = float(data.get("monto"))
        tasa_interes = float(data.get("tasa_interes"))
        plazo = int(data.get("plazo"))
    except (TypeError, ValueError):
        return jsonify({"error": "Valores numericos inválidos" }), 400
    
    fecha = data.get("fecha_otorgamiento", "").strip()
    if not (cliente and fecha):
        return jsonify({"error": "Datos obligatorios"}), 400
    
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error":"Fecha inválida (YYYY-MM-DD)"}), 400
    
    nuevo_id = db.create_credito(cliente, monto, tasa_interes, plazo, fecha)
    return jsonify({"mensaje": "Creado con exito", "id": nuevo_id}), 201
    
    #-------- EDITAR ------

@app.route("/api/creditos/<int:credito_id>", methods=["PUT"])
def api_editar(credito_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON requerido"}), 400
        
    cliente = data.get("cliente", "").strip()
    try:
        monto = float(data.get("monto"))
        tasa_interes = float(data.get("tasa_interes"))
        plazo = int(data.get("plazo"))
    except(TypeError, ValueError):
        return jsonify({"error": "Valores numericos inválidos"}), 400
        
    fecha = data.get("fecha_otorgamiento", "").strip()
    if not (cliente and fecha):
        return jsonify({"error": "Datos obligatorios"}), 400
        
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Fecha inválida (YYYY-MM-DD)"}), 400
        
    rows = db.update_credito(credito_id, cliente, monto, tasa_interes, plazo, fecha)
    if rows == 0:
        return jsonify({"error": "Datos no encontrados"}), 404
    return jsonify({"mensaje":"Actualizados"})
    
    #--------- ELIMINAR -----------

@app.route("/api/creditos/<int:credito_id>", methods=["DELETE"])
def api_eliminar(credito_id):
    rows = db.delete_credito(credito_id)
    if rows == 0:
        return jsonify({"error": "Datos no encontrados"}), 404
    return jsonify({"mensaje":"Eliminado con exito"})
    
    #--------- LISTAR CREDITOS--------------
@app.route("/api/creditos", methods=["GET"])
def api_listar_creditos():
    return jsonify(db.get_all_creditos())
    
    #--------- Rutas para graficas ---------

@app.route("/api/stats/month", methods=["GET"])
def api_month():
    data = db.get_total_month()
    labels = [d["mes"] for d in data]
    totals = [d["total"] for d in data]
    return jsonify({"labels": labels, "totals": totals})
    
@app.route("/api/stats/cliente", methods=["GET"])
def api_cliente():
    data = db.get_total_cliente()
    labels = [d["cliente"] for d in data]
    totals = [d["total"] for d in data]
    return jsonify({"labels": labels, "totals": totals})
    
@app.route("/api/stats/distribucion", methods=["GET"])
def api_distribucion():

    # Definicion de rangos

    ranges = [(0,10000), (10001,50000),(50001,100000), (100001, None)]
    buckets = db.get_distribucion_ranges(ranges)
    labels = [b["label"] for b in buckets]
    totals = [b["total"] for b in buckets]
    return jsonify({"labels": labels, "totals": totals})

#---------- Grafica (PNG) ----------

@app.route("/chart.png")
def chart_png():
    data = db.get_total_month()
    labels = [d["mes"] for d in data]
    totals = [d["total"] for d in data]
    if not labels:
        labels = ["sin_datos"]
        totals = [0]

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(labels, totals)
    ax.set_title("Total de creditos otorgados por mes")
    ax.set_ylabel("Monto")
    ax.set_xlabel("Mes (YYYY-MM)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    db.ini_db() #inicializa la Base de Datos 
    app.run(debug=True)
#  app.run(host="127.0.0.1", port=5000, debug=True)
