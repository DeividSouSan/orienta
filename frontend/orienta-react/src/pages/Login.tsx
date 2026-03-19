import GuestGuard from "@/components/guest-guard";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { SpinnerButton } from "@/components/ui/spinner-button";
import { useAuth } from "@/hooks/useAuth";
import { useMessage } from "@/hooks/useMessage";
import { Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const navigate = useNavigate();
  const auth = useAuth();
  const message = useMessage();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const { login, isLoading } = auth;
  const { successMessage, errorMessage } = message;

  const submit = async (email: string, password: string) => {
    const result = await login(email, password);

    if (!result.success) {
      errorMessage(result.message);
      return;
    }

    successMessage(result.message);
    navigate("/dashboard");
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    submit(email, password);
  };

  return (
    <GuestGuard>
      <div className="flex min-h-full items-center justify-center px-6 py-12">
        <div className="w-full max-w-2xl">
          <Card className="animate-fade-in">
            <CardHeader className="text-xl font-serif">
              <CardTitle className="animate-fade-in">Faça Login</CardTitle>
              <CardDescription className="animate-fade-in animation-delay-200">
                Envia o que quer estudar e a gente te orienta.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit}>
                <FieldGroup>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="email">E-mail</FieldLabel>
                    <Input
                      id="email"
                      type="email"
                      placeholder="user@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                    <FieldDescription>Insira seu e-mail</FieldDescription>
                  </Field>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="password">Password</FieldLabel>
                    <div className="relative">
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="pr-10"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground focus:outline-none"
                        aria-label={
                          showPassword ? "Hide password" : "Show password"
                        }
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                    <FieldDescription>Insira sua senha.</FieldDescription>
                  </Field>
                  <Field className="animate-fade-in animation-delay-600">
                    {isLoading ? (
                      <SpinnerButton>Entrando...</SpinnerButton>
                    ) : (
                      <Button type="submit">Entrar</Button>
                    )}
                    <FieldDescription className="text-center">
                      Não tem uma conta? <Link to="/register">Cadastre-se</Link>
                      .
                    </FieldDescription>
                  </Field>
                </FieldGroup>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </GuestGuard>
  );
}
