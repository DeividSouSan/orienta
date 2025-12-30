import { useEffect, useRef, useState } from "react";
import { useMessage } from "./useMessage";

export function useStudyGuide(guideId) {
    const [guide, setGuide] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSavingBatch, setIsSavingBatch] = useState(false);

    const { errorMessage } = useMessage();

    const lastSavedBatch = useRef("");

    useEffect(() => {
        async function getGuide() {
            if (!guideId) return;
            try {
                const response = await fetch(`/api/v1/guides/${guideId}`, {
                    method: "GET",
                    credentials: "include",
                });

                if (response.ok) {
                    const responseBody = await response.json();

                    setGuide(responseBody.data);
                    lastSavedBatch.current = JSON.stringify(
                        responseBody.data.daily_study,
                    );
                }
            } catch (error) {
                console.error("Erro ao buscar o guia: ", error);
            } finally {
                setIsLoading(false);
            }
        }

        getGuide();
    }, []);

    const updateDayCompletion = (dayIndex, isChecked) => {
        setGuide((prevGuide) => {
            const updatedDailyStudy = [...prevGuide.daily_study];
            updatedDailyStudy[dayIndex] = {
                ...updatedDailyStudy[dayIndex],
                completed: isChecked,
            };

            return { ...prevGuide, daily_study: updatedDailyStudy };
        });
    };

    useEffect(() => {
        if (!guide) return;

        const currentBatchString = JSON.stringify(guide.daily_study);
        if (currentBatchString === lastSavedBatch.current) return;

        const timeoutId = setTimeout(async () => {
            setIsSavingBatch(true);

            try {
                await fetch(`/api/v1/guides/${guideId}`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify({
                        new_studies_list: guide.daily_study,
                    }),
                });
                lastSavedBatch.current = currentBatchString;
            } catch (error) {
                errorMessage("Erro ao salvar os estudos.");
            } finally {
                setIsSavingBatch(false);
            }
        }, 2000);

        return () => clearTimeout(timeoutId);
    }, [guide, guideId]);
    return { guide, isLoading, updateDayCompletion, isSavingBatch };
}
