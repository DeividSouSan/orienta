/*
Serviços fazem requisições à API do Orienta, validando os dados de
entrada e os dados de saída utilizando a biblioteca Zod.

Os argumentos são esquemas de requisição (FooRequest) que são validados
(utilizando .parse) na página, antes de serem fornecidos como
argumento para os Serviços. Os retornos são as respostas, que devem
aderir ao esquema e portanto são validadas utilizando .parse().

Serviços sobem erros! Caso a resposta da API seja diferente de 200-299
um erro ocorreu. As mensagens de erro da API já são formatados por
isso é possível usar throw new APIError(error) diretamente.
*/

import { APIError } from "@/errors";
import {
  CreateUserRequest,
  UserResponse,
  UserResponseSchema,
} from "@/schemas/userSchema";

async function createUser(data: CreateUserRequest): Promise<UserResponse> {
  const response = await fetch("/api/v1/users", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new APIError(error);
  }

  const responseBody = await response.json();
  const validatedResponse = UserResponseSchema.parse(responseBody);
  return validatedResponse;
}

export const userService = {
  createUser,
};
