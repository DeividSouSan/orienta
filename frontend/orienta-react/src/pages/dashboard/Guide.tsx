import { useParams, useNavigate, Link } from "react-router";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronLeft, Check, Lightbulb, AlertCircle } from "lucide-react";
import { ErrorAlert } from "@/components/error-alert";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { useCurrentGuide } from "@/hooks/useCurrentGuide";
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
import { Card, CardContent } from "@/components/ui/card";

export default function GuideDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { successMessage, errorMessage } = useMessage();

  const {
    guide,
    fetchGuideById,
    updateDayStatus,
    deleteGuide,
    isSaving,
    isLoading,
    isDeleting,
  } = useCurrentGuide(id);

  const [showSavingFeedback, setShowSavingFeedback] = useState(false);
  const [showConfirmationDelete, setShowConfirmationDelete] = useState(false);

  const handleDayStatusChange = (index: number, checked: boolean) => {
    setShowSavingFeedback(true);
    updateDayStatus(index, checked);
  };

  useEffect(() => {
    fetchGuideById();
  }, []);

  useEffect(() => {
    if (!isSaving) {
      setShowSavingFeedback(false);
    }
  }, [isSaving]);

  const completedDays =
    guide?.daily_study?.filter((d: any) => d.completed)?.length || 0;
  const totalDays = guide?.daily_study?.length || 0;
  const progressPercentage =
    totalDays > 0 ? Math.round((completedDays / totalDays) * 100) : 0;

  const handleConfirmDelete = async () => {
    if (!id) return;

    const result = await deleteGuide();
    if (result.success) {
      successMessage(result.message);
      navigate("/dashboard/my-guides");
    } else {
      errorMessage(result.message);
    }
  };

  return (
    <AuthGuard>
      <div className="flex flex-col items-center w-full max-w-3xl mx-auto px-6 py-8">
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <Spinner className="size-6" />
          </div>
        ) : !guide ? (
          <section className="flex flex-col items-center w-full gap-4">
            <ErrorAlert
              message="Não conseguimos carregar este guia, ele pode ter sido excluído. Verifique sua conexão e tente novamente."
              onClose={() => navigate("/dashboard/my-guides")}
            />
            <Link to="/dashboard/my-guides" className="w-full sm:w-auto">
              <Button className="w-full sm:w-auto">
                <ChevronLeft size={18} />
                Voltar para Meus Guias
              </Button>
            </Link>
          </section>
        ) : (
          <article className="flex flex-col gap-6 w-full animate-fade-in">
            {/* Header */}
            <section className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 w-full">
              <div className="flex-1">
                <h1 className="font-bold font-serif text-2xl sm:text-3xl lg:text-4xl wrap-break-word">
                  {guide.inputs?.title}
                </h1>
                <p className="text-muted-foreground text-sm sm:text-base mt-2">
                  {guide.inputs?.topic}
                </p>
              </div>
              <Link to="/dashboard/my-guides" className="w-full sm:w-auto">
                <Button variant="outline" className="w-full sm:w-auto">
                  <ChevronLeft size={18} />
                  Voltar
                </Button>
              </Link>
            </section>

            {/* Progress */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">
                    Progresso: {completedDays}/{totalDays} dias
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold">
                      {progressPercentage}%
                    </span>
                    {(showSavingFeedback || isSaving) && (
                      <div className="flex items-center gap-1 text-xs text-muted-foreground animate-pulse">
                        <div className="w-2 h-2 bg-muted-foreground rounded-full" />
                        Salvando...
                      </div>
                    )}
                    {!showSavingFeedback && !isSaving && guide && (
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Check size={14} />
                        Salvo
                      </div>
                    )}
                  </div>
                </div>
                <div className="w-full bg-muted rounded-md h-2">
                  <div
                    className="bg-primary h-2 rounded-md transition-all duration-300"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            {/* Study Days */}
            <Accordion
              type="single"
              defaultValue="dia1"
              collapsible
              className="flex flex-col w-full space-y-3"
            >
              {Array.isArray(guide.daily_study) && guide.daily_study.length ? (
                guide.daily_study.map((study: any, index: number) => (
                  <AccordionItem
                    key={study.day}
                    value={"dia" + study.day}
                    className={`border px-3 md:px-4 rounded-md transition-all duration-200 ${
                      study.completed
                        ? "bg-accent border-primary border-2 shadow-sm"
                        : "bg-background border-border"
                    }`}
                  >
                    <AccordionTrigger className="hover:no-underline py-4">
                      <div className="flex items-start sm:items-center gap-3 text-left w-full">
                        <Checkbox
                          disabled={isLoading}
                          onClick={(e: React.MouseEvent) => e.stopPropagation()}
                          onCheckedChange={(checked: boolean) =>
                            handleDayStatusChange(index, !!checked)
                          }
                          checked={study.completed}
                          className="h-5 w-5 mt-1 sm:mt-0 shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
                          aria-label={`Marcar dia ${study.day} como ${study.completed ? "incompleto" : "completo"}`}
                        />
                        <span
                          className={`text-sm sm:text-base flex-1 ${
                            study.completed
                              ? "font-bold line-through opacity-75"
                              : "font-medium"
                          }`}
                        >
                          Dia {study.day} - {study.title}
                        </span>
                        {isLoading && <Spinner className="size-4" />}
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="space-y-4 text-left sm:text-justify text-sm sm:text-base pb-4 pt-4">
                      <div>
                        <h3 className="font-bold mb-2">Meta:</h3>
                        <p className="text-muted-foreground">{study.goal}</p>
                      </div>
                      <div>
                        <h3 className="font-bold mb-3">O que pesquisar:</h3>
                        <ul className="space-y-2 pl-4">
                          {study.theoretical_research.map(
                            (searchItem: string, i: number) => (
                              <li key={i} className="flex gap-3 items-start">
                                <Lightbulb
                                  size={18}
                                  className="text-muted-foreground shrink-0 mt-0.5"
                                  aria-hidden="true"
                                />
                                <span>{searchItem}</span>
                              </li>
                            ),
                          )}
                        </ul>
                      </div>
                      <div>
                        <h3 className="font-bold mb-2">Mão na massa:</h3>
                        <p className="text-muted-foreground">
                          {study.practical_activity}
                        </p>
                      </div>
                      <div>
                        <h3 className="font-bold mb-2">
                          Verificação de Aprendizado:
                        </h3>
                        <p className="text-muted-foreground">
                          {study.learning_verification}
                        </p>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))
              ) : (
                <section className="flex flex-col items-center gap-3 py-12">
                  <AlertCircle size={32} className="text-muted-foreground" />
                  <p className="text-center text-muted-foreground text-sm sm:text-base">
                    Não foi possível recuperar os dias de estudo desse guia.
                    <br />
                    Tente recarregar a página ou entre em contato com o suporte
                    se o problema persistir.
                  </p>
                </section>
              )}
            </Accordion>

            {/* Delete */}
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
    </AuthGuard>
  );
}
