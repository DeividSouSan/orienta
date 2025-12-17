import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import Link from "next/link";
import { LibraryBig, NotebookPen, Compass } from "lucide-react";

export default function DashboardPage() {
    return (
        <main className="flex w-full items-center justify-center px-3 sm:px-4">
            <div className="flex flex-col gap-6 sm:gap-12 w-full max-w-4xl animate-fade-in py-8 sm:py-12">
                <section className="text-center">
                    <div className="mb-4">
                        <Compass className="inline-block text-2xl sm:text-3xl w-8 h-8 sm:w-10 sm:h-10 text-gray-900" />
                    </div>
                    <h1 className="text-2xl sm:text-3xl lg:text-4xl font-semibold text-gray-900 mt-2 sm:mt-4 font-serif">
                        Bem-vindo ao Orienta.
                    </h1>
                    <p className="text-gray-600 mt-2 sm:mt-3 text-base sm:text-lg">
                        Seu planejador de estudos inteligente.
                    </p>
                    <p className="text-gray-500 mt-1 text-sm sm:text-base">
                        O que gostaria de fazer hoje?
                    </p>
                </section>

                <section className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 lg:gap-12 font-serif">
                    <Link
                        href="/dashboard/generate"
                        className="h-full flex flex-col transition-all duration-300 ease-in-out hover:-translate-y-2 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-lg"
                    >
                        <Card className="h-full hover:border-blue-300 transition-colors duration-300">
                            <CardHeader className="flex flex-col items-center gap-3 sm:gap-4 text-center">
                                <CardTitle className="flex flex-col items-center gap-3 sm:gap-4 text-xl sm:text-2xl">
                                    <NotebookPen className="text-gray-900 w-10 h-10 sm:w-12 sm:h-12" />
                                    Gerar Novo Guia
                                </CardTitle>
                                <CardDescription className="text-sm sm:text-base text-gray-700 leading-relaxed">
                                    Crie um plano de estudos personalizado
                                    definindo seu tópico, ritmo e duração.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                    </Link>
                    <Link
                        href="/dashboard/my-guides"
                        className="h-full flex flex-col transition-all duration-300 ease-in-out hover:-translate-y-2 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-lg"
                    >
                        <Card className="h-full hover:border-blue-300 transition-colors duration-300">
                            <CardHeader className="flex flex-col items-center gap-3 sm:gap-4 text-center">
                                <CardTitle className="flex flex-col items-center gap-3 sm:gap-4 text-xl sm:text-2xl">
                                    <LibraryBig className="text-gray-900 w-10 h-10 sm:w-12 sm:h-12" />
                                    Ver Meus Guias
                                </CardTitle>
                                <CardDescription className="text-sm sm:text-base text-gray-700 leading-relaxed">
                                    Acesse sua biblioteca pessoal, acompanhe
                                    progresso e continue estudando.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                    </Link>
                </section>
            </div>
        </main>
    );
}
