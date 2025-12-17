"use client";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card";
import { LibraryBig, CircleDashed, CircleCheck, BookOpen, PlusCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { Spinner } from "@/components/ui/spinner";
import Link from "next/link";
import { useGuideApi } from "@/hooks/useGuideApi";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { ErrorAlert } from "@/components/error-alert";
import { EmptyState } from "@/components/empty-state";
import { CardSkeleton } from "@/components/card-skeleton";

export default function MyGuidesPage() {
    const [completedGuides, setCompletedGuides] = useState([]); // guias já feitos
    const [ongoingGuides, setOngoingGuides] = useState([]); // guias em andamento
    const [confirmDelete, setConfirmDelete] = useState(null); // { guideId, title }
    const [deletingGuideId, setDeletingGuideId] = useState(null);
    const { loading, error, setError, fetchGuides, deleteGuide } =
        useGuideApi();

    useEffect(() => {
        const loadGuides = async () => {
            const result = await fetchGuides();
            if (result) {
                setOngoingGuides(result.ongoingGuidesList);
                setCompletedGuides(result.completedGuidesList);
            }
        };

        loadGuides();
    }, []);

    function formatDate(date) {
        return new Date(date).toLocaleDateString("pt-br", {
            day: "2-digit",
            month: "long",
            year: "numeric",
        });
    }

    const handleDeleteGuide = async (guideId) => {
        setDeletingGuideId(guideId);
        const result = await deleteGuide(guideId);

        if (result.success) {
            // Recarrega os guias
            const updatedGuides = await fetchGuides();
            if (updatedGuides) {
                setOngoingGuides(updatedGuides.ongoingGuidesList);
                setCompletedGuides(updatedGuides.completedGuidesList);
            }
            setConfirmDelete(null);
        }

        setDeletingGuideId(null);
    };

    return (
        <>
            {error && (
                <div className="p-4">
                    <ErrorAlert
                        message={error}
                        onClose={() => setError(null)}
                    />
                </div>
            )}

            {confirmDelete && (
                <ConfirmDialog
                    title="Excluir Guia"
                    description={`Tem certeza que deseja excluir o guia "${confirmDelete.title}"? Esta ação não pode ser desfeita.`}
                    onConfirm={() => handleDeleteGuide(confirmDelete.guideId)}
                    onCancel={() => setConfirmDelete(null)}
                    isLoading={deletingGuideId === confirmDelete.guideId}
                />
            )}

            <div className="flex flex-col w-full">
                <div className="flex flex-col items-center px-3 sm:px-4">
                    <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 my-6 sm:my-10 justify-center">
                        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-semibold text-center">
                            Meus Guias de Estudo
                        </h1>
                        <LibraryBig
                            size={24}
                            className="sm:w-8 sm:h-8 lg:w-8 lg:h-8"
                        />
                    </div>
                    <div className="flex w-full flex-col max-w-3xl px-0 sm:px-3">
                        <span className="flex gap-2 items-center mb-4 sm:mb-5">
                            <CircleDashed size={20} className="sm:w-6 sm:h-6" />
                            <h2 className="text-lg sm:text-xl font-serif font-semibold">
                                Estudando
                            </h2>
                        </span>
                        <div className="flex flex-col items-center w-full gap-3 sm:gap-4">
                            {loading ? (
                                <>
                                    <CardSkeleton />
                                    <CardSkeleton />
                                </>
                            ) : ongoingGuides.length ? (
                                ongoingGuides.map((guide) => {
                                    const daysCompleted =
                                        guide.daily_studies.filter(
                                            (day) => day.completed === true,
                                        ).length;
                                    const progress = Math.floor(
                                        (daysCompleted / guide.days) * 100,
                                    );

                                    return (
                                        <Card
                                            key={guide.id}
                                            className={`w-full max-w-2xl transition-all duration-300 ${deletingGuideId === guide.id
                                                    ? "opacity-50 scale-95"
                                                    : ""
                                                }`}
                                        >
                                            <CardHeader className="pb-3 sm:pb-4">
                                                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                                                    <div className="flex-1">
                                                        <h2 className="text-xl sm:text-2xl font-semibold text-gray-900 font-serif">
                                                            {guide.title}
                                                        </h2>
                                                        <p className="mt-1 text-sm sm:text-base text-gray-600">
                                                            {guide.topic}
                                                        </p>
                                                    </div>
                                                    <span className="text-xs sm:text-sm text-gray-600 whitespace-nowrap">
                                                        {guide.days} dias
                                                    </span>
                                                </div>
                                            </CardHeader>

                                            <CardContent className="pb-3 sm:pb-4">
                                                <div className="space-y-3 sm:space-y-4">
                                                    <p className="text-xs sm:text-sm text-gray-600">
                                                        Criado em:{" "}
                                                        {formatDate(
                                                            guide.created_at,
                                                        )}
                                                    </p>
                                                    <div className="space-y-2">
                                                        <p className="text-xs sm:text-sm text-gray-600">
                                                            Progresso
                                                        </p>
                                                        <Progress
                                                            value={progress}
                                                            className="h-2"
                                                        />
                                                        <p className="text-right text-xs sm:text-sm text-gray-600">
                                                            {progress}%
                                                        </p>
                                                    </div>
                                                </div>
                                            </CardContent>

                                            <CardFooter className="flex flex-col sm:flex-row gap-2 sm:gap-0 sm:justify-between">
                                                <Link
                                                    href={`/dashboard/my-guides/guide?id=${guide.id}`}
                                                    className="w-full sm:w-auto"
                                                >
                                                    <Button
                                                        variant="default"
                                                        className="w-full sm:w-auto"
                                                    >
                                                        Continuar Estudo
                                                    </Button>
                                                </Link>
                                                <Button
                                                    variant="ghost"
                                                    className="text-gray-600 w-full sm:w-auto"
                                                    onClick={() => {
                                                        setConfirmDelete({
                                                            guideId: guide.id,
                                                            title: guide.title,
                                                        });
                                                    }}
                                                >
                                                    Excluir
                                                </Button>
                                            </CardFooter>
                                        </Card>
                                    );
                                })
                            ) : (
                                <EmptyState
                                    icon={PlusCircle}
                                    title="Nenhum guia em andamento"
                                    description="Comece um novo guia de estudo para acompanhar seu progresso e aprender de forma estruturada."
                                    ctaText="Criar Novo Guia"
                                    ctaHref="/dashboard/generate"
                                />
                            )}
                        </div>
                    </div>
                    <div className="flex w-full flex-col max-w-3xl px-0 sm:px-3 mt-6 sm:mt-8">
                        <span className="flex gap-2 items-center mb-4 sm:mb-5">
                            <CircleCheck size={20} className="sm:w-6 sm:h-6" />
                            <h2 className="text-lg sm:text-xl font-serif font-semibold">
                                Completos
                            </h2>
                        </span>
                        <div className="flex flex-col items-center w-full gap-2 sm:gap-3">
                            {loading ? (
                                <>
                                    <CardSkeleton />
                                    <CardSkeleton />
                                </>
                            ) : completedGuides.length ? (
                                completedGuides.map((guide) => {
                                    return (
                                        <Card
                                            key={guide.id}
                                            className={`w-full max-w-2xl transition-all duration-300 ${deletingGuideId === guide.id
                                                    ? "opacity-50 scale-95"
                                                    : ""
                                                }`}
                                        >
                                            <CardHeader className="pb-3 sm:pb-4">
                                                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4">
                                                    <div className="flex-1">
                                                        <h2 className="text-xl sm:text-2xl font-semibold text-gray-900 font-serif">
                                                            {guide.title}
                                                        </h2>
                                                        <span className="text-xs sm:text-sm text-gray-600 block mt-1">
                                                            Concluído em:{" "}
                                                            {formatDate(
                                                                guide.completed_at,
                                                            )}{" "}
                                                            ({guide.days} dias)
                                                        </span>
                                                    </div>
                                                    <Link
                                                        href={`/dashboard/my-guides/guide?id=${guide.id}`}
                                                        className="w-full sm:w-auto"
                                                    >
                                                        <Button className="w-full sm:w-auto">
                                                            Revisar
                                                        </Button>
                                                    </Link>
                                                </div>
                                            </CardHeader>
                                        </Card>
                                    );
                                })
                            ) : (
                                <EmptyState
                                    icon={BookOpen}
                                    title="Nenhum guia completado"
                                    description="Continue estudando seus guias em andamento para alcançar seus objetivos!"
                                />
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
