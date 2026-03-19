import GuestGuard from "@/components/guest-guard";
import { Button } from "@/components/ui/button";
import { SpinnerButton } from "@/components/ui/spinner-button";
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
import { useMessage } from "@/hooks/useMessage";
import { useUser } from "@/hooks/useUser";
import { z } from "zod";
import { Eye, EyeOff } from "lucide-react";

const RegisterFormSchema = z
  .object({
    username: z
      .string()
      .min(3, "Nome de usuário deve ter no mínimo 3 caracteres."),
    email: z.email("Email inválido."),
    password: z.string().min(6, "Senha deve ter mais de 6 caracteres."),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "As senhas não coincidem.",
    path: ["confirmPassword"],
  });

type RegisterFormData = z.infer<typeof RegisterFormSchema>;

export default function RegisterPage() {
  const navigate = useNavigate();
  const message = useMessage();
  const user = useUser();

  const { register, isLoading } = user;
  const { errorMessage, successMessage } = message;

  const [formData, setFormData] = useState<RegisterFormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const submit = async () => {
    const result = await register(formData);

    if (!result.success) {
      errorMessage(result.message);
      return;
    }
    successMessage(result.message);
    navigate("/login");
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      RegisterFormSchema.parse(formData);
      submit();
    } catch (error) {
      if (error instanceof z.ZodError) {
        error.issues.forEach((err) => {
          errorMessage(err.message);
        });
      }
    }
  };

  return (
    <GuestGuard>
      <div className="flex min-h-full items-center justify-center px-6 py-12">
        <div className="w-full max-w-2xl">
          <Card className="animate-fade-in">
            <CardHeader className="text-xl font-serif">
              <CardTitle className="animate-fade-in animation-delay-200">
                Cadastre-se
              </CardTitle>
              <CardDescription className="animate-fade-in animation-delay-400">
                <p>Crie sua conta para começar a gerar guias.</p>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit}>
                <FieldGroup>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="username">Nome de usuário</FieldLabel>
                    <Input
                      id="username"
                      type="text"
                      placeholder="Deve conter no mínimo 3 caracteres."
                      required
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          username: e.target.value,
                        })
                      }
                    />
                  </Field>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="email">E-mail</FieldLabel>
                    <Input
                      id="email"
                      type="email"
                      placeholder="Insira seu melhor e-mail."
                      required
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          email: e.target.value,
                        })
                      }
                    />
                  </Field>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="password">Senha</FieldLabel>
                    <div className="relative">
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        placeholder="Insira uma senha maior que 6 caracteres."
                        required
                        className="pr-10"
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            password: e.target.value,
                          })
                        }
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
                  </Field>
                  <Field className="animate-fade-in animation-delay-400">
                    <FieldLabel htmlFor="confirm-password">
                      Confirmação de senha
                    </FieldLabel>
                    <div className="relative">
                      <Input
                        id="confirm-password"
                        type={showConfirmPassword ? "text" : "password"}
                        placeholder="Insira sua senha novamente."
                        required
                        className="pr-10"
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            confirmPassword: e.target.value,
                          })
                        }
                      />
                      <button
                        type="button"
                        onClick={() =>
                          setShowConfirmPassword(!showConfirmPassword)
                        }
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground focus:outline-none"
                        aria-label={
                          showConfirmPassword
                            ? "Hide password"
                            : "Show password"
                        }
                      >
                        {showConfirmPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </Field>
                  <FieldGroup>
                    <Field className="animate-fade-in animation-delay-600">
                      {isLoading ? (
                        <SpinnerButton type="submit" disabled={isLoading}>
                          Criando conta...
                        </SpinnerButton>
                      ) : (
                        <Button type="submit">Criar Conta</Button>
                      )}
                      <FieldDescription className="px-6 text-center">
                        Já tem uma conta? <Link to="/login">Faça login.</Link>
                      </FieldDescription>
                    </Field>
                  </FieldGroup>
                </FieldGroup>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </GuestGuard>
  );
}
