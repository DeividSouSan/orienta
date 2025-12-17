"use client";

import { AlertCircle, X } from "lucide-react";
import { Button } from "./ui/button";

export function ErrorAlert({ message, onClose }) {
    return (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 sm:p-4 flex items-start gap-3 animate-fade-in mx-3 sm:mx-4">
            <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5 w-5 h-5 sm:w-5 sm:h-5" />
            <div className="flex-1 min-w-0">
                <p className="text-xs sm:text-sm text-red-800 break-words">
                    {message}
                </p>
            </div>
            {onClose && (
                <Button
                    variant="ghost"
                    size="sm"
                    className="text-red-600 hover:text-red-700 hover:bg-red-100 flex-shrink-0"
                    onClick={onClose}
                >
                    <X size={16} />
                </Button>
            )}
        </div>
    );
}
