import { useEffect, ReactNode } from "react";
import { useNavigate } from "react-router";
import { useAuth } from "@/hooks/useAuth";

export default function GuestGuard({ children }: { children: ReactNode }) {
  const auth = useAuth();
  const navigate = useNavigate();

  const { isAuthenticated, isLoading } = auth;

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, isLoading, navigate]);

  return <>{children}</>;
}
