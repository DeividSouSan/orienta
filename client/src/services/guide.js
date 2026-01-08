export async function deleteGuideRequest(guideId) {
    const response = await fetch(`/api/v1/guides/${guideId}`, {
        method: "DELETE",
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Ocorreu um erro ao deletar o guia.")
    }

    return response.json()
}

export async function getGuidesRequest() {
    const response = await fetch("/api/v1/guides", {
        method: "GET",
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.message ||
            "Erro ao buscar guias. Tente novamente.",
        );
    }
    return response.json();
}

