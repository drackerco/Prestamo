from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "97"

dispositivos = [
    {"id": 1, "nombre": "Laptop Dell Latitude 5420", "serie": "LN-2024-001", "tipo": "Computador", "disponible": 2},
    {"id": 2, "nombre": "Tablet Samsung Galaxy Tab A8", "serie": "TAB-2024-002", "tipo": "Tableta", "disponible": 1},
    {"id": 3, "nombre": "Proyector Epson X39", "serie": "PRO-2024-003", "tipo": "Proyector", "disponible": 1}
]

solicitudes = [
    {"id": 1, "nombre": "María González", "universidad": "Universidad Nacional", "dispositivo": "Laptop Dell Latitude 5420", "motivo": "Proyecto de investigación IA", "estado": "Pendiente"},
    {"id": 2, "nombre": "Carlos Mendoza", "universidad": "Universidad Tecnológica", "dispositivo": "Tablet Samsung Galaxy Tab A8", "motivo": "Clases virtuales de diseño", "estado": "Pendiente"},
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        rol = request.form["rol"]
        if rol == "Administrador" and request.form.get("password") != "7755":
            return "<script>alert('Clave incorrecta');history.back()</script>"
        session["correo"] = correo
        session["rol"] = rol
        return redirect("/panel")
    return render_template("login.html")

@app.route("/panel")
def panel():
    if "correo" not in session: return redirect("/")
    if session["rol"] == "Administrador":
        return render_template("admin.html", dispositivos=dispositivos, solicitudes=solicitudes, correo=session["correo"])
    else:
        return render_template("estudiante.html", dispositivos=dispositivos, solicitudes=solicitudes, correo=session["correo"])

@app.route("/aprobar/<int:id>")
def aprobar(id):
    if session.get("rol") != "Administrador": return redirect("/panel")
    for s in solicitudes:
        if s["id"] == id: s["estado"] = "Aprobado"
    return redirect("/panel")

@app.route("/rechazar/<int:id>")
def rechazar(id):
    if session.get("rol") != "Administrador": return redirect("/panel")
    for s in solicitudes:
        if s["id"] == id: s["estado"] = "Rechazado"
    return redirect("/panel")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    if session.get("rol") != "Administrador": return redirect("/panel")
    global dispositivos
    dispositivos = [d for d in dispositivos if d["id"] != id]
    return redirect("/panel")

@app.route("/solicitar", methods=["POST"])
def solicitar():
    solicitudes.append({
        "id": len(solicitudes)+1,
        "nombre": request.form["nombre"],
        "universidad": request.form["universidad"],
        "dispositivo": request.form["dispositivo"],
        "motivo": request.form["motivo"],
        "estado": "Pendiente"
    })
    return redirect("/panel")

@app.route("/agregar", methods=["POST"])
def agregar():
    if session.get("rol") != "Administrador": return redirect("/panel")
    dispositivos.append({"id": len(dispositivos)+1, "nombre": request.form["nombre"], "serie": request.form["serie"], "tipo": request.form["tipo"], "disponible": 0})
    return redirect("/panel")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5001)