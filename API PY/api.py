from flask import Flask

from endpoints.serie_A import serieA_bp
from endpoints.serie_B import serieB_bp
from endpoints.serie_C import serieC_bp
from endpoints.serie_D import serieD_bp

app = Flask(__name__)

# Registro dos Blueprints
app.register_blueprint(serieA_bp)
app.register_blueprint(serieB_bp)
app.register_blueprint(serieC_bp)
app.register_blueprint(serieD_bp)

if __name__ == "__main__":
    app.run(debug=True)
