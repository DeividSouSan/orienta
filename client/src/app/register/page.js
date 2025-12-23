import GuestGuard from "@/components/guest-guard";
import { SignupForm } from "@/components/signup-form";

export default function RegisterPage() {
    return (
        <GuestGuard>
            <div className="flex w-full items-center justify-center">
                <div className="w-full max-w-sm">
                    <SignupForm />
                </div>
            </div>
        </GuestGuard>
    );
}
