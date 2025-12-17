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
    FieldSet,
    FieldLegend,
    FieldSeparator,
} from "@/components/ui/field";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { SpinnerButton } from "./ui/spinner-button";
import { useAuth } from "@/contexts/AuthContext";
import { Textarea } from "./ui/textarea";
import { ArrowBigLeftDash, RotateCcw, Sparkles } from "lucide-react";
import { Progress } from "./ui/progress";
import { ErrorAlert } from "./error-alert";

// Constantes de validação
const VALIDATION_LIMITS = {
    TITLE_MIN: 3,
    TITLE_MAX: 40,
    TOPIC_MIN: 10,
    TOPIC_MAX: 150,
    FOCUS_TIME_MIN: 30,
    FOCUS_TIME_MAX: 480,
    DAYS_MIN: 3,
    DAYS_MAX: 30,
};

export function GuideForm({ className, ...props }) {
    const { logout } = useAuth();
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [step, setStep] = useState(1);

    // Form state
    const [title, setTitle] = useState("");
    const [topic, setTopic] = useState("");
    const [knowledge, setKnowledge] = useState("zero");
    const [focusTime, setFocusTime] = useState(30);
    const [days, setDays] = useState(3);

    function nextForm(e) {
        e.preventDefault();
        setStep(step + 1);
    }

    function previousForm(e) {
        e.preventDefault();
        setStep(step - 1);
    }

    function resetForm(e) {
        e.preventDefault();
        setTitle("");
        setTopic("");
        setKnowledge("zero");
        setFocusTime(30);
        setDays(3);
        setStep(1);
        setError("");
    }

    async function validateTopicRelevance(event) {
        if (!validateStep1()) {
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/api/v1/validate/topic", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({
                    topic: topic,
                }),
            });

            const responseBody = await response.json();

            if (response.ok) {
                setLoading(false);
                nextForm(event);
            } else {
                if (response.status === 401) {
                    logout();
                    router.push("/login");
                }
                setLoading(false);
                setError(
                    responseBody.message || "Tópico não aprovado. Tente outro.",
                );
            }
        } catch (error) {
            setLoading(false);
            setError(
                "Não conseguimos validar seu tópico. Verifique sua conexão e tente novamente.",
            );
        }
    }

    function validateStep1() {
        setError("");

        const trimmedTitle = title.trim();
        const trimmedTopic = topic.trim();

        if (!trimmedTitle) {
            setError("Qual é o título do seu estudo?");
            return false;
        }

        if (trimmedTitle.length < VALIDATION_LIMITS.TITLE_MIN) {
            setError(
                `O título precisa ter pelo menos ${VALIDATION_LIMITS.TITLE_MIN} caracteres.`,
            );
            return false;
        }

        if (!trimmedTopic) {
            setError("Conte-nos sobre o que você quer estudar.");
            return false;
        }

        if (trimmedTopic.length < VALIDATION_LIMITS.TOPIC_MIN) {
            setError("Descreva melhor seu tópico (mínimo 10 caracteres).");
            return false;
        }

        return true;
    }

    async function submit(e) {
        e.preventDefault();

        // Validação centralizada dentro do submit
        setError("");

        // Validar focusTime
        const parsedFocusTime = parseInt(focusTime) || 0;
        if (
            !parsedFocusTime ||
            parsedFocusTime < VALIDATION_LIMITS.FOCUS_TIME_MIN
        ) {
            setError(
                `Você precisa dedicar no mínimo ${VALIDATION_LIMITS.FOCUS_TIME_MIN} minutos por dia.`,
            );
            return;
        }

        if (parsedFocusTime > VALIDATION_LIMITS.FOCUS_TIME_MAX) {
            setError(
                `O máximo de tempo é ${VALIDATION_LIMITS.FOCUS_TIME_MAX} minutos por dia.`,
            );
            return;
        }

        // Validar days
        const parsedDays = parseInt(days) || 0;
        if (!parsedDays || parsedDays < VALIDATION_LIMITS.DAYS_MIN) {
            setError(
                `Seu guia precisa ter no mínimo ${VALIDATION_LIMITS.DAYS_MIN} dias.`,
            );
            return;
        }

        if (parsedDays > VALIDATION_LIMITS.DAYS_MAX) {
            setError(`O máximo de dias é ${VALIDATION_LIMITS.DAYS_MAX}.`);
            return;
        }

        setLoading(true);

        const guideInputs = {
            title: title.trim(),
            topic: topic.trim(),
            knowledge: knowledge,
            focus_time: parsedFocusTime,
            days: parsedDays,
        };

        try {
            const response = await fetch("/api/v1/guides", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify(guideInputs),
            });

            if (response.ok) {
                router.push("/dashboard/my-guides");
            } else {
                if (response.status === 401) {
                    logout();
                    router.push("/login");
                    return;
                }
                const responseBody = await response.json();
                setError(
                    responseBody.message ||
                    "Não conseguimos gerar seu guia. Tente novamente.",
                );
                setLoading(false);
            }
        } catch (error) {
            setError("Erro ao conectar com o servidor. Verifique sua conexão.");
            setLoading(false);
        }
    }

    function renderGuideSteps() {
        if (step === 1) {
            // Formulário 1: Tópico
            const hasError = error !== "";
            return (
                <FieldGroup>
                    <Field className="animate-fade-in animation-delay-400">
                        <FieldLabel
                            htmlFor="title"
                            className="text-sm sm:text-base"
                        >
                            Dê um nome para esse seu novo estudo
                        </FieldLabel>
                        <Input
                            id="title"
                            type="text"
                            placeholder="Ex.: Estudo sobre a Segunda Guerra Mundial"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            maxLength={VALIDATION_LIMITS.TITLE_MAX}
                            className={`text-sm sm:text-base ${hasError && !title.trim()
                                    ? "border-red-500 focus:ring-red-500"
                                    : ""
                                }`}
                            required
                        />
                        <FieldDescription className="text-xs sm:text-sm">
                            {title.length}/{VALIDATION_LIMITS.TITLE_MAX}
                        </FieldDescription>

                        <FieldLabel
                            htmlFor="topic"
                            className="text-sm sm:text-base"
                        >
                            O que você gostaria de estudar?
                        </FieldLabel>
                        <Textarea
                            id="topic"
                            placeholder="Ex.: Como a Segunda Guerra Mundial chegou ao fim e seus impactos globais."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            maxLength={VALIDATION_LIMITS.TOPIC_MAX}
                            className={`text-sm sm:text-base ${hasError && !topic.trim()
                                    ? "border-red-500 focus:ring-red-500"
                                    : ""
                                }`}
                            required
                        />
                        <FieldDescription className="text-xs sm:text-sm">
                            {topic.length}/{VALIDATION_LIMITS.TOPIC_MAX}
                        </FieldDescription>
                    </Field>
                    {error && (
                        <div className="mt-3">
                            <ErrorAlert
                                message={error}
                                onClose={() => setError("")}
                            />
                        </div>
                    )}
                    <Field>
                        {loading ? (
                            <SpinnerButton className="w-full">
                                Validando...
                            </SpinnerButton>
                        ) : (
                            <Button
                                className="w-full"
                                onClick={(e) => validateTopicRelevance(e)}
                            >
                                Avançar
                            </Button>
                        )}
                    </Field>
                </FieldGroup>
            );
        } else if (step === 2) {
            // Formulário 2: Nível de Conhecimento
            return (
                <FieldSet>
                    <FieldLegend className="text-sm sm:text-base">
                        Qual seu nível de conhecimento em relação a:
                    </FieldLegend>
                    <FieldDescription className="text-center text-sm sm:text-base break-words font-medium">
                        "{topic}"
                    </FieldDescription>
                    <FieldSeparator></FieldSeparator>
                    <RadioGroup value={knowledge} onValueChange={setKnowledge}>
                        <Field orientation="horizontal">
                            <RadioGroupItem value="zero" id="knowledge-zero" />
                            <FieldLabel
                                htmlFor="knowledge-zero"
                                className="text-sm sm:text-base cursor-pointer"
                            >
                                Nenhum conhecimento
                            </FieldLabel>
                        </Field>
                        <Field orientation="horizontal">
                            <RadioGroupItem
                                value="iniciante"
                                id="knowledge-beginner"
                            />
                            <FieldLabel
                                htmlFor="knowledge-beginner"
                                className="text-sm sm:text-base cursor-pointer"
                            >
                                Iniciante
                            </FieldLabel>
                        </Field>
                        <Field orientation="horizontal">
                            <RadioGroupItem
                                value="intermediario"
                                id="knowledge-intermediate"
                            />
                            <FieldLabel
                                htmlFor="knowledge-intermediate"
                                className="text-sm sm:text-base cursor-pointer"
                            >
                                Intermediário/Avançado
                            </FieldLabel>
                        </Field>
                    </RadioGroup>
                    <Field className="flex flex-col sm:flex-row mt-5">
                        <Button
                            className="w-full sm:flex-1"
                            onClick={(e) => nextForm(e)}
                        >
                            Avançar
                        </Button>
                    </Field>
                </FieldSet>
            );
        } else {
            // Formulário 3: Tempo de Estudo
            const hasError = error !== "";
            return (
                <FieldSet>
                    <FieldLegend className="font-bold text-lg sm:text-xl">
                        Informações temporais:
                    </FieldLegend>
                    <Field className="animate-fade-in">
                        <FieldLabel
                            htmlFor="focus-time"
                            className="text-sm sm:text-base"
                        >
                            Quanto tempo você pode se dedicar por dia (em
                            minutos)?
                        </FieldLabel>
                        <Input
                            id="focus-time"
                            type="number"
                            value={focusTime}
                            onChange={(e) => {
                                setFocusTime(e.target.value);
                            }}
                            min={VALIDATION_LIMITS.FOCUS_TIME_MIN}
                            max={VALIDATION_LIMITS.FOCUS_TIME_MAX}
                            className={`text-sm sm:text-base ${hasError &&
                                    (focusTime < VALIDATION_LIMITS.FOCUS_TIME_MIN ||
                                        focusTime >
                                        VALIDATION_LIMITS.FOCUS_TIME_MAX)
                                    ? "border-red-500 focus:ring-red-500"
                                    : ""
                                }`}
                            required
                        />
                        <FieldDescription className="text-xs sm:text-sm">
                            {VALIDATION_LIMITS.FOCUS_TIME_MIN} a{" "}
                            {VALIDATION_LIMITS.FOCUS_TIME_MAX} minutos
                        </FieldDescription>
                    </Field>
                    <Field className="animate-fade-in">
                        <FieldLabel
                            htmlFor="days"
                            className="text-sm sm:text-base"
                        >
                            Qual será a duração total do estudo (em dias)?
                        </FieldLabel>
                        <Input
                            id="days"
                            type="number"
                            value={days}
                            onChange={(e) => {
                                setDays(e.target.value);
                            }}
                            min={VALIDATION_LIMITS.DAYS_MIN}
                            max={VALIDATION_LIMITS.DAYS_MAX}
                            className={`text-sm sm:text-base ${hasError &&
                                    (days < VALIDATION_LIMITS.DAYS_MIN ||
                                        days > VALIDATION_LIMITS.DAYS_MAX)
                                    ? "border-red-500 focus:ring-red-500"
                                    : ""
                                }`}
                            required
                        />
                        <FieldDescription className="text-xs sm:text-sm">
                            {VALIDATION_LIMITS.DAYS_MIN} a{" "}
                            {VALIDATION_LIMITS.DAYS_MAX} dias
                        </FieldDescription>
                    </Field>
                    {error && (
                        <div className="mt-3">
                            <ErrorAlert
                                message={error}
                                onClose={() => setError("")}
                            />
                        </div>
                    )}
                    <Field className="flex flex-col sm:flex-row gap-2 sm:gap-3">
                        {loading ? (
                            <SpinnerButton className="w-full">
                                <Sparkles size={18} />
                                Gerando seu guia...
                            </SpinnerButton>
                        ) : (
                            <>
                                <Button
                                    className="w-full sm:flex-1 font-bold bg-gray-300 text-black hover:bg-gray-400"
                                    onClick={(e) => previousForm(e)}
                                >
                                    <ArrowBigLeftDash size={18} />
                                    Voltar
                                </Button>
                                <Button
                                    className="w-full sm:flex-1 font-bold"
                                    onClick={(e) => submit(e)}
                                >
                                    <Sparkles size={18} />
                                    Gerar o guia
                                </Button>
                            </>
                        )}
                    </Field>
                </FieldSet>
            );
        }
    }

    return (
        <div
            className={cn(
                "flex flex-col gap-4 sm:gap-6 px-3 sm:px-0",
                className,
            )}
            {...props}
        >
            <Card className="animate-fade-in">
                <CardHeader className="flex flex-col items-center text-base sm:text-xl font-serif justify-center gap-3 sm:gap-5">
                    <CardTitle className="flex flex-col justify-between w-full text-center gap-3 sm:gap-5 animate-fade-in">
                        <div className="text-gray-500 text-xs sm:text-base">
                            <div className="mb-3 sm:mb-5">
                                Etapa {step} de 3
                            </div>
                            <Progress value={(step / 3) * 100} />
                        </div>
                        <div className="font-bold text-xl sm:text-2xl lg:text-3xl">
                            <h1>O que vamos dominar hoje?</h1>
                            <h2 className="font-thin text-xs sm:text-sm text-gray-500 mt-2">
                                Defina um tema e vamos criar um guia
                                personalizado
                            </h2>
                        </div>
                    </CardTitle>
                    {topic !== "" && (
                        <Button
                            variant="ghost"
                            className="text-xs sm:text-sm text-gray-600 hover:text-red-600 hover:bg-red-50"
                            onClick={resetForm}
                            title="Limpar formulário"
                        >
                            <RotateCcw size={16} className="mr-2" />
                            Recomeçar
                        </Button>
                    )}
                </CardHeader>
                <CardContent className="px-3 sm:px-6">
                    <form onSubmit={(e) => e.preventDefault()}>
                        {renderGuideSteps()}
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
