"use client";

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
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMessage } from "@/hooks/useMessage";
import { success } from "zod";

export default function SignupPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);

    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
    });

    const { successMessage, errorMessage } = useMessage();

    const handleSubmit = async () => {
        setIsLoading(true);

        try {
            const response = await fetch("/api/v1/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            const responseBody = await response.json();

            if (response.ok) {
                successMessage(responseBody.message);
                return router.push("/login");
            } else {
                errorMessage(responseBody.message);
                return;
            }
        } catch (error) {
            errorMessage(
                "Um erro interno aconteceu. Tente novamente mais tarde.",
            );
            return;
        } finally {
            setIsLoading(false);
            return;
        }
    };

    const validateForm = async () => {
        let valid = true;

        setIsLoading(true);

        if (formData.username.length < 3) {
            errorMessage("O nome de usuário deve conter no mínimo 3.");
            valid = false;
        }

        if (formData.password.length < 6) {
            errorMessage("A senha deve conter mais de 6 caracteres.");
            valid = false;
        }

        if (formData.confirmPassword !== formData.password) {
            errorMessage("A confirmação de senha não coincide.");
            valid = false;
        }

        if (valid) await handleSubmit();
        else {
            setIsLoading(false);
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
                                <p>
                                    Crie sua conta para começar a gerar guias.
                                </p>
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form>
                                <FieldGroup>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="username">
                                            Nome de usuário
                                        </FieldLabel>
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
                                        <FieldLabel htmlFor="email">
                                            E-mail
                                        </FieldLabel>
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
                                        <FieldLabel htmlFor="password">
                                            Senha
                                        </FieldLabel>
                                        <Input
                                            id="password"
                                            type="password"
                                            placeholder="Insira uma senha maior que 6 caracteres."
                                            required
                                            onChange={(e) =>
                                                setFormData({
                                                    ...formData,
                                                    password: e.target.value,
                                                })
                                            }
                                        />
                                    </Field>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="confirm-password">
                                            Confirmação de senha
                                        </FieldLabel>
                                        <Input
                                            id="confirm-password"
                                            type="password"
                                            placeholder="Insira sua senha novamente."
                                            required
                                            onChange={(e) =>
                                                setFormData({
                                                    ...formData,
                                                    confirmPassword:
                                                        e.target.value,
                                                })
                                            }
                                        />
                                    </Field>
                                    <FieldGroup>
                                        <Field className="animate-fade-in animation-delay-600">
                                            {isLoading ? (
                                                <SpinnerButton
                                                    type="submit"
                                                    disabled={isLoading}
                                                >
                                                    Criando conta...
                                                </SpinnerButton>
                                            ) : (
                                                <Button
                                                    type="submit"
                                                    onClick={validateForm}
                                                >
                                                    Criar Conta
                                                </Button>
                                            )}
                                            <FieldDescription className="px-6 text-center">
                                                Já tem uma conta?{" "}
                                                <Link href="/login">
                                                    Faça login.
                                                </Link>
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
