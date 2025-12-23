"use client";

import { Button } from "./ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./ui/card";

export function ConfirmDialog({
    title,
    description,
    onConfirm,
    onCancel,
    isLoading = false,
}) {
    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-sm">
                <CardHeader className="pb-3">
                    <CardTitle className="text-lg sm:text-xl">
                        {title}
                    </CardTitle>
                    {description && (
                        <CardDescription className="text-xs sm:text-sm mt-2">
                            {description}
                        </CardDescription>
                    )}
                </CardHeader>
                <CardFooter className="flex gap-2 justify-end flex-col-reverse sm:flex-row">
                    <Button
                        variant="ghost"
                        onClick={onCancel}
                        disabled={isLoading}
                        className="w-full sm:w-auto"
                    >
                        Cancelar
                    </Button>
                    <Button
                        variant="destructive"
                        onClick={onConfirm}
                        disabled={isLoading}
                        className="w-full sm:w-auto"
                    >
                        {isLoading ? "Processando..." : "Confirmar"}
                    </Button>
                </CardFooter>
            </Card>
        </div>
    );
}
