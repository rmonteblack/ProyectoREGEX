from flask import Blueprint, render_template, request, flash
import re
import html

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/reglas")
def reglas():
    return render_template("reglas.html")

@routes.route("/probar", methods=["GET", "POST"])
def probar():
    resultado = None
    regex_value = ""
    texto_value = ""
    conteo = 0
    coincidencias_list = []

    if request.method == "POST":
        regex_value = request.form.get("regex", "") or ""
        texto_value = request.form.get("texto", "") or ""

        # Validar regex
        try:
            patron = re.compile(regex_value)
        except re.error:
            flash("❌ La expresión regex no es válida", "danger")
            return render_template("probar.html",
                                   regex_value=regex_value,
                                   texto_value=texto_value,
                                   resultado=None,
                                   conteo=0,
                                   coincidencias_list=[])

        # Validar texto mínimo 5 líneas
        if len(texto_value.strip().splitlines()) < 5:
            flash("⚠️ El texto debe contener al menos 5 líneas", "warning")
            return render_template("probar.html",
                                   regex_value=regex_value,
                                   texto_value=texto_value,
                                   resultado=None,
                                   conteo=0,
                                   coincidencias_list=[])

        # Buscar coincidencias (lista exacta)
        coincidencias_list = patron.findall(texto_value)
        conteo = len(coincidencias_list)

        # Construir 'resultado' de forma segura:
        # escapamos todas las porciones no coincidentes y reemplazamos
        # cada coincidencia por <mark>escaped(match)</mark>
        parts = []
        last = 0
        for m in patron.finditer(texto_value):
            s, e = m.span()
            # texto entre last y s (escapado)
            parts.append(html.escape(texto_value[last:s]))
            # match escapado dentro de mark
            parts.append(f'<mark style="background-color:#FFD700; color:#000;">{html.escape(m.group(0))}</mark>')
            last = e
        parts.append(html.escape(texto_value[last:]))
        resultado = "".join(parts)

    return render_template("probar.html",
                           regex_value=regex_value,
                           texto_value=texto_value,
                           resultado=resultado,
                           conteo=conteo,
                           coincidencias_list=coincidencias_list)
