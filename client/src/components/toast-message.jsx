import * as React from "react";
import { cn } from "@/lib/utils";
import { CheckCircle, XCircle, X } from "lucide-react";

export function ToastMessage({ type, message, onClose, className, ...props }) {
    const isSuccess = type === "success";

    return (
        <div
            className={cn(
                "fixed top-20 right-6 z-50 flex items-center justify-between px-4 py-3 rounded-sm shadow-lg border gap-3",
                isSuccess
                    ? "bg-green-50 border-green-400 text-green-800"
                    : "bg-red-50 border-red-400 text-red-800",
                className,
            )}
            role="alert"
            {...props}
        >
            <div className="flex items-center gap-2">
                {isSuccess ? (
                    <CheckCircle
                        className="w-5 h-5 text-green-500 flex-shrink-0"
                        aria-hidden="true"
                    />
                ) : (
                    <XCircle
                        className="w-5 h-5 text-red-500 flex-shrink-0"
                        aria-hidden="true"
                    />
                )}
                <span className="font-semibold">{message}</span>
            </div>

            <button
                onClick={onClose}
                className={cn(
                    "p-1 rounded-md hover:opacity-75 transition-opacity flex-shrink-0 cursor-pointer",
                    isSuccess ? "hover:bg-green-100" : "hover:bg-red-100",
                )}
                aria-label="Fechar notificação"
            >
                <X className="w-4 h-4" />
            </button>
        </div>
    );
}
