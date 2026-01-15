/*
Serviços fazem requisições à API do Orienta, validando os dados de
entrada e os dados de saída utilizando a biblioteca Zod.

Os argumentos são esquemas de requisição (FooRequest) que são validados
(utilizando .parse) na página, antes de serem fornecidos como
argumento para os Serviços. Os retornos são as respostas, que devem
aderir ao esquema e portanto são validadas utilizando .parse().

Serviços sobem erros! Caso a resposta da API seja diferente de 200-299
um erro ocorreu. As mensagens de erro da API já são formatados por
isso é possível usar throw new APIError(error) diretamente.
*/

import { APIError } from "@/errors";
import {
  GenerateGuideResponse,
  GuideForm,
  Topic,
  TopicData,
} from "@/schemas/guideSchema";

async function createTopic(topic: Topic): Promise<void> {
  const response = await fetch("/api/v1/validations/topic", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ topic }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new APIError(error);
  }
}

async function deleteGuideById(guideId: string) {
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

async function getMyGuides() {
  const response = await fetch("/api/v1/my-guides", {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Erro ao buscar guias. Tente novamente.");
  }
  return response.json();
}

async function getGuideById(guideId: string) {
  const response = await fetch(`/api/v1/guides/${guideId}`, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.message || "Erro ao buscar o guia especificado. Tente novamente.",
    );
  }
  return response.json();
}

async function updateGuideById(guideId: string, updated_daily_studies: any) {
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
    throw new Error(error.message || "Erro ao salvar o guia. Tente novamente.");
  }
  return response.json();
}

async function generateGuide(formData: GuideForm) {
  const response = await fetch("/api/v1/guides", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
      title: formData.title,
      topic: formData.topic,
      knowledge: formData.knowledgeLevel,
      focus_time: formData.focusTime,
      days: formData.days,
    }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new APIError(error);
  }
}

export const guideService = {
  createTopic,
  deleteGuideById,
  getMyGuides,
  getGuideById,
  updateGuideById,
  generateGuide,
};
