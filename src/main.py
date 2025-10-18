import os
import traceback
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
)

from src.errors import InternalServerError, ServiceError, ValidationError
import src.models.firebase as firebase


from src.api.user import user_bp

# App configuration

app = Flask(__name__)

ENV = os.getenv("ENVIRONMENT")

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api/v1")

# Initialize Firebase
firebase.initialize_app()


# Global error handler


@app.errorhandler(Exception)  # type: ignore
def handle_api_error(error: Exception) -> Response:
    print("O erro foi ", error)
    traceback.print_exc()

    if isinstance(error, ValidationError) or isinstance(error, ServiceError):
        return make_response(jsonify(error.toDict()), error.code)

    error = InternalServerError()
    return make_response(jsonify(error.toDict()), 500)
