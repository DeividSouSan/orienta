import { SignupForm } from "@/components/signup-form";

export default function RegisterPage() {
    return (
        <>
            <div className="flex w-full items-center justify-center">
                <div className="w-full max-w-sm">
                    <SignupForm />
                </div>
            </div>
        </>
    );
}
