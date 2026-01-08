import { useState } from "react";
import { GuideSchema } from "@/schemas/guideSchema";
import { z } from "zod";
import { deleteGuideRequest, getGuidesRequest } from "@/services/guide";

export function useGuideAPI() {
    const [isLoading, setIsLoading] = useState(false);

    const fetchGuides = async () => {
        setIsLoading(true);
        try {
            const result = await getGuidesRequest();
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

            return { success: true, message: result.message, data: { inProgressGuides, completedGuides } };
        } catch (error) {
            return { success: false, error: error.message || "Um erro aconteceu. Tente novamente." }
        } finally {
            setIsLoading(false);
        }
    };

    const deleteGuide = async (guideId) => {
        setIsLoading(true);
        try {
            const result = await deleteGuideRequest(guideId);
            return { success: true, message: result.message }
        } catch (error) {
            return { success: false, error: error.message || "Um erro aconteceu. Tente novamente." }
        } finally {
            setIsLoading(false)
        }
    };

    return {
        isLoading,
        fetchGuides,
        deleteGuide,
    };
}
