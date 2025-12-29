"use client";

import { Card, CardContent, CardFooter, CardHeader } from "./ui/card";

export function CardSkeleton() {
    return (
        <Card className="w-full max-w-2xl animate-pulse">
            <CardHeader className="pb-3 sm:pb-4">
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                    <div className="flex-1">
                        <div className="h-6 sm:h-7 bg-gray-300 rounded w-3/4 mb-2"></div>
                        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                    </div>
                    <div className="h-4 bg-gray-300 rounded w-16"></div>
                </div>
            </CardHeader>

            <CardContent className="pb-3 sm:pb-4">
                <div className="space-y-3 sm:space-y-4">
                    <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                    <div className="space-y-2">
                        <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                        <div className="h-2 bg-gray-200 rounded w-full"></div>
                        <div className="h-4 bg-gray-200 rounded w-1/4 ml-auto"></div>
                    </div>
                </div>
            </CardContent>

            <CardFooter className="flex flex-col sm:flex-row gap-2 sm:gap-0 sm:justify-between">
                <div className="h-10 bg-gray-300 rounded w-full sm:w-32"></div>
                <div className="h-10 bg-gray-200 rounded w-full sm:w-24"></div>
            </CardFooter>
        </Card>
    );
}
