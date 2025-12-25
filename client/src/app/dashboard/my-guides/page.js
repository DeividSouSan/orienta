"use client";
import {
    CheckCircle2,
    BookOpen,
    Clock,
    Plus,
    ChevronLeft,
    ChevronRight,
} from "lucide-react";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useGuideAPI } from "@/hooks/useGuideApi";
import { ConfirmDialog } from "@/components/confirm-dialog";
import AuthGuard from "@/components/auth-guard";

const ITEMS_PER_PAGE = 4;

export default function MyGuidesPage() {
    const [currentPage, setCurrentPage] = useState(1);
    const [completedGuides, setCompletedGuides] = useState([]);
    const [inProgressGuides, setInProgressGuides] = useState([]);
    const [confirmDelete, setConfirmDelete] = useState(null);
    const [deletingGuideId, setDeletingGuideId] = useState(null);
    const { fetchGuides, deleteGuide } = useGuideAPI();

    const totalPages = Math.ceil(completedGuides.length / ITEMS_PER_PAGE);
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const paginatedCompletedGuides = completedGuides.slice(
        startIndex,
        endIndex,
    );

    useEffect(() => {
        const loadGuides = async () => {
            const result = await fetchGuides();
            if (result) {
                setInProgressGuides(result.inProgressGuides);
                setCompletedGuides(result.completedGuides);
            }
        };

        loadGuides();
    }, []);

    const handleDeleteGuide = async (guideId) => {
        setDeletingGuideId(guideId);
        const result = await deleteGuide(guideId);

        if (result.ok) {
            const updatedGuides = await fetchGuides();
            if (updatedGuides) {
                setInProgressGuides(updatedGuides.inProgressGuides);
                setCompletedGuides(updatedGuides.completedGuides);
            }
            setConfirmDelete(null);
        }

        setDeletingGuideId(null);
    };

    const daysInfo = (guide) => {
        const completed =
            guide.daily_studies.filter((day) => day.completed === true)
                .length || 0;
        const total = guide.daily_studies.length || 0;
        const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
        return { completed, total, progress };
    };

    function formatDate(date) {
        return new Date(date).toLocaleDateString("pt-br", {
            day: "2-digit",
            month: "long",
            year: "numeric",
        });
    }

    return (
        <AuthGuard>
            {confirmDelete && (
                <ConfirmDialog
                    title="Excluir Guia"
                    description={`Tem certeza que deseja excluir o guia "${confirmDelete.title}"? Esta ação não pode ser desfeita.`}
                    onConfirm={() => handleDeleteGuide(confirmDelete.guideId)}
                    onCancel={() => setConfirmDelete(null)}
                    isLoading={deletingGuideId === confirmDelete.guideId}
                />
            )}

            <div className="max-w-8xl mx-auto px-6 py-6">
                <h1 className="font-serif text-3xl text-gray-900 mb-2">
                    Meus Guias de Estudo
                </h1>
                <p className="font-sans text-gray-600">
                    Acompanhe seu progresso e continue aprendendo
                </p>
            </div>

            <section className="max-w-5xl mx-auto px-6 py-12">
                <section className="mb-12">
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center">
                            <h2 className="font-serif text-2xl text-gray-900 flex items-center gap-2">
                                <Clock className="w-6 h-6 text-blue-800" />
                                Em Andamento
                            </h2>
                            <span className="ml-3 bg-gray-200 text-gray-700 font-sans text-sm font-bold px-3 py-1 rounded-sm">
                                {inProgressGuides.length}
                            </span>
                        </div>

                        <Link href="/dashboard/generate">
                            <button className="bg-gray-800 text-white font-bold py-3 px-6 rounded-sm hover:bg-gray-900 transition-colors flex items-center gap-2">
                                <Plus className="w-5 h-5" />
                                Novo Guia
                            </button>
                        </Link>
                    </div>

                    {inProgressGuides.length === 0 ? (
                        <div className="bg-white rounded-sm shadow-sm border border-gray-200 p-12 text-center">
                            <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <h3 className="font-serif text-xl text-gray-900 mb-2">
                                Nenhum guia em andamento
                            </h3>
                            <p className="font-sans text-gray-600 mb-6">
                                Comece criando seu primeiro guia de estudos
                            </p>
                            <Link href="/dashboard/generate">
                                <button className="bg-gray-800 text-white font-bold py-3 px-6 rounded-sm hover:bg-gray-900 transition-colors">
                                    Criar Primeiro Guia
                                </button>
                            </Link>
                        </div>
                    ) : (
                        <div className="grid gap-4">
                            {inProgressGuides.map((guide) => (
                                <Link
                                    href={`/dashboard/my-guides/guide?id=${guide.id}`}
                                    key={guide.id}
                                >
                                    <div
                                        key={guide.id}
                                        className="bg-white rounded-sm shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow cursor-pointer"
                                    >
                                        <div className="flex items-start justify-between mb-4">
                                            <div className="flex-1">
                                                <h3 className="font-serif text-xl text-gray-900 mb-1">
                                                    {guide.title}
                                                </h3>
                                                <p className="font-sans text-sm text-gray-600">
                                                    <strong>Prompt: </strong>
                                                    {guide.topic}
                                                </p>
                                            </div>
                                            <span className="bg-blue-50 text-blue-800 font-sans text-xs font-bold px-3 py-1 rounded-sm">
                                                {daysInfo(guide).progress}%
                                            </span>
                                        </div>

                                        {/* Barra de Progresso */}
                                        <div className="mb-4">
                                            <div className="w-full bg-gray-200 rounded-sm h-2">
                                                <div
                                                    className="bg-blue-800 h-2 rounded-sm transition-all"
                                                    style={{
                                                        width: `${daysInfo(guide).progress}%`,
                                                    }}
                                                />
                                            </div>
                                        </div>

                                        <div className="flex items-center justify-between font-sans text-sm">
                                            <span className="text-gray-600">
                                                {daysInfo(guide).completed} de{" "}
                                                {daysInfo(guide).total} dias
                                                concluídos
                                            </span>
                                            <span className="text-gray-500 text-xs">
                                                Criado em:{" "}
                                                {formatDate(guide.created_at)}
                                            </span>
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                </section>

                <section>
                    <div className="flex items-center mb-6">
                        <h2 className="font-serif text-2xl text-gray-900 flex items-center gap-2">
                            <CheckCircle2 className="w-6 h-6 text-green-700" />
                            Concluídos
                        </h2>
                        <span className="ml-3 bg-gray-200 text-gray-700 font-sans text-sm font-bold px-3 py-1 rounded-sm">
                            {completedGuides.length}
                        </span>
                    </div>

                    {completedGuides.length === 0 ? (
                        <div className="bg-white rounded-sm shadow-sm border border-gray-200 p-12 text-center">
                            <CheckCircle2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <h3 className="font-serif text-xl text-gray-900 mb-2">
                                Nenhum guia concluído ainda
                            </h3>
                            <p className="font-sans text-gray-600">
                                Continue estudando para completar seus guias
                            </p>
                        </div>
                    ) : (
                        <>
                            <div className="grid gap-4 mb-6">
                                {paginatedCompletedGuides.map((guide) => (
                                    <Link
                                        href={`/dashboard/my-guides/guide?id=${guide.id}`}
                                        key={guide.id}
                                    >
                                        <div
                                            key={guide.id}
                                            className="bg-white rounded-sm shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer opacity-90 hover:opacity-100"
                                        >
                                            <div className="flex items-start justify-between mb-3">
                                                <div className="flex-1">
                                                    <h3 className="font-serif text-lg text-gray-800 mb-1">
                                                        {guide.title}
                                                    </h3>
                                                    <p className="font-sans text-sm text-gray-500">
                                                        <strong>
                                                            Prompt:{" "}
                                                        </strong>
                                                        {guide.topic}
                                                    </p>
                                                </div>
                                                <CheckCircle2 className="w-5 h-5 text-green-700 flex-shrink-0" />
                                            </div>

                                            <div className="flex items-center justify-between font-sans text-sm">
                                                <span className="text-gray-600">
                                                    Todos os {guide.days} dias
                                                    foram concluídos
                                                </span>
                                                <span className="text-gray-500 text-xs">
                                                    Concluído em{" "}
                                                    {formatDate(
                                                        guide.completed_at,
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    </Link>
                                ))}
                            </div>

                            {totalPages > 1 && (
                                <div className="flex items-center justify-center gap-2">
                                    <button
                                        onClick={() =>
                                            setCurrentPage((prev) =>
                                                Math.max(1, prev - 1),
                                            )
                                        }
                                        disabled={currentPage === 1}
                                        className="p-2 rounded-sm border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                        aria-label="Página anterior"
                                    >
                                        <ChevronLeft className="w-5 h-5 text-gray-700" />
                                    </button>

                                    <div className="flex items-center gap-2">
                                        {Array.from(
                                            { length: totalPages },
                                            (_, i) => i + 1,
                                        ).map((page) => (
                                            <button
                                                key={page}
                                                onClick={() =>
                                                    setCurrentPage(page)
                                                }
                                                className={`w-10 h-10 rounded-sm font-sans font-bold text-sm transition-colors ${currentPage === page
                                                        ? "bg-blue-800 text-white"
                                                        : "bg-white border border-gray-300 text-gray-700 hover:bg-gray-100"
                                                    }`}
                                            >
                                                {page}
                                            </button>
                                        ))}
                                    </div>

                                    <button
                                        onClick={() =>
                                            setCurrentPage((prev) =>
                                                Math.min(totalPages, prev + 1),
                                            )
                                        }
                                        disabled={currentPage === totalPages}
                                        className="p-2 rounded-sm border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                        aria-label="Próxima página"
                                    >
                                        <ChevronRight className="w-5 h-5 text-gray-700" />
                                    </button>
                                </div>
                            )}
                        </>
                    )}
                </section>
            </section>
        </AuthGuard>
    );
}
