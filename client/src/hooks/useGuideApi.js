import { useState } from "react";
import { GuideSchema } from "@/schemas/guideSchema";
import { z } from "zod";

export function useGuideAPI() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleError = (error, defaultMessage) => {
        let message = defaultMessage;

        if (error instanceof z.ZodError) {
            message = "Dados inválidos recebidos da API.";
        } else if (
            error instanceof TypeError &&
            error.message.includes("fetch")
        ) {
            message = "Erro de conexão. Verifique sua internet.";
        }

        setError(message);
        return message;
    };

    const fetchGuides = async () => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch("/api/v1/guides", {
                method: "GET",
                credentials: "include",
            });

            const responseBody = await response.json();

            if (!response.ok) {
                throw new Error(
                    responseBody.message ||
                        "Erro ao buscar guias. Tente novamente.",
                );
            }

            let inProgressGuides = [];
            let completedGuides = [];

            responseBody.data.forEach((guideInfo) => {
                try {
                    GuideSchema.parse(guideInfo);

                    if (guideInfo.status === "studying") {
                        inProgressGuides.push(guideInfo);
                    } else {
                        completedGuides.push(guideInfo);
                    }
                } catch (error) {
                    handleError(
                        error,
                        "Alguns dados dos guias estão inválidos.",
                    );
                }
            });

            setIsLoading(false);
            return { inProgressGuides, completedGuides };
        } catch (error) {
            handleError(error, "Erro ao buscar guias. Tente novamente.");
            setIsLoading(false);
            return null;
        }
    };

    const deleteGuide = async (guideId) => {
        setError(null);

        try {
            const response = await fetch(`/api/v1/guides/${guideId}`, {
                method: "DELETE",
                credentials: "include",
            });

            const responseBody = await response.json();

            if (!response.ok) {
                throw new Error(
                    responseBody.message ||
                        "Erro ao deletar guia. Tente novamente.",
                );
            }

            return { ok: true };
        } catch (error) {
            const message = handleError(
                error,
                "Erro ao deletar guia. Tente novamente.",
            );
            return { ok: false, error: message };
        }
    };

    return {
        isLoading,
        error,
        setError,
        fetchGuides,
        deleteGuide,
    };
}
