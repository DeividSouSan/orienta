import { z } from "zod";

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
