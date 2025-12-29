class ValidationError(Exception):
    def __init__(
        self,
        message: str = "Ocorreu um erro de validação nos dados fornecidos.",
        action: str = "Verifique os dados e tente novamente.",
    ):
        self.name = "ValidationError"
        self.message = message
        self.action = action
        self.code = 400

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class UnauthorizedError(Exception):
    def __init__(
        self,
        message: str = "Você não está autorizado a acessar este recurso.",
        action: str = "Verifique os dados e tente novamente.",
    ):
        self.name = "UnauthorizedError"
        self.message = message
        self.action = action
        self.code = 401

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class InternalServerError(Exception):
    def __init__(
        self,
        message: str = "Um erro interno inesperado aconteceu. Envie um e-mail para deividsantana2013@gmail.com.",
    ):
        self.name = "InternalServerError"
        self.message = message
        self.action = "Tente novamente mais tarde."
        self.code = 500

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class ServiceError(Exception):
    def __init__(
        self,
        message: str = "Um erro inesperado em serviço aconteceu.",
        action: str = "Entre em contado com o suporte.",
    ):
        self.name = "ServiceError"
        self.message = message
        self.action = action
        self.code = 503

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class MethodNotAllowed(Exception):
    def __init__(
        self,
        message: str = "O método HTTP utilizado não é permitido.",
        action: str = "Corrija o método HTTP utilizado.",
    ):
        self.name = "MethodNotAllowed"
        self.message = message
        self.action = action
        self.code = 405

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class NotFoundError(Exception):
    def __init__(
        self,
        message: str = "O recurso solicitado não foi encontrado.",
        action: str = "Verifique se o recurso solicitado exisste e tente novamente.",
    ):
        self.name = "NotFoundError"
        self.message = message
        self.action = action
        self.code = 404

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }


class ConflictError(Exception):
    def __init__(
        self,
        message: str = "Um erro de conflito aconteceu.",
        action: str = "Verifique se o dado fornecido é único e tente novamemnte.",
    ):
        self.name = "ConflictError"
        self.message = message
        self.action = action
        self.code = 409

        super().__init__(self.message)

    def toDict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "code": self.code,
        }
