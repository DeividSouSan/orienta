import AuthGuard from "@/components/auth-guard";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { ArrowLeft, RotateCcw, Sparkles } from "lucide-react";
import { useMessage } from "@/hooks/useMessage";
import { useGuideAPI } from "@/hooks/useGuideApi";
import { z } from "zod";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

import {
  DaysSchema,
  FocusTimeSchema,
  GuideForm,
  KnowledgeLevelSchema,
  TitleSchema,
  TopicSchema,
} from "@/schemas/guideSchema";

export default function GeneratePage() {
  const navigate = useNavigate();
  const message = useMessage();
  const guide = useGuideAPI();

  const { createTopic, generateGuide, isLoading } = guide;
  const { successMessage, errorMessage } = message;

  const [currentStep, setCurrentStep] = useState(0);
  const progressPercentage = (currentStep / 3) * 100;

  const [formData, setFormData] = useState<GuideForm>({
    title: "",
    topic: "",
    knowledgeLevel: "iniciante",
    focusTime: 30,
    days: 7,
  });

  const handleNext = async () => {
    console.log(currentStep);
    if (currentStep === 0) {
      try {
        TitleSchema.parse(formData.title);
        TopicSchema.parse(formData.topic);

        const result = await createTopic(formData.topic);

        if (!result.success) {
          errorMessage(result.message);
        } else {
          setCurrentStep((prev) => prev + 1);
        }
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.issues.forEach((err) => {
            errorMessage(err.message);
          });
        }
      }
    } else if (currentStep === 1) {
      try {
        KnowledgeLevelSchema.parse(formData.knowledgeLevel);

        setCurrentStep((prev) => prev + 1);
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.issues.forEach((err) => {
            errorMessage(err.message);
          });
        }
      }
    } else if (currentStep === 2) {
      try {
        FocusTimeSchema.parse(formData.focusTime);
        DaysSchema.parse(formData.days);

        setCurrentStep((prev) => prev + 1);
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.issues.forEach((err) => {
            errorMessage(err.message);
          });
        }
      }
    } else {
      await handleGenerate();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    } else {
      navigate("/dashboard");
    }
  };

  const handleRestart = () => {
    setFormData({
      title: "",
      topic: "",
      knowledgeLevel: "iniciante",
      focusTime: 30,
      days: 7,
    });
    setCurrentStep(1);
  };

  const handleGenerate = async () => {
    const result = await generateGuide(formData);

    if (!result.success) {
      errorMessage(result.message);
      return;
    }

    successMessage(result.message);
  };

  return (
    <AuthGuard>
      <div className="flex min-h-full items-center justify-center px-6 py-12">
        <div className="w-full max-w-2xl">
          <Card className="animate-fade-in">
            <CardHeader className="text-center space-y-4">
              <div>
                <p className="text-sm text-muted-foreground mb-3">
                  Etapa {currentStep + 1} de 3
                </p>
                <div className="w-full bg-muted rounded-md h-2 mb-6">
                  <div
                    className="bg-primary h-2 rounded-md transition-all duration-500 ease-out"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>

              <CardTitle className="font-serif text-3xl md:text-4xl">
                O que vamos dominar hoje?
              </CardTitle>
              <CardDescription className="text-base">
                {currentStep === 0 &&
                  "Defina um tema e vamos criar um guia personalizado"}
                {currentStep === 1 &&
                  "Ajuste o guia ao seu nível atual de conhecimento"}
                {currentStep === 2 &&
                  "Configure a duração e ritmo dos seus estudos"}
              </CardDescription>

              {currentStep !== 3 && (
                <Button
                  onClick={handleRestart}
                  variant="ghost"
                  size="sm"
                  className="mx-auto mt-4"
                >
                  <RotateCcw className="w-4 h-4" />
                  Recomeçar
                </Button>
              )}
            </CardHeader>

            <CardContent>
              {currentStep === 0 && (
                <div className="space-y-6 animate-fade-in">
                  <div className="space-y-2">
                    <Label htmlFor="title" className="">
                      Dê um nome para esse seu novo estudo
                    </Label>
                    <Input
                      type="text"
                      id="title"
                      value={formData.title}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          title: e.target.value,
                        })
                      }
                      placeholder="Ex: Observabilidade (Intro)"
                      maxLength={40}
                    />
                    <p className="text-xs text-muted-foreground text-right">
                      {formData.title.length}/40
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="topic" className="">
                      O que você gostaria de estudar?
                    </Label>
                    <Textarea
                      id="topic"
                      value={formData.topic}
                      onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                        setFormData({
                          ...formData,
                          topic: e.target.value,
                        })
                      }
                      placeholder="Descreva em detalhes o que você quer aprender..."
                      rows={4}
                      maxLength={150}
                      className=""
                    />
                    <p className="text-xs text-muted-foreground text-right">
                      {formData.topic.length}/150
                    </p>
                  </div>
                </div>
              )}

              {currentStep === 1 && (
                <div className="space-y-4 animate-fade-in">
                  <Label className="block mb-4">
                    Qual seu nível de conhecimento em relação a:
                  </Label>
                  <div className="bg-muted border rounded-md p-4 mb-6">
                    <p className="text-sm italic leading-relaxed">
                      {formData.topic}
                    </p>
                  </div>

                  <div className="space-y-3">
                    {[
                      {
                        value: "zero",
                        label: "Nenhum conhecimento",
                        topic: "Estou começando do zero",
                      },
                      {
                        value: "iniciante",
                        label: "Iniciante",
                        topic: "Tenho conhecimentos básicos",
                      },
                      {
                        value: "intermediario",
                        label: "Intermediário/Avançado",
                        topic: "Quero me aprofundar",
                      },
                    ].map((option) => (
                      <label
                        key={option.value}
                        className={`flex items-start gap-4 p-4 border-2 rounded-md cursor-pointer transition-all ${
                          formData.knowledgeLevel === option.value
                            ? "border-primary bg-accent"
                            : "border-border bg-background hover:border-muted-foreground/50"
                        }`}
                      >
                        <input
                          type="radio"
                          name="knowledgeLevel"
                          value={option.value}
                          checked={formData.knowledgeLevel === option.value}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              knowledgeLevel: e.target.value,
                            })
                          }
                          className="mt-1 w-5 h-5 cursor-pointer"
                        />
                        <div className="flex-1">
                          <p className="font-medium">{option.label}</p>
                          <p className="text-sm text-muted-foreground">
                            {option.topic}
                          </p>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-6 animate-fade-in">
                  <div className="mb-8">
                    <h3 className="font-serif text-xl mb-6">
                      Informações temporais:
                    </h3>

                    <div className="space-y-6">
                      <div className="space-y-2">
                        <Label htmlFor="dailyMinutes" className="">
                          Quanto tempo você pode se dedicar por dia (em
                          minutos)?
                        </Label>
                        <Input
                          type="number"
                          id="dailyMinutes"
                          value={formData.focusTime}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              focusTime: parseInt(e.target.value),
                            })
                          }
                          min={30}
                          max={480}
                        />
                        <p className="text-xs text-muted-foreground">
                          30 a 480 minutos
                        </p>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="totalDays" className="">
                          Qual será a duração total do estudo (em dias)?
                        </Label>
                        <Input
                          type="number"
                          id="totalDays"
                          value={formData.days}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              days: parseInt(e.target.value),
                            })
                          }
                          min={3}
                          max={30}
                        />
                        <p className="text-xs text-muted-foreground">
                          3 a 30 dias
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              {currentStep === 3 && (
                <div className="space-y-4 animate-fade-in">
                  <div className="space-y-3">
                    <div className="border rounded-md p-4 bg-muted/30">
                      <p className="text-xs text-muted-foreground mb-1">
                        Título
                      </p>
                      <p className="font-medium">{formData.title}</p>
                    </div>

                    <div className="border rounded-md p-4 bg-muted/30">
                      <p className="text-xs text-muted-foreground mb-1">
                        Tópico
                      </p>
                      <p className="font-medium">{formData.topic}</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="border rounded-md p-4 bg-muted/30">
                        <p className="text-xs text-muted-foreground mb-1">
                          Nível
                        </p>
                        <p className="font-medium capitalize">
                          {formData.knowledgeLevel}
                        </p>
                      </div>

                      <div className="border rounded-md p-4 bg-muted/30">
                        <p className="text-xs text-muted-foreground mb-1">
                          Dedicação diária
                        </p>
                        <p className="font-medium">
                          {formData.focusTime} minutos
                        </p>
                      </div>

                      <div className="border rounded-md p-4 bg-muted/30">
                        <p className="text-xs text-muted-foreground mb-1">
                          Duração total
                        </p>
                        <p className="font-medium">{formData.days} dias</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-3 mt-6">
                <Button
                  onClick={handleBack}
                  variant="outline"
                  className="flex-1"
                  size="lg"
                >
                  <ArrowLeft className="w-4 h-4" />
                  Voltar
                </Button>

                <Button
                  onClick={handleNext}
                  disabled={isLoading}
                  className="flex-1"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Gerando...
                    </>
                  ) : currentStep === 3 ? (
                    <>
                      <Sparkles className="w-4 h-4" />
                      Gerar o guia
                    </>
                  ) : (
                    "Avançar"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  );
}
