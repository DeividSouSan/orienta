import { useState, useRef, useEffect } from "react";
import { GuideSchema } from "@/schemas/guideSchema";
import { z } from "zod";
import {
    deleteGuideRequest,
    getGuidesRequest,
    getGuideByIdRequest,
    patchGuideById,
} from "@/services/guide";

export function useGuideAPI(guideId) {
    const [guide, setGuide] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    const previousStudyDays = useRef("");

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

    const fetchGuideById = async () => {
        setIsLoading(true);
        try {
            const result = await getGuideByIdRequest(guideId);
            setGuide(result.data);
            return {
                success: true,
                message: result.message,
                data: result.data,
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

    const updateDayStatus = async (dayIndex, isChecked) => {
        setGuide((prevGuide) => {
            const updatedStudyDays = [...prevGuide.daily_study];

            updatedStudyDays[dayIndex] = {
                ...updatedStudyDays[dayIndex],
                completed: isChecked,
            };

            return { ...prevGuide, daily_study: updatedStudyDays };
        });
    };

    const deleteGuide = async () => {
        setIsDeleting(true);
        try {
            const result = await deleteGuideRequest(guideId);
            return { success: true, message: result.message };
        } catch (error) {
            return {
                success: false,
                error: error.message || "Um erro aconteceu. Tente novamente.",
            };
        } finally {
            setIsDeleting(false);
        }
    };

    useEffect(() => {
        if (!guide) return;

        const currentStudyDays = JSON.stringify(guide.daily_study);
        if (currentStudyDays === previousStudyDays.current) return;

        const timeoutId = setTimeout(async () => {
            setIsSaving(true);

            try {
                const result = await patchGuideById(guideId, guide.daily_study);
                previousStudyDays.current = currentStudyDays;
                return { success: true, message: result.message };
            } catch (error) {
                return {
                    success: false,
                    error:
                        error.message || "Um erro aconteceu. Tente novamente.",
                };
            } finally {
                setIsSaving(false);
            }
        }, 2000);

        return () => clearTimeout(timeoutId);
    }, [guide]);

    return {
        guide,
        isLoading,
        isSaving,
        isDeleting,
        fetchGuides,
        fetchGuideById,
        updateDayStatus,
        deleteGuide,
    };
}
