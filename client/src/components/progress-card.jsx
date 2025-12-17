import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

import { cn } from "@/lib/utils";
export function ProgressCard({
    className,
    title,
    topic,
    createdAt,
    progress,
    totalDays,
}) {
    return (
        <Card className={cn("w-full max-w-2xl", className)}>
            <CardHeader>
                <div className="flex items-start justify-between">
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-900 font-serif">
                            {title}
                        </h2>
                        <p className="mt-1 text-md text-gray-600">{topic}</p>
                    </div>
                    <span className="text-sm text-gray-600">
                        {totalDays} dias
                    </span>
                </div>
            </CardHeader>

            <CardContent>
                <div className="space-y-4">
                    <p className="text-sm text-gray-600">
                        Criado em: {createdAt}
                    </p>
                    <div className="space-y-2">
                        <p className="text-sm text-gray-600">Progresso</p>
                        <Progress value={progress} className="h-2" />
                        <p className="text-right text-sm text-gray-600">
                            {progress}%
                        </p>
                    </div>
                </div>
            </CardContent>

            <CardFooter className="flex justify-between">
                <Button variant="default">Continuar Estudo</Button>
                <Button variant="ghost" className="text-gray-600">
                    Excluir
                </Button>
            </CardFooter>
        </Card>
    );
}
