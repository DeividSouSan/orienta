import { z } from "zod";

export const CreateUserRequestSchema = z.object({
  username: z.string(),
  email: z.email(),
  password: z.string(),
});

export const UserDataSchema = z.object({
  uid: z.string(),
  username: z.string(),
  email: z.email(),
  created_at: z.string(),
});

export const UserResponseSchema = z.object({
  message: z.string(),
  data: UserDataSchema,
});

export type UserData = z.infer<typeof UserDataSchema>;
export type UserResponse = z.infer<typeof UserResponseSchema>;
export type CreateUserRequest = z.infer<typeof CreateUserRequestSchema>;
