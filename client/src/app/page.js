import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
    return (
        <div className="flex flex-col items-center w-full border-4">
            <div className="p-2 w-full max-w-3xl flex flex-col text-center justify-center items-center gap-12 mt-12">
                <h1 className="text-5xl font-bold font-serif animate-fade-in">
                    O seu mapa para o conhecimento.
                </h1>
                <p className="text-[#4b5563] text-xl animate-fade-in animation-delay-200">
                    Orienta usa inteligência artificial para criar{" "}
                    <em>planos de estudo personalizados</em>, transformando a
                    maneira como você aprende qualquer tópico, no{" "}
                    <strong>seu ritmo</strong>.
                </p>
                <Link href="/login">
                    <Button
                        className="font-bold max-w-xs animate-fade-in animation-delay-200"
                        size="lg"
                    >
                        Criar meu plano de estudo gratuito
                    </Button>
                </Link>
            </div>
        </div>
    );
}
