import { boolean, z } from "zod";

export const VALIDATION_LIMITS = {
  TITLE_MIN: 10,
  TITLE_MAX: 40,
  TOPIC_MIN: 10,
  TOPIC_MAX: 150,
  FOCUS_TIME_MIN: 30,
  FOCUS_TIME_MAX: 480,
  DAYS_MIN: 3,
  DAYS_MAX: 30,
};

// TODO Criar um arquivo de configuração pra usar no front e no back

export const TitleSchema = z
  .string()
  .trim()
  .min(
    VALIDATION_LIMITS.TITLE_MIN,
    "O título deve ter no mínimo 10 caracteres.",
  )
  .max(
    VALIDATION_LIMITS.TITLE_MAX,
    "O título deve ter no máximo 40 caracteres.",
  );

export const TopicSchema = z
  .string()
  .trim()
  .min(10, "O tópico deve ter no mínimo 10 caracteres.")
  .max(150, "O tópico deve ter no máximo 150 caracteres.");

export const KnowledgeLevelSchema = z.string();

export const FocusTimeSchema = z
  .number()
  .min(30, "O tempo de estudo deve ser no mínimo 30 minutos.")
  .max(480, "O tempo de estudo deve ser no máximo 480.");

export const DaysSchema = z
  .number()
  .min(3, "O número de dias deve ser no mínimo 3 dias.")
  .max(30, "O número de dias deve ser no máximo 30 dias.");

export const GuideSchema = z.object({
  id: z.string(),
  title: z.string(),
  topic: z.string(),
  days: z.number(),
  created_at: z.string(),
  status: z.string(),
  completed_at: z.string().optional(),
  daily_studies: z.array(z.any()).optional(),
});

const GuideFormSchema = z.object({
  title: TitleSchema,
  topic: TopicSchema,
  knowledgeLevel: KnowledgeLevelSchema,
  focusTime: FocusTimeSchema,
  days: DaysSchema,
});

export const StudyDaySchema = z.object({
  title: z.string(),
  day: z.int(),
  goal: z.string(),
  theoretical_research: z.array(z.string()),
  practical_activity: z.string(),
  learning_verification: z.string(),
  completed: z.boolean(),
});

export const GenerateGuideData = z.object({
  id: z.int(),
  owner: z.string(),
  inputs: GuideFormSchema,
  model: z.string(),
  temperature: z.literal(2.0),
  generation_time_seconds: z.int(),
  daily_study: z.array(StudyDaySchema),
  created_at: z.date(),
  is_public: z.boolean(),
});

export const GenerateGuideResponse = z.object({
  message: z.string(),
  data: GenerateGuideData,
});

export type GuideForm = z.infer<typeof GuideFormSchema>;

export type Topic = z.infer<typeof TopicSchema>;
