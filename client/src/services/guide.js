export async function deleteGuideRequest(guideId) {
    const response = await fetch(`/api/v1/guides/${guideId}`, {
        method: "DELETE",
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Ocorreu um erro ao deletar o guia.");
    }

    return response.json();
}

export async function getGuidesRequest() {
    const response = await fetch("/api/v1/my-guides", {
        method: "GET",
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.message || "Erro ao buscar guias. Tente novamente.",
        );
    }
    return response.json();
}

export async function getGuideByIdRequest(guideId) {
    const response = await fetch(`/api/v1/guides/${guideId}`, {
        method: "GET",
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.message ||
                "Erro ao buscar o guia especificado. Tente novamente.",
        );
    }
    return response.json();
}

export async function patchGuideById(guideId, updated_daily_studies) {
    const response = await fetch(`/api/v1/guides/${guideId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
            new_studies_list: updated_daily_studies,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.message || "Erro ao salvar o guia. Tente novamente.",
        );
    }
    return response.json();
}
