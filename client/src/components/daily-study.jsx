import {
    Accordion,
    AccordionItem,
    AccordionContent,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { Checkbox } from "@/components/ui/checkbox";
import { useState } from "react";
export function DailyStudyAccordion({
    day,
    title,
    goal,
    learningVerification,
    theoreticalResearch,
    practicalActivity,
    completed,
}) {
    const [checked, setChecked] = useState(completed);
    return (
        <AccordionItem
            value={"dia" + day}
            className={`px-4 mb-4 rounded-md border transition-all duration-200 ${checked ? "bg-green-50 border-black border-2 shadow-sm" : "bg-white border-gray-200"}`}
        >
            <AccordionTrigger>
                <div className="flex items-center gap-3 text-left">
                    <Checkbox
                        onClick={(e) => e.stopPropagation()}
                        onCheckedChange={(e) => setChecked(!checked)}
                        checked={checked}
                        className="h-5 w-5 rounded border-gray-300 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                    />
                    <span
                        className={`text-base ${checked ? "font-bold text-gray-900" : "font-medium text-gray-700"}`}
                    >
                        Dia {day} - {title}
                    </span>
                </div>
            </AccordionTrigger>
            <AccordionContent className="space-y-3 text-gray-700 text-justify">
                <p>
                    <strong>Meta: </strong>
                    {goal}
                </p>
                <p>
                    <strong>O que pesquisar: </strong>
                </p>
                <ul className="pl-5 mt-2 space-y-1">
                    {theoreticalResearch.map((searchItem) => {
                        return <li>💡 {searchItem}</li>;
                    })}
                </ul>
                <p>
                    <strong>Mão na massa: </strong>
                    {learningVerification}
                </p>
                <p>
                    <strong>Verficação do Aprendizado: </strong>
                    {practicalActivity}
                </p>
            </AccordionContent>
        </AccordionItem>
    );
}
