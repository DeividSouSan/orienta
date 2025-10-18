import os
import random
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    g,
)
from werkzeug.exceptions import HTTPException, MethodNotAllowed, NotFound

from src.errors import (
    UnauthorizedError,
    ValidationError,
    InternalServerError,
    ServiceError,
)
from src.models import user, auth, session, guide
import src.models.firebase as firebase

import traceback
from src.actions import api

ENV = os.getenv("ENVIRONMENT")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.register_blueprint(api, url_prefix="/api")
firebase.initialize_app()


ERROR = "red"
WARN = "yellow"
SUCCESS = "green"


def is_logged():
    session_cookie = request.cookies.get("session_id")
    if not session_cookie:
        return False

    try:
        decoded_claims = session.verify(session_cookie)
        g.username = decoded_claims.get("name")
        g.uid = decoded_claims.get("user_id")
        return True
    except UnauthorizedError:
        return False


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/", methods=["GET"])
def index():
    if is_logged():
        return redirect("/plan")

    return render_template("index.html")


@app.route("/plan", methods=["GET"])
def plan():
    if not is_logged():
        flash(
            "Você não está autorizado e portanto não tem acesso à essa rota! Você foi redirecionado para uma rota permitida.",
            ERROR,
        )
        return redirect("/")

    return render_template("plan.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged():
        flash(
            "Usuário já está autenticado! Você foi redirecionado para uma rota autorizada.",
            ERROR,
        )
        flash("Se quiser criar um novo cadastro primeiro faça logout.", WARN)

        return redirect("/plan")

    if request.method == "POST":
        try:
            user.create(
                username=request.form["username"],
                email=request.form["email"],
                password=request.form["password"],
            )

            flash("Usuário criado com sucesso! Faça login para entrar.", SUCCESS)

            return redirect("/login")

        except Exception as error:
            if isinstance(error, ValidationError) or isinstance(error, ServiceError):
                flash(error.message, ERROR)
            else:
                error = InternalServerError()
                flash(error.message, ERROR)

            traceback.print_exc()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged():
        flash(
            "Usuário já está autenticado! Você foi redirecionado para uma rota autorizada.",
            ERROR,
        )
        flash(
            "Se quiser fazer login em outra conta primeiro faça logout.",
            WARN,
        )

        return redirect("/plan")

    if request.method == "POST":
        try:
            authenticated_user = auth.authenticate(
                email=request.form["email"], password=request.form["password"]
            )

            session_cookie = session.create(authenticated_user["idToken"])

            response = make_response(redirect("/plan"))
            response.set_cookie(
                key="session_id",
                value=session_cookie,
                max_age=session.DURATION_IN_SECONDS,
                httponly=True,
                path="/",
                secure=(ENV == "production"),
            )

            flash("Autenticação efetuada com sucesso!", SUCCESS)
            return response

        except Exception as error:
            if isinstance(error, UnauthorizedError) or isinstance(error, ServiceError):
                flash(error.message, ERROR)
            else:
                error = InternalServerError()
                flash(error.message, ERROR)

            traceback.print_exc()

    quotes = [
        "Sem direção? Faça login que a gente te Orienta.",
        "Encontre o seu norte. Faça o login para continuar.",
        "A bússola para o seu conhecimento aponta para cá.",
        "O conhecimento está a um login de distância.",
        "Foco no objetivo. O caminho já foi traçado.",
        "Um passo de cada vez. Vamos retomar o plano.",
    ]

    return render_template("login.html", quote=random.choice(quotes))


@app.route("/logout", methods=["POST"])  # tem que ser só POST
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie("session_id")
    flash("Usuário deslogado com sucesso!", SUCCESS)
    return response


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if not is_logged():
        flash(
            "Para gerar um guia você precisa estar autenticado. Faça login.",
            ERROR,
        )
        return redirect("/login")

    if request.method == "POST":
        inputs = {
            "topic": request.form["study-topic"],
            "objective": request.form["objective"],
            "study_time": request.form["study-time"],
            "duration_time": request.form["duration-value"],
            "knowledge": request.form["knowledge"],
        }

        try:
            study_plan: dict = guide.build(uid=g.uid, inputs=inputs)
            guide.save(study_plan)
        except Exception as error:
            if isinstance(error, ValidationError) or isinstance(error, ServiceError):
                flash(error.message, ERROR)
            else:
                error = InternalServerError()
                flash(error.message, ERROR)

            traceback.print_exc()

    return render_template("generate.html")


@app.route("/guides", methods=["GET"])
def my_guides():
    if not is_logged():
        flash(
            "Para ver os seus guias você precisa estar autenticado. Faça login.",
            ERROR,
        )
        return redirect("/login")

    try:
        all_guides = guide.find_guides(g.uid)

    except Exception as error:
        if isinstance(error, ServiceError):
            flash(error.message, ERROR)
        else:
            error = InternalServerError()
            flash(error.message, ERROR)

    return render_template("my-guides.html", guides=all_guides)


@app.route("/guides/<string:guide_id>")
def guide_study_plan(guide_id):
    if not is_logged():
        flash(
            "Para visualizar os detalhes de um guia você precisa estar autenticado.",
            ERROR,
        )
        return redirect("/")

    try:
        study_guide_list = guide.retrieve_daily_plan(guide_id)
    except Exception as error:
        if isinstance(error, ServiceError):
            flash(error.message, ERROR)
        else:
            error = InternalServerError()
            flash(error.message, ERROR)

    return render_template("guide.html", daily_study_list=study_guide_list)


@app.route("/status")
def status():
    status = firebase.check_status()
    return render_template("status.html", status=status)


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e: MethodNotAllowed):
    traceback.print_exc()
    return redirect("/")


@app.errorhandler(NotFound)
def handle_not_found_error(e: NotFound):
    accept = request.headers.get("Accept", "")
    if "text/html" in accept:
        flash("Essa página não existe.", ERROR)
        return redirect("/")

    return "", 204


@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    flash("Um erro aconteceu. Tente novamente mais tarde.", ERROR)
    traceback.print_exc()
    return redirect("/")


@app.errorhandler(Exception)
def handle_generic_exception(e):
    error = InternalServerError()
    flash(error.message, ERROR)
    traceback.print_exc()
    return redirect("/")
