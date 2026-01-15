import { APIError } from "@/errors";
import { CreateUserRequest } from "@/schemas/userSchema";
import { userService } from "@/services/userService";
import { useState } from "react";

type Result = {
  success: boolean;
  message: string;
};

export function useUser() {
  const [isLoading, setIsLoading] = useState(false);

  const register = async (data: CreateUserRequest): Promise<Result> => {
    setIsLoading(true);

    try {
      const result = await userService.createUser(data);
      return {
        success: true,
        message: result.message,
      };
    } catch (error) {
      console.error(error);
      let message = null;
      if (error instanceof APIError) {
        message = error.message;
      }

      return {
        success: false,
        message: message || "Não foi possível criar o usuário.",
      };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    register,
    isLoading,
  };
}
