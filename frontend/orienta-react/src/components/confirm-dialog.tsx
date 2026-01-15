import { useEffect } from "react";
import { createPortal } from "react-dom";
import { Button } from "./ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";

interface ConfirmDialogProps {
  title: string;
  description?: string;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export function ConfirmDialog({
  title,
  description,
  onConfirm,
  onCancel,
  isLoading = false,
}: ConfirmDialogProps) {
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  return createPortal(
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onCancel}
    >
      <Card className="w-full max-w-sm" onClick={(e) => e.stopPropagation()}>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg sm:text-xl">{title}</CardTitle>
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
    </div>,
    document.body,
  );
}
