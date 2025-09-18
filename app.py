from flask import Flask
from routes import routes  # blueprint

app = Flask(__name__, template_folder="templates")
app.secret_key = "una_clave_muy_secreta_123"  # necesario para flash()
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
