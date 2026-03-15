"use client";

import { cn } from "@/lib/utils";
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
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { SpinnerButton } from "./ui/spinner-button";
import { useAuth } from "@/hooks/useAuth";
import { useMessage } from "@/hooks/useMessage";

export function LoginForm({ className, ...props }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { addMessage } = useMessage();

  async function onSubmit(event) {
    event.preventDefault();

    setLoading(true);

    const result = await login(
      event.target.email.value,
      event.target.password.value,
    );

    if (result.success) {
      addMessage({
        type: "success",
        text: "Login realizado com sucesso!",
      });
      navigate("/dashboard");
      return;
    } else {
      console.error("O backend não conseguiu logar o usuário.");
      addMessage({
        type: "error",
        text: "Falha no login. Verifique suas credenciais e tente novamente.",
      });
      setLoading(false);
    }
  }

  return (
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
            <form onSubmit={onSubmit}>
              <FieldGroup>
                <Field className="animate-fade-in animation-delay-400">
                  <FieldLabel htmlFor="email">E-mail</FieldLabel>
                  <Input
                    id="email"
                    type="email"
                    placeholder="user@example.com"
                    required
                  />
                  <FieldDescription>Insira seu e-mail</FieldDescription>
                </Field>
                <Field className="animate-fade-in animation-delay-400">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <Input id="password" type="password" required />
                  <FieldDescription>Insira sua senha.</FieldDescription>
                </Field>
                <Field className="animate-fade-in animation-delay-600">
                  {loading ? (
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
  );
}
