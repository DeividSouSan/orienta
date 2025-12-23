import AuthGuard from "@/components/auth-guard";
import { GuideForm } from "@/components/guide-form";

export default function GenerateGuidePage() {
    return (
        <AuthGuard>
            <GuideForm />
        </AuthGuard>
    );
}
