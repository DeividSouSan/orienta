"use client";

import { Button } from "./ui/button";
import Link from "next/link";

export function EmptyState({
    icon: Icon,
    title,
    description,
    ctaText,
    ctaHref,
}) {
    return (
        <div className="flex flex-col items-center justify-center py-12 sm:py-16 px-4">
            <div className="mb-4">
                <Icon size={48} className="text-gray-400 sm:w-12 sm:h-12" />
            </div>
            <h3 className="text-lg sm:text-xl font-semibold text-gray-900 text-center mb-2">
                {title}
            </h3>
            <p className="text-sm sm:text-base text-gray-600 text-center mb-6 max-w-sm">
                {description}
            </p>
            {ctaText && ctaHref && (
                <Link href={ctaHref}>
                    <Button variant="default">{ctaText}</Button>
                </Link>
            )}
        </div>
    );
}
