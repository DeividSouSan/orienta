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

export default function SignupPage() {
    const [loading, setLoading] = useState(false);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [errorMessage, setErrorMessage] = useState("");

    const router = useRouter();

    async function handleSubmit() {
        const response = await fetch("/api/v1/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                confirmPassword: confirmPassword,
            }),
        });

        if (response.ok) {
            console.log("User registered successfully");
            router.push("/login");
        } else {
            // Handle error
            console.error("Error registering user");
            const error = await response.json();
            setErrorMessage(error.action);
        }
    }

    async function validateForm(event) {
        event.preventDefault();

        let valid = true;
        setLoading(true);
        setErrorMessage("");

        // validar username
        if (username.length < 3 || username.length > 20) {
            setErrorMessage(
                "O nome de usuário deve conter entre 3 e 20 caracteres.",
            );
            valid = false;
        }
        // validar senha
        if (password.length < 6) {
            setErrorMessage("A senha deve conter mais de 6 caracteres.");
            valid = false;
        }

        // validar confirmação de senha
        if (confirmPassword !== password) {
            setErrorMessage("A confirmação de senha não coincide.");
            valid = false;
        }

        // tudo ok
        if (valid) {
            await handleSubmit();
        } else {
            setLoading(false);
        }
    }

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
                                {errorMessage ? (
                                    <p> {errorMessage} </p>
                                ) : (
                                    <p>
                                        Crie sua conta para começar a gerar
                                        guias.
                                    </p>
                                )}
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={validateForm}>
                                <FieldGroup>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="username">
                                            Nome de usuário
                                        </FieldLabel>
                                        <Input
                                            id="username"
                                            type="text"
                                            placeholder="username"
                                            required
                                            onChange={(e) =>
                                                setUsername(e.target.value)
                                            }
                                        />
                                        <FieldDescription>
                                            *Deve conter de 3 a 20 caracteres.
                                        </FieldDescription>
                                    </Field>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="email">
                                            E-mail
                                        </FieldLabel>
                                        <Input
                                            id="email"
                                            type="email"
                                            placeholder="email@orienta.com"
                                            required
                                            onChange={(e) =>
                                                setEmail(e.target.value)
                                            }
                                        />
                                        <FieldDescription>
                                            Insira um e-mail válido.
                                        </FieldDescription>
                                    </Field>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="password">
                                            Senha
                                        </FieldLabel>
                                        <Input
                                            id="password"
                                            type="password"
                                            required
                                            onChange={(e) =>
                                                setPassword(e.target.value)
                                            }
                                        />
                                        <FieldDescription>
                                            Insira uma senha maior que 6
                                            caracteres.
                                        </FieldDescription>
                                    </Field>
                                    <Field className="animate-fade-in animation-delay-400">
                                        <FieldLabel htmlFor="confirm-password">
                                            Confirmação de senha
                                        </FieldLabel>
                                        <Input
                                            id="confirm-password"
                                            type="password"
                                            required
                                            onChange={(e) =>
                                                setConfirmPassword(
                                                    e.target.value,
                                                )
                                            }
                                        />
                                        <FieldDescription>
                                            Confirme sua senha.
                                        </FieldDescription>
                                    </Field>
                                    <FieldGroup>
                                        <Field className="animate-fade-in animation-delay-600">
                                            {loading ? (
                                                <SpinnerButton
                                                    type="submit"
                                                    disabled={loading}
                                                >
                                                    Criando conta...
                                                </SpinnerButton>
                                            ) : (
                                                <Button type="submit">
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
