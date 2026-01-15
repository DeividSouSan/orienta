import { useState, useRef, useEffect } from "react";
import { guideService } from "@/services/guideService";

type Result = {
  success: boolean;
  message: string;
};

export function useCurrentGuide(guideId: string | undefined) {
  const [guide, setGuide] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const previousStudyDays = useRef("");

  const fetchGuideById = async (): Promise<Result> => {
    if (!guideId)
      return { success: false, message: "ID do guia não informado." };

    setIsLoading(true);
    try {
      const result = await guideService.getGuideById(guideId);
      setGuide(result.data);
      previousStudyDays.current = JSON.stringify(result.data?.daily_study);
      return {
        success: true,
        message: result.message,
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.message || "Erro ao buscar o guia. Tente novamente.",
      };
    } finally {
      setIsLoading(false);
    }
  };

  const updateDayStatus = (dayIndex: number, isChecked: boolean) => {
    setGuide((prevGuide: any) => {
      if (!prevGuide) return prevGuide;

      const updatedStudyDays = [...prevGuide.daily_study];
      updatedStudyDays[dayIndex] = {
        ...updatedStudyDays[dayIndex],
        completed: isChecked,
      };

      return { ...prevGuide, daily_study: updatedStudyDays };
    });
  };

  const deleteGuide = async (): Promise<Result> => {
    if (!guideId)
      return { success: false, message: "ID do guia não informado." };

    setIsDeleting(true);
    try {
      const result = await guideService.deleteGuideById(guideId);
      return {
        success: true,
        message: result.message || "Guia excluído com sucesso.",
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.message || "Erro ao excluir o guia. Tente novamente.",
      };
    } finally {
      setIsDeleting(false);
    }
  };

  // Auto-save: debounce de 2s ao alterar status dos dias
  useEffect(() => {
    if (!guide || !guideId) return;

    const currentStudyDays = JSON.stringify(guide.daily_study);
    if (currentStudyDays === previousStudyDays.current) return;

    const timeoutId = setTimeout(async () => {
      setIsSaving(true);
      try {
        await guideService.updateGuideById(guideId, guide.daily_study);
        previousStudyDays.current = currentStudyDays;
      } catch (error) {
        console.error("Erro ao salvar progresso:", error);
      } finally {
        setIsSaving(false);
      }
    }, 2000);

    return () => clearTimeout(timeoutId);
  }, [guide, guideId]);

  return {
    guide,
    isLoading,
    isSaving,
    isDeleting,
    fetchGuideById,
    updateDayStatus,
    deleteGuide,
  };
}
