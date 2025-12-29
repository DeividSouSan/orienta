import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

export function CompletedCard({ className, title, completedAt, totalDays }) {
    return (
        <Card className={cn("w-full max-w-2xl", className)}>
            <CardHeader>
                <div className="flex items-center justify-between ">
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-900 font-serif">
                            {title}
                        </h2>
                        <span className="text-sm text-gray-600">
                            Concluído em: {completedAt} ({totalDays} dias)
                        </span>
                    </div>
                    <div>
                        <Button>Revisar</Button>
                    </div>
                </div>
            </CardHeader>
        </Card>
    );
}
