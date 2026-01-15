import { APIError } from "@/errors";
import { ErrorSchema } from "@/schemas/errorSchema";
import {
  CurrentUserResponseSchema,
  LoginResponse,
  LoginResponseSchema,
  LogoutResponse,
  LogoutResponseSchema,
  SessionUserResponse,
} from "@/schemas/sessionSchema";

async function getCurrentUser(): Promise<SessionUserResponse> {
  const response = await fetch("/api/v1/user", {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new APIError(error);
  }

  const responseBody = await response.json();
  const validatedResponse = CurrentUserResponseSchema.parse(responseBody);
  return validatedResponse;
}

async function createSession(
  email: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch("/api/v1/sessions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new APIError(error);
  }

  const responseBody = await response.json();
  const validatedResponse = LoginResponseSchema.parse(responseBody);
  return validatedResponse;
}

async function deleteSession(): Promise<LogoutResponse> {
  const response = await fetch("/api/v1/sessions", {
    method: "DELETE",
    credentials: "include",
  });

  if (!response.ok) {
    const error = ErrorSchema.parse(await response.json());
    throw new APIError(error);
  }

  const responseBody = await response.json();
  const validatedResponse = LogoutResponseSchema.parse(responseBody);
  return validatedResponse;
}

export const authService = {
  createSession,
  deleteSession,
  getCurrentUser,
};
