import {
  CheckCircle2,
  BookOpen,
  Clock,
  Plus,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { useGuideAPI } from "@/hooks/useGuideApi";
import AuthGuard from "@/components/auth-guard";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { z } from "zod";
import { GuideSchema } from "@/schemas/guideSchema";

type Guide = z.infer<typeof GuideSchema>;

const ITEMS_PER_PAGE = 4;

export default function MyGuidesPage() {
  const { fetchGuides } = useGuideAPI();
  const [inProgressGuides, setInProgressGuides] = useState<Guide[]>([]);
  const [completedGuides, setCompletedGuides] = useState<Guide[]>([]);

  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(completedGuides.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedCompletedGuides = completedGuides.slice(startIndex, endIndex);

  useEffect(() => {
    const loadGuides = async () => {
      const result = await fetchGuides();
      if (result.success && result.data) {
        setInProgressGuides(result.data.inProgressGuides);
        setCompletedGuides(result.data.completedGuides);
      }
    };

    loadGuides();
  }, []);

  const getProgress = (guide: Guide) => {
    const study_days = guide.daily_studies || [];

    const completed =
      study_days.filter((day: any) => day.completed === true).length || 0;

    const total = study_days.length || 0;

    const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

    return { completed, total, progress };
  };

  function formatDate(date: string | undefined) {
    if (!date) return "";
    return new Date(date).toLocaleDateString("pt-br", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  }

  return (
    <AuthGuard>
      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Page Header */}
        <div className="mb-10 animate-fade-in">
          <h1 className="font-serif text-3xl md:text-4xl font-bold">
            Meus Guias de Estudo
          </h1>
          <p className="text-muted-foreground mt-2">
            Acompanhe seu progresso e continue aprendendo
          </p>
        </div>

        {/* Em Andamento */}
        <section className="mb-12 animate-fade-in animation-delay-200">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <h2 className="font-serif text-xl flex items-center gap-2">
                <Clock className="w-5 h-5 text-muted-foreground" />
                Em Andamento
              </h2>
              <span className="bg-muted text-muted-foreground text-xs font-medium px-2.5 py-0.5 rounded-md">
                {inProgressGuides.length}
              </span>
            </div>

            <Link to="/dashboard/generate">
              <Button size="sm">
                <Plus className="w-4 h-4" />
                Novo Guia
              </Button>
            </Link>
          </div>

          {inProgressGuides.length === 0 ? (
            <Card className="text-center py-8">
              <CardContent className="flex flex-col items-center gap-4">
                <BookOpen className="w-12 h-12 text-muted-foreground/40" />
                <div>
                  <h3 className="font-serif text-lg font-semibold mb-1">
                    Nenhum guia em andamento
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Comece criando seu primeiro guia de estudos
                  </p>
                  <Link to="/dashboard/generate">
                    <Button>Criar Primeiro Guia</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {inProgressGuides.map((guide) => (
                <Link to={`/dashboard/my-guides/${guide.id}`} key={guide.id}>
                  <Card className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardContent className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="font-serif text-lg font-semibold mb-1">
                            {guide.title}
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            <strong>Prompt: </strong>
                            {guide.topic}
                          </p>
                        </div>
                        <span className="bg-accent text-accent-foreground text-xs font-medium px-2.5 py-1 rounded-md">
                          {getProgress(guide).progress}%
                        </span>
                      </div>

                      <div className="mb-4">
                        <div className="w-full bg-muted rounded-md h-2">
                          <div
                            className="bg-primary h-2 rounded-md transition-all"
                            style={{
                              width: `${getProgress(guide).progress}%`,
                            }}
                          />
                        </div>
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">
                          {getProgress(guide).completed} de{" "}
                          {getProgress(guide).total} dias concluídos
                        </span>
                        <span className="text-muted-foreground text-xs">
                          Criado em: {formatDate(guide.created_at)}
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </section>

        {/* Concluídos */}
        <section className="animate-fade-in animation-delay-400">
          <div className="flex items-center gap-3 mb-6">
            <h2 className="font-serif text-xl flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-muted-foreground" />
              Concluídos
            </h2>
            <span className="bg-muted text-muted-foreground text-xs font-medium px-2.5 py-0.5 rounded-md">
              {completedGuides.length}
            </span>
          </div>

          {completedGuides.length === 0 ? (
            <Card className="text-center py-8">
              <CardContent className="flex flex-col items-center gap-4">
                <CheckCircle2 className="w-12 h-12 text-muted-foreground/40" />
                <div>
                  <h3 className="font-serif text-lg font-semibold mb-1">
                    Nenhum guia concluído ainda
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Continue estudando para completar seus guias
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="grid gap-4 mb-6">
                {paginatedCompletedGuides.map((guide) => (
                  <Link to={`/dashboard/my-guides/${guide.id}`} key={guide.id}>
                    <Card className="hover:shadow-md transition-shadow cursor-pointer opacity-90 hover:opacity-100">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h3 className="font-serif text-lg font-semibold mb-1">
                              {guide.title}
                            </h3>
                            <p className="text-sm text-muted-foreground">
                              <strong>Prompt: </strong>
                              {guide.topic}
                            </p>
                          </div>
                          <CheckCircle2 className="w-5 h-5 text-muted-foreground shrink-0" />
                        </div>

                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">
                            Todos os {guide.days} dias foram concluídos
                          </span>
                          <span className="text-muted-foreground text-xs">
                            Concluído em {formatDate(guide.completed_at)}
                          </span>
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>

              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2">
                  <Button
                    variant="outline"
                    size="icon-sm"
                    onClick={() =>
                      setCurrentPage((prev) => Math.max(1, prev - 1))
                    }
                    disabled={currentPage === 1}
                    aria-label="Página anterior"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </Button>

                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                      (page) => (
                        <Button
                          key={page}
                          variant={currentPage === page ? "default" : "outline"}
                          size="icon-sm"
                          onClick={() => setCurrentPage(page)}
                        >
                          {page}
                        </Button>
                      ),
                    )}
                  </div>

                  <Button
                    variant="outline"
                    size="icon-sm"
                    onClick={() =>
                      setCurrentPage((prev) => Math.min(totalPages, prev + 1))
                    }
                    disabled={currentPage === totalPages}
                    aria-label="Próxima página"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </AuthGuard>
  );
}
