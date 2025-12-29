"use client";
import AuthGuard from "@/components/auth-guard";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { ArrowLeft, RotateCcw, Sparkles } from "lucide-react";
import { useMessage } from "@/hooks/useMessage";

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

export default function GeneratePage() {
    const router = useRouter();

    const { errorMessage } = useMessage();
    const { logout } = useAuth();

    const [isGenerating, setIsGenerating] = useState(false);

    const [currentStep, setCurrentStep] = useState(1);
    const progressPercentage = (currentStep / 3) * 100;

    const [formData, setFormData] = useState({
        title: "",
        topic: "",
        knowledgeLevel: null,
        focusTime: 30,
        days: 7,
    });

    const handleNext = async () => {
        console.log("O passo atual é: ", currentStep);
        if (currentStep === 1) {
            if (!stepOneValidation()) return;

            setIsGenerating(true);
            try {
                const response = await callValidateTopicAPI();
                const body = await response.json();

                if (!response.ok) {
                    if (response.status === 401 && body.code === 401) {
                        errorMessage(body.message);
                        logout();
                        return router.push("/login");
                    }
                    errorMessage(body.message);
                    return;
                }
            } catch (error) {
                errorMessage(
                    "Não conseguimos validar seu tópico. Tente novamente.",
                );
                return;
            } finally {
                setIsGenerating(false);
            }

            async function callValidateTopicAPI() {
                const response = await fetch("/api/v1/validate/topic", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify({
                        topic: formData.topic,
                    }),
                });

                return response;
            }
        } else if (currentStep === 2) {
            if (formData.knowledgeLevel === null) return;
        } else if (currentStep === 3) {
            const parsedFocusTime = parseInt(formData.focusTime) || 0;
            if (
                !parsedFocusTime ||
                parsedFocusTime < VALIDATION_LIMITS.FOCUS_TIME_MIN
            ) {
                errorMessage(
                    `Você precisa dedicar no mínimo ${VALIDATION_LIMITS.FOCUS_TIME_MIN} minutos por dia.`,
                );
                return;
            }

            if (parsedFocusTime > VALIDATION_LIMITS.FOCUS_TIME_MAX) {
                errorMessage(
                    `O máximo de tempo é ${VALIDATION_LIMITS.FOCUS_TIME_MAX} minutos por dia.`,
                );
                return;
            }

            const parsedDays = parseInt(formData.days) || 0;
            if (!parsedDays || parsedDays < VALIDATION_LIMITS.DAYS_MIN) {
                errorMessage(
                    `Seu guia precisa ter no mínimo ${VALIDATION_LIMITS.DAYS_MIN} dias.`,
                );
                return;
            }

            if (parsedDays > VALIDATION_LIMITS.DAYS_MAX) {
                errorMessage(
                    `O máximo de dias é ${VALIDATION_LIMITS.DAYS_MAX}.`,
                );
                return;
            }
        }

        console.log("Agora aumentando o currentStep");
        if (currentStep < 3) {
            setCurrentStep((prev) => prev + 1);
            console.log("O currentStep é agora: ", currentStep);
        } else {
            handleGenerate();
        }
    };

    const handleBack = () => {
        if (currentStep > 1) {
            setCurrentStep((prev) => prev - 1);
        } else {
            router.push("/");
        }
    };

    const handleRestart = () => {
        setFormData({
            title: "",
            topic: "",
            knowledgeLevel: null,
            dailyMinutes: 30,
            totalDays: 7,
        });
        setCurrentStep(1);
    };

    const stepOneValidation = () => {
        const trimmedTitle = formData.title.trim();
        const trimmedTopic = formData.topic.trim();

        if (!trimmedTitle) {
            errorMessage("Qual é o título do seu estudo?");
            return false;
        }

        if (trimmedTitle.length < VALIDATION_LIMITS.TITLE_MIN) {
            errorMessage(
                `O título precisa ter pelo menos ${VALIDATION_LIMITS.TITLE_MIN} caracteres.`,
            );
            return false;
        }

        if (!trimmedTopic) {
            errorMessage("Conte-nos sobre o que você quer estudar.");
            return false;
        }

        if (trimmedTopic.length < VALIDATION_LIMITS.TOPIC_MIN) {
            errorMessage("Descreva melhor seu tópico (mínimo 10 caracteres).");
            return false;
        }

        return true;
    };

    async function handleGenerate() {
        setIsGenerating(true);

        const guideInputs = {
            title: formData.title.trim(),
            topic: formData.topic.trim(),
            knowledge: formData.knowledgeLevel,
            focus_time: parseInt(formData.focusTime),
            days: parseInt(formData.days),
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

            const body = await response.json();

            if (response.ok) return router.push("/dashboard/my-guides");
            else {
                if (response.status === 401 && body.status === 401) {
                    errorMessage(body.message);
                    logout();
                    return router.push("/login");
                }
                errorMessage(body.message);
            }
        } catch (error) {
            errorMessage(
                "Erro ao conectar com o servidor. Verifique sua conexão.",
            );
        } finally {
            setIsGenerating(false);
        }
    }

    return (
        <AuthGuard>
            <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6 py-12">
                <div className="w-full max-w-2xl">
                    <div className="bg-white rounded-sm shadow-md border border-gray-200 p-8 md:p-12">
                        <div className="mb-8">
                            <p className="font-sans text-sm text-gray-600 text-center mb-3">
                                Etapa {currentStep} de 3
                            </p>
                            <div className="w-full bg-gray-200 rounded-sm h-2 mb-6">
                                <div
                                    className="bg-gray-900 h-2 rounded-sm transition-all duration-500 ease-out"
                                    style={{ width: `${progressPercentage}%` }}
                                />
                            </div>

                            <h1 className="font-serif text-3xl md:text-4xl text-gray-900 text-center mb-3 text-balance">
                                O que vamos dominar hoje?
                            </h1>
                            <p className="font-sans text-gray-600 text-center text-pretty">
                                {currentStep === 1 &&
                                    "Defina um tema e vamos criar um guia personalizado"}
                                {currentStep === 2 &&
                                    "Ajuste o guia ao seu nível atual de conhecimento"}
                                {currentStep === 3 &&
                                    "Configure a duração e ritmo dos seus estudos"}
                            </p>

                            <button
                                onClick={handleRestart}
                                className="flex items-center gap-2 mx-auto mt-6 font-sans text-sm text-gray-600 hover:text-gray-900 transition-colors"
                            >
                                <RotateCcw className="w-4 h-4" />
                                Recomeçar
                            </button>
                        </div>

                        <div className="mb-8">
                            {currentStep === 1 && (
                                <div className="space-y-6 animate-fade-in">
                                    <div>
                                        <label
                                            htmlFor="title"
                                            className="block font-sans text-sm font-bold text-gray-900 mb-2"
                                        >
                                            Dê um nome para esse seu novo estudo
                                        </label>
                                        <input
                                            type="text"
                                            id="title"
                                            value={formData.title}
                                            onChange={(e) =>
                                                setFormData({
                                                    ...formData,
                                                    title: e.target.value,
                                                })
                                            }
                                            placeholder="Ex: Observabilidade (Intro)"
                                            maxLength={40}
                                            className="w-full bg-gray-50 border border-gray-300 rounded-sm px-4 py-3 font-sans text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-transparent transition-all"
                                        />
                                        <p className="font-sans text-xs text-gray-500 mt-1 text-right">
                                            {formData.title.length}/40
                                        </p>
                                    </div>

                                    <div>
                                        <label
                                            htmlFor="topic"
                                            className="block font-sans text-sm font-bold text-gray-900 mb-2"
                                        >
                                            O que você gostaria de estudar?
                                        </label>
                                        <textarea
                                            id="topic"
                                            value={formData.topic}
                                            onChange={(e) =>
                                                setFormData({
                                                    ...formData,
                                                    topic: e.target.value,
                                                })
                                            }
                                            placeholder="Descreva em detalhes o que você quer aprender..."
                                            rows={4}
                                            maxLength={150}
                                            className="w-full bg-gray-50 border border-gray-300 rounded-sm px-4 py-3 font-sans text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-transparent transition-all resize-none"
                                        />
                                        <p className="font-sans text-xs text-gray-500 mt-1 text-right">
                                            {formData.topic.length}/150
                                        </p>
                                    </div>
                                </div>
                            )}

                            {currentStep === 2 && (
                                <div className="space-y-4 animate-fade-in">
                                    <label className="block font-sans text-sm font-bold text-gray-900 mb-4">
                                        Qual seu nível de conhecimento em
                                        relação a:
                                    </label>
                                    <div className="bg-gray-50 border border-gray-200 rounded-sm p-4 mb-6">
                                        <p className="font-sans text-gray-700 italic text-sm leading-relaxed">
                                            {formData.topic}
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        {[
                                            {
                                                value: "zero",
                                                label: "Nenhum conhecimento",
                                                topic: "Estou começando do zero",
                                            },
                                            {
                                                value: "iniciante",
                                                label: "Iniciante",
                                                topic: "Tenho conhecimentos básicos",
                                            },
                                            {
                                                value: "intermediario",
                                                label: "Intermediário/Avançado",
                                                topic: "Quero me aprofundar",
                                            },
                                        ].map((option) => (
                                            <label
                                                key={option.value}
                                                className={`flex items-start gap-4 p-4 border-2 rounded-sm cursor-pointer transition-all ${
                                                    formData.knowledgeLevel ===
                                                    option.value
                                                        ? "border-gray-900 bg-gray-50"
                                                        : "border-gray-200 bg-white hover:border-gray-300"
                                                }`}
                                            >
                                                <input
                                                    type="radio"
                                                    name="knowledgeLevel"
                                                    value={option.value}
                                                    checked={
                                                        formData.knowledgeLevel ===
                                                        option.value
                                                    }
                                                    onChange={(e) =>
                                                        setFormData({
                                                            ...formData,
                                                            knowledgeLevel:
                                                                e.target.value,
                                                        })
                                                    }
                                                    className="mt-1 w-5 h-5 text-gray-900 cursor-pointer"
                                                />
                                                <div className="flex-1">
                                                    <p className="font-sans font-bold text-gray-900">
                                                        {option.label}
                                                    </p>
                                                    <p className="font-sans text-sm text-gray-600">
                                                        {option.topic}
                                                    </p>
                                                </div>
                                            </label>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {currentStep === 3 && (
                                <div className="space-y-6 animate-fade-in">
                                    <div className="mb-8">
                                        <h3 className="font-serif text-xl text-gray-900 mb-6">
                                            Informações temporais:
                                        </h3>

                                        <div className="space-y-6">
                                            <div>
                                                <label
                                                    htmlFor="dailyMinutes"
                                                    className="block font-sans text-sm font-bold text-gray-900 mb-2"
                                                >
                                                    Quanto tempo você pode se
                                                    dedicar por dia (em
                                                    minutos)?
                                                </label>
                                                <input
                                                    type="number"
                                                    id="dailyMinutes"
                                                    value={formData.focusTime}
                                                    onChange={(e) =>
                                                        setFormData({
                                                            ...formData,
                                                            focusTime: parseInt(
                                                                e.target.value,
                                                            ),
                                                        })
                                                    }
                                                    min={30}
                                                    max={480}
                                                    className="w-full bg-gray-50 border border-gray-300 rounded-sm px-4 py-3 font-sans text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-transparent transition-all"
                                                />
                                                <p className="font-sans text-xs text-gray-500 mt-1">
                                                    30 a 480 minutos
                                                </p>
                                            </div>

                                            <div>
                                                <label
                                                    htmlFor="totalDays"
                                                    className="block font-sans text-sm font-bold text-gray-900 mb-2"
                                                >
                                                    Qual será a duração total do
                                                    estudo (em dias)?
                                                </label>
                                                <input
                                                    type="number"
                                                    id="totalDays"
                                                    value={formData.days}
                                                    onChange={(e) =>
                                                        setFormData({
                                                            ...formData,
                                                            days: parseInt(
                                                                e.target.value,
                                                            ),
                                                        })
                                                    }
                                                    min={3}
                                                    max={30}
                                                    className="w-full bg-gray-50 border border-gray-300 rounded-sm px-4 py-3 font-sans text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-transparent transition-all"
                                                />
                                                <p className="font-sans text-xs text-gray-500 mt-1">
                                                    3 a 30 dias
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={handleBack}
                                className="flex-1 bg-gray-200 text-gray-900 font-bold py-3 px-6 rounded-sm hover:bg-gray-300 transition-colors flex items-center justify-center gap-2"
                            >
                                <ArrowLeft className="w-5 h-5" />
                                Voltar
                            </button>

                            <button
                                onClick={handleNext}
                                disabled={isGenerating}
                                className="flex-1 bg-gray-900 text-white font-bold py-3 px-6 rounded-sm hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:not-allowed flex items-center justify-center gap-2"
                            >
                                {isGenerating ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                        Gerando...
                                    </>
                                ) : currentStep === 3 ? (
                                    <>
                                        <Sparkles className="w-5 h-5" />
                                        Gerar o guia
                                    </>
                                ) : (
                                    "Avançar"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </AuthGuard>
    );
}
