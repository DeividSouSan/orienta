"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useStudyGuide } from "@/hooks/useStudyGuide";
import { Suspense, useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ChevronLeft, Check, Lightbulb, AlertCircle } from "lucide-react";
import { ErrorAlert } from "@/components/error-alert";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { useGuideAPI } from "@/hooks/useGuideApi";
import { useMessage } from "@/hooks/useMessage";
import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
} from "@/components/ui/accordion";
import { Checkbox } from "@/components/ui/checkbox";
import { Spinner } from "@/components/ui/spinner";
import AuthGuard from "@/components/auth-guard";
import { cn } from "@/lib/utils";

function GuideDetailsView() {
    const searchParams = useSearchParams();
    const guideId = searchParams.get("id");
    const router = useRouter();

    const { guide, isLoading, updateDayCompletion, isSavingBatch } =
        useStudyGuide(guideId);

    const { deleteGuide, isLoading: isDeleting } = useGuideAPI();
    const { successMessage, errorMessage } = useMessage();

    const [showSavingFeedback, setShowSavingFeedback] = useState(false);

    const [showConfirmationDelete, setShowConfirmationDelete] = useState(false);

    const handleToggleDay = (index, checked) => {
        setShowSavingFeedback(true);
        updateDayCompletion(index, checked);
    };

    useEffect(() => {
        if (!isSavingBatch) {
            setShowSavingFeedback(false);
        }
    }, [isSavingBatch]);

    const completedDays =
        guide?.daily_study?.filter((d) => d.completed)?.length || 0;
    const totalDays = guide?.daily_study?.length || 0;
    const progressPercentage =
        totalDays > 0 ? Math.round((completedDays / totalDays) * 100) : 0;

    const handleConfirmDelete = async () => {
        if (!guideId) return;

        const result = await deleteGuide(guideId);
        if (result.success) {
            successMessage(result.message);
            return router.push("/dashboard/my-guides")
        } else {
            errorMessage(result.message)
        }
    };

    return (
        <main className={cn("flex flex-col w-full items-center min-h-screen bg-gray-50")}>
            <div className="flex flex-col items-center w-full max-w-3xl px-3 sm:px-4 py-6 sm:py-8">
                {isLoading ? (
                    <Spinner />
                ) : !guide ? (
                    <section className="flex flex-col items-center w-full gap-4">
                        <ErrorAlert
                            message="Não conseguimos carregar este guia. Verifique sua conexão e tente novamente."
                            onClose={() => window.location.reload()}
                        />
                        <Link
                            href="/dashboard/my-guides"
                            className="w-full sm:w-auto"
                        >
                            <Button className="w-full sm:w-auto">
                                <ChevronLeft size={18} />
                                Voltar para Meus Guias
                            </Button>
                        </Link>
                    </section>
                ) : (
                    <article className="flex flex-col gap-6 w-full">
                        <section className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 w-full">
                            <div className="flex-1">
                                <h1 className="font-bold font-serif text-2xl sm:text-3xl lg:text-4xl break-words text-gray-900">
                                    {guide.inputs?.title}
                                </h1>
                                <p className="text-gray-600 text-sm sm:text-base mt-2">
                                    {guide.inputs?.topic}
                                </p>
                            </div>
                            <Link
                                href="/dashboard/my-guides"
                                className="w-full sm:w-auto"
                            >
                                <Button
                                    variant="outline"
                                    className="w-full sm:w-auto"
                                >
                                    <ChevronLeft size={18} />
                                    Voltar
                                </Button>
                            </Link>
                        </section>

                        <section className="bg-white rounded-lg p-4 border border-gray-200">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-medium text-gray-700">
                                    Progresso: {completedDays}/{totalDays} dias
                                </span>
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-bold text-blue-600">
                                        {progressPercentage}%
                                    </span>
                                    {(showSavingFeedback || isSavingBatch) && (
                                        <div className="flex items-center gap-1 text-xs text-amber-600 animate-pulse">
                                            <div className="w-2 h-2 bg-amber-600 rounded-full" />
                                            Salvando...
                                        </div>
                                    )}
                                    {!showSavingFeedback &&
                                        !isSavingBatch &&
                                        guide && (
                                            <div className="flex items-center gap-1 text-xs text-green-600">
                                                <Check size={14} />
                                                Salvo
                                            </div>
                                        )}
                                </div>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                    style={{ width: `${progressPercentage}%` }}
                                />
                            </div>
                        </section>

                        <Accordion
                            type="single"
                            defaultValue="dia1"
                            collapsible
                            className="flex flex-col w-full space-y-3"
                        >
                            {Array.isArray(guide.daily_study) &&
                                guide.daily_study.length ? (
                                guide.daily_study.map((study, index) => {
                                    return (
                                        <AccordionItem
                                            key={study.day}
                                            value={"dia" + study.day}
                                            className={`border last:border border-b-5 last:border-b-5 px-3 md:px-4 rounded-md transition-all duration-200 ${study.completed
                                                ? "bg-green-50 border-black border-2 border-b-5 last:border-2 last:border-b-5 shadow-sm"
                                                : "bg-white border-gray-200"
                                                }`}
                                        >
                                            <AccordionTrigger className="hover:no-underline py-4">
                                                <div className="flex items-start sm:items-center gap-3 text-left w-full">
                                                    <div className="relative">
                                                        <Checkbox
                                                            disabled={isLoading}
                                                            onClick={(e) =>
                                                                e.stopPropagation()
                                                            }
                                                            onCheckedChange={(
                                                                checked,
                                                            ) =>
                                                                handleToggleDay(
                                                                    index,
                                                                    checked,
                                                                )
                                                            }
                                                            checked={
                                                                study.completed
                                                            }
                                                            className="h-5 w-5 mt-1 sm:mt-0 shrink-0 rounded border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                                                            aria-label={`Marcar dia ${study.day} como ${study.completed ? "incompleto" : "completo"}`}
                                                        />
                                                        {isLoading && (
                                                            <div className="absolute inset-0 flex items-center justify-center">
                                                                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse" />
                                                            </div>
                                                        )}
                                                    </div>
                                                    <span
                                                        className={`text-sm sm:text-base flex-1 ${study.completed
                                                            ? "font-bold text-gray-900 line-through opacity-75"
                                                            : "font-medium text-gray-700"
                                                            }`}
                                                    >
                                                        Dia {study.day} -{" "}
                                                        {study.title}
                                                    </span>
                                                    {isLoading && (
                                                        <Spinner size="sm" />
                                                    )}
                                                </div>
                                            </AccordionTrigger>
                                            <AccordionContent className="space-y-4 text-gray-700 text-left sm:text-justify text-sm sm:text-base pb-4 pt-4">
                                                <div>
                                                    <h3 className="font-bold text-gray-900 mb-2">
                                                        Meta:
                                                    </h3>
                                                    <p>{study.goal}</p>
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-gray-900 mb-3">
                                                        O que pesquisar:
                                                    </h3>
                                                    <ul className="space-y-2 pl-4">
                                                        {study.theoretical_research.map(
                                                            (
                                                                searchItem,
                                                                index,
                                                            ) => {
                                                                return (
                                                                    <li
                                                                        key={
                                                                            index
                                                                        }
                                                                        className="flex gap-3 items-start"
                                                                    >
                                                                        <Lightbulb
                                                                            size={
                                                                                18
                                                                            }
                                                                            className="text-yellow-500 shrink-0 mt-0.5"
                                                                            aria-hidden="true"
                                                                        />
                                                                        <span>
                                                                            {
                                                                                searchItem
                                                                            }
                                                                        </span>
                                                                    </li>
                                                                );
                                                            },
                                                        )}
                                                    </ul>
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-gray-900 mb-2">
                                                        Mão na massa:
                                                    </h3>
                                                    <p>
                                                        {
                                                            study.practical_activity
                                                        }
                                                    </p>
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-gray-900 mb-2">
                                                        Verificação de
                                                        Aprendizado:
                                                    </h3>
                                                    <p>
                                                        {
                                                            study.learning_verification
                                                        }
                                                    </p>
                                                </div>
                                            </AccordionContent>
                                        </AccordionItem>
                                    );
                                })
                            ) : (
                                <section className="flex flex-col items-center gap-3 py-12">
                                    <AlertCircle
                                        size={32}
                                        className="text-yellow-500"
                                    />
                                    <p className="text-center text-gray-600 text-sm sm:text-base">
                                        Não foi possível recuperar os dias de
                                        estudo desse guia.
                                        <br />
                                        Tente recarregar a página ou entre em
                                        contato com o suporte se o problema
                                        persistir.
                                    </p>
                                </section>
                            )}
                        </Accordion>
                        <section>
                            <Button
                                variant="destructive"
                                onClick={() => setShowConfirmationDelete(true)}
                            >
                                Excluir Guia
                            </Button>

                            {showConfirmationDelete && (
                                <ConfirmDialog
                                    title="Excluir este guia?"
                                    description="Esta ação não pode ser desfeita. O guia será removido da sua lista."
                                    onCancel={() => setShowConfirmationDelete(false)}
                                    onConfirm={handleConfirmDelete}
                                    isLoading={isDeleting}
                                />
                            )}
                        </section>
                    </article>
                )}
            </div>
        </main>
    );
}

export default function GuideDetailsPage() {
    return (
        <AuthGuard>
            <Suspense fallback={<Spinner />}>
                <GuideDetailsView />
            </Suspense>
        </AuthGuard>
    );
}
