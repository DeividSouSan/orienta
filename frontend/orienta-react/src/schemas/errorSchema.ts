import { z } from "zod";

export const ErrorSchema = z.object({
  name: z.string(),
  message: z.string(),
  action: z.string(),
  code: z.int(),
});

export type ErrorResponse = z.infer<typeof ErrorSchema>;
