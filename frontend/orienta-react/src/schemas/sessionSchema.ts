import { z } from "zod";

export const SessionUserDataSchema = z.object({
  userId: z.string(),
  username: z.string(),
  email: z.email(),
});

export const LoginResponseSchema = z.object({
  message: z.string(),
});

export const LogoutResponseSchema = z.object({
  message: z.string(),
});

export const CurrentUserResponseSchema = z.object({
  message: z.string(),
  data: SessionUserDataSchema,
});

export type SessionUserData = z.infer<typeof SessionUserDataSchema>;
export type LoginResponse = z.infer<typeof LoginResponseSchema>;
export type SessionUserResponse = z.infer<typeof CurrentUserResponseSchema>;
export type LogoutResponse = z.infer<typeof LogoutResponseSchema>;
