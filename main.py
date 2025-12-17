import os
import sys
from flask import Flask

from api.v1.user import user_bp
from api.v1.sessions import session_bp
from api.v1.guides import guides_bp
from api.v1.users import users_bp
from api.v1.validate import validations_bp
from api.v1.status import status_bp
from utils import initialize_app

import traceback
from flask import Response, jsonify, make_response, send_from_directory

from errors import (
    InternalServerError,
    MethodNotAllowed,
    NotFoundError,
    ServiceError,
    UnauthorizedError,
    ValidationError,
    ConflictError,
)


# Check environment variables and initialize firebase
try:
    initialize_app()
except EnvironmentError as e:
    print(f"Falha na inicialização: {e}")
    sys.exit(1)

# App configuration
app = Flask(__name__, static_folder="client/out", static_url_path="")


# Register blueprints
app.register_blueprint(blueprint=status_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=user_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=users_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=session_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=guides_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=validations_bp, url_prefix="/api/v1")

# Static Pages


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    # Ignorar chamadas de API
    if path.startswith("api"):
        return make_response(jsonify({"message": "API endpoint not found"}), 404)

    # 1. Tentar servir o arquivo exato (ex: favicon.ico, _next/static/...)
    full_path = os.path.join(app.static_folder, path)
    if path and os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)

    # 2. Tentar servir o index.html da pasta (padrão trailingSlash do Next.js)
    # Ex: /login -> dist/login/index.html
    index_path = os.path.join(full_path, "index.html")
    if os.path.isfile(index_path):
        return send_from_directory(app.static_folder, os.path.join(path, "index.html"))

    # 3. Fallback para o index.html principal (SPA behavior)
    return send_from_directory(app.static_folder, "index.html")


# Error handlers
@app.errorhandler(405)
def handle_method_not_allowed(error):
    error = MethodNotAllowed()
    return make_response(jsonify(error.toDict()), error.code)


@app.errorhandler(404)
def handle_not_found_error(error):
    error = NotFoundError()
    return make_response(jsonify(error.toDict()), error.code)


@app.errorhandler(Exception)
def handle_api_error(error: Exception) -> Response:
    print("O erro foi ", error)
    traceback.print_exc()

    if (
        isinstance(error, ValidationError)
        or isinstance(error, ServiceError)
        or isinstance(error, UnauthorizedError)
        or isinstance(error, NotFoundError)
        or isinstance(error, ConflictError)
    ):
        return make_response(jsonify(error.toDict()), error.code)

    error = InternalServerError()
    return make_response(jsonify(error.toDict()), 500)
