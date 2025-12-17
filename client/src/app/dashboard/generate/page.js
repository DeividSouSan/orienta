import { GuideForm } from "@/components/guide-form";

export default function GenerateGuidePage() {
    return (
        <>
            <div className="flex flex-col w-full items-center justify-center">
                <div className="w-full max-w-sm">
                    <GuideForm />
                </div>
            </div>
        </>
    );
}
