import { useState } from "react";
import { GuideSchema } from "@/schemas/guideSchema";
import { z } from "zod";

export function useGuideApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleError = (err, defaultMessage) => {
        let message = defaultMessage;

        if (err instanceof z.ZodError) {
            message = "Dados inválidos recebidos da API.";
        } else if (err instanceof TypeError && err.message.includes("fetch")) {
            message = "Erro de conexão. Verifique sua internet.";
        }

        setError(message);
        console.error(err);
        return message;
    };

    const fetchGuides = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch("/api/v1/guides", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });

            const responseBody = await response.json();

            if (!response.ok) {
                throw new Error(
                    responseBody.message ||
                    "Erro ao buscar guias. Tente novamente."
                );
            }

            let ongoingGuidesList = [];
            let completedGuidesList = [];

            responseBody.data.forEach((guideInfo) => {
                try {
                    GuideSchema.parse(guideInfo);
                    if (guideInfo.status === "studying") {
                        ongoingGuidesList.push(guideInfo);
                    } else {
                        completedGuidesList.push(guideInfo);
                    }
                } catch (validationError) {
                    handleError(
                        validationError,
                        "Alguns dados dos guias estão inválidos."
                    );
                }
            });

            setLoading(false);
            return { ongoingGuidesList, completedGuidesList };
        } catch (err) {
            handleError(err, "Erro ao buscar guias. Tente novamente.");
            setLoading(false);
            return null;
        }
    };

    const deleteGuide = async (guideId) => {
        setError(null);

        try {
            const response = await fetch(`/api/guides/${guideId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });

            const responseBody = await response.json();

            if (!response.ok) {
                throw new Error(
                    responseBody.message ||
                    "Erro ao deletar guia. Tente novamente."
                );
            }

            return { success: true };
        } catch (err) {
            const message = handleError(
                err,
                "Erro ao deletar guia. Tente novamente."
            );
            return { success: false, error: message };
        }
    };

    return {
        loading,
        error,
        setError,
        fetchGuides,
        deleteGuide,
    };
}
