import { useState, useRef, useEffect } from "react";
import { GuideForm, GuideSchema } from "@/schemas/guideSchema";
import { z } from "zod";
import { guideService } from "@/services/guideService";
import { APIError } from "@/errors";
import { useAuth } from "./useAuth";

type Result = {
  success: boolean;
  message: string;
};

export function useGuideAPI() {
  const auth = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const { logout } = auth;

  const createTopic = async (topic: string): Promise<Result> => {
    setIsLoading(true);
    try {
      await guideService.createTopic(topic);

      return {
        success: true,
        message: "Tópico é válido.",
      };
    } catch (error) {
      console.error(error);
      let message = "Erro interno aconteceu.";
      if (error instanceof APIError) {
        message = error.message;
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      setIsLoading(false);
    }
  };

  const fetchGuides = async () => {
    setIsLoading(true);
    try {
      const result = await guideService.getMyGuides();
      let inProgressGuides = [];
      let completedGuides = [];

      result.data.forEach((guideInfo) => {
        GuideSchema.parse(guideInfo);

        if (guideInfo.status === "studying") {
          inProgressGuides.push(guideInfo);
        } else {
          completedGuides.push(guideInfo);
        }
      });

      return {
        success: true,
        message: result.message,
        data: { inProgressGuides, completedGuides },
      };
    } catch (error) {
      return {
        success: false,
        error: error.message || "Um erro aconteceu. Tente novamente.",
      };
    } finally {
      setIsLoading(false);
    }
  };

  const generateGuide = async (formData: GuideForm): Promise<Result> => {
    setIsLoading(true);
    try {
      await guideService.generateGuide(formData);

      return {
        success: true,
        message: "Guia gerado com sucesso!",
      };
    } catch (error) {
      console.error(error);
      let message = "Erro interno aconteceu.";
      if (error instanceof APIError) {
        if (error.code === 401) {
          await logout();
        }

        message = error.message;
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    createTopic,
    fetchGuides,
    generateGuide,
  };
}
