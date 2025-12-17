import { Lato, Lora } from "next/font/google";
import { cn } from "@/lib/utils";
import "@/app/globals.css";
import Header from "@/components/header";
import { AuthProvider } from "@/contexts/AuthContext";
import { MessageProvider } from "@/contexts/MessageContext";
import { MessageContainer } from "@/components/message-container";
// Google Fonts: Lora (serif para títulos) e Lato (sans-serif para corpo)

export const lato = Lato({
    subsets: ["latin"],
    weight: ["400", "700"],
    variable: "--font-sans",
});

export const lora = Lora({
    subsets: ["latin"],
    variable: "--font-serif",
});

// Metadados

export const metadata = {
    title: "Orienta - Sua jornada de estudos começa aqui",
    description:
        "Orienta ajuda você a planejar e organizar seus estudos de forma eficiente.",
};

export default function RootLayout({ children }) {
    return (
        <html lang="pt-br" suppressHydrationWarning>
            <body
                className={cn(
                    "font-sans antialiased ",
                    lato.variable,
                    lora.variable,
                )}
            >
                <div className="flex flex-col min-h-screen">
                    <MessageProvider>
                        <MessageContainer />
                        <AuthProvider>
                            <Header />
                            <main className="flex-1 flex">{children}</main>
                        </AuthProvider>
                    </MessageProvider>
                    <footer className="bg-white border border-t-2 py-4">
                        <div className="max-w-5xl mx-auto px-4 text-center text-gray-500 text-sm">
                            <p>
                                &copy; 2025 Orienta. Todos os direitos
                                reservados.
                            </p>
                        </div>
                    </footer>
                </div>
            </body>
        </html>
    );
}
