"use client";

import GuestGuard from "@/components/guest-guard";
import { LoginForm } from "@/components/login-form";

export default function LoginPage() {
    return (
        <GuestGuard>
            <div className="flex w-full items-center justify-center">
                <div className="w-full max-w-sm">
                    <LoginForm />
                </div>
            </div>
        </GuestGuard>
    );
}
