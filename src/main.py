import os
import traceback
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
)
from src.errors import (
    InternalServerError,
    ServiceError,
    UnauthorizedError,
    ValidationError,
)
import src.models.firebase as firebase


from src.api.user import user_bp
from src.api.sessions import session_bp

# Check environment variables
ENV = os.getenv("ENVIRONMENT")

print(f"Variáveis de Ambiente ({ENV}): ")
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is None:
    print("❌ GOOGLE_APPLICATION_CREDENTIALS")
else:
    print("✔ GOOGLE_APPLICATION_CREDENTIALS")

if ENV != "development":
    if os.getenv("GOOGLE_SERVICES_JSON") is None:
        print("❌ GOOGLE_SERVICES_JSON")
    else:
        print("✔ GOOGLE_SERVICES_JSON")


if os.getenv("GEMINI_API_KEY") is None:
    print("❌ GEMINI_API_KEY")
else:
    print("✔ GEMINI_API_KEY")

if os.getenv("FIREBASE_API_KEY") is None:
    print("❌ FIREBASE_API_KEY")
else:
    print("✔ FIREBASE_API_KEY")

if ENV != "production":
    if os.getenv("API_URL") is None:
        print("❌ API_URL")
    else:
        print("✔ API_URL")

print("\n")

print("Arquivos: ")

if os.path.exists("service-account.json"):
    print("✔ 'service-account.json' EXISTE")
else:
    print("❌ 'service-account.json' NÃO EXISTE")

print("\n\n")
# App configuration

app = Flask(__name__)


# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api/v1")
app.register_blueprint(session_bp, url_prefix="/api/v1")

# Initialize Firebase
firebase.initialize_app()


# Global error handler


@app.errorhandler(Exception)  # type: ignore
def handle_api_error(error: Exception) -> Response:
    print("O erro foi ", error)
    traceback.print_exc()

    if (
        isinstance(error, ValidationError)
        or isinstance(error, ServiceError)
        or isinstance(error, UnauthorizedError)
    ):
        return make_response(jsonify(error.toDict()), error.code)

    error = InternalServerError()
    return make_response(jsonify(error.toDict()), 500)
