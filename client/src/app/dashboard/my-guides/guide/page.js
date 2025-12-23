"use client";

import GuideView from "@/components/guide-view";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Spinner } from "@/components/ui/spinner";
import AuthGuard from "@/components/auth-guard";
function GuideContent() {
    const searchParams = useSearchParams();
    const guideId = searchParams.get("id");

    return <GuideView guideId={guideId} />;
}

export default function Page() {
    return (
        <AuthGuard>
            <Suspense fallback={<Spinner />}>
                <GuideContent />
            </Suspense>
        </AuthGuard>
    );
}
