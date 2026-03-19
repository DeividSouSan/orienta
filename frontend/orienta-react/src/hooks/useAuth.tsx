import { APIError } from "@/errors";
import { SessionUserData } from "@/schemas/sessionSchema";
import { authService } from "@/services/authService";
import {
  createContext,
  useState,
  useEffect,
  type ReactNode,
  useContext,
} from "react";

type Result = {
  success: boolean;
  message: string;
};

interface AuthContextValue {
  isAuthenticated: boolean;
  currentUser: SessionUserData | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<Result>;
  logout: () => Promise<Result>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<SessionUserData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const login = async (email: string, password: string): Promise<Result> => {
    setIsLoading(true);

    try {
      const result = await authService.createSession(email, password);
      console.log(result);

      // Fetch user data after successful session creation
      const userData = await authService.getCurrentUser();
      setCurrentUser(userData.data);
      setIsAuthenticated(true);

      return {
        success: true,
        message: result.message,
      };
    } catch (error) {
      let message = "Um erro não interno aconteceu.";

      if (error instanceof APIError) {
        message = error.message;
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<Result> => {
    setIsLoading(true);
    try {
      const result = await authService.deleteSession();
      setCurrentUser(null);
      setIsAuthenticated(false);
      return {
        success: true,
        message: result.message,
      };
    } catch (error) {
      let message = "Um erro interno aconteceu.";

      if (error instanceof APIError) {
        message = error.message;
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const result = await authService.getCurrentUser();
        setIsAuthenticated(true);
        setCurrentUser(result.data);
        return { success: true, message: result.message };
      } catch (error) {
        return await logout();
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();
  }, []);

  const value = {
    isAuthenticated,
    currentUser,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth(): AuthContextValue {
  return useContext(AuthContext)!;
}
