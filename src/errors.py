class ValidationError(Exception):
    def __init__(
        self,
        message: str = "Um erro de validação ocorreu.",
        action: str = "Ajuste os dados enviados e tente novamente.",
    ):
        self.name = "ValidationError"
        self.message = message
        self.action = action
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(
        self,
        message: str = "Usuário não autenticado.",
        action: str = "Faça login novamente para continuar.",
    ):
        self.name = "UnauthorizedError"
        self.message = message
        self.action = action
        super().__init__(self.message)


class InternalServerError(Exception):
    def __init__(
        self,
        message: str = "Um erro interno inesperado aconteceu. Envie um e-mail para deividsantana2013@gmail.com.",
    ):
        self.name = "InternalServerError"
        self.message = message
        super().__init__(self.message)


class ServiceError(Exception):
    def __init__(
        self,
        message: str = "Um erro inesperado em serviço aconteceu.",
        action: str = "Entre em contado com o suporte.",
    ):
        self.name = "ServiceError"
        self.message = message
        self.action = action
        super().__init__(self.message)
