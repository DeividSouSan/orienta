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
from flask import Response, jsonify, make_response

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
app = Flask(__name__)


# Register blueprints
app.register_blueprint(blueprint=status_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=user_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=users_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=session_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=guides_bp, url_prefix="/api/v1")
app.register_blueprint(blueprint=validations_bp, url_prefix="/api/v1")


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
