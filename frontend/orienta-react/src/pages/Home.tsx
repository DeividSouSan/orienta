import GuestGuard from "@/components/guest-guard";
import { Button } from "@/components/ui/button";
import { Link } from "react-router";
import { BookOpen, Sparkles, Target } from "lucide-react";

export default function HomePage() {
  return (
    <GuestGuard>
      <div className="flex flex-col items-center px-6">
        {/* Hero */}
        <section className="flex flex-col items-center text-center pt-24 pb-20 max-w-2xl">
          <h1 className="font-serif text-4xl md:text-5xl font-bold tracking-tight animate-fade-in">
            Aprenda qualquer coisa,
            <br />
            <span className="text-muted-foreground">no seu ritmo.</span>
          </h1>

          <p className="mt-6 text-muted-foreground text-lg leading-relaxed max-w-lg animate-fade-in animation-delay-200">
            Guias de estudo personalizados com inteligência artificial. Diga o
            que quer aprender — a gente te orienta.
          </p>

          <div className="flex gap-3 mt-10 animate-fade-in animation-delay-400">
            <Link to="/register">
              <Button size="lg">Começar gratuitamente</Button>
            </Link>
            <Link to="/login">
              <Button variant="outline" size="lg">
                Entrar
              </Button>
            </Link>
          </div>
        </section>

        {/* Divisor sutil */}
        <div className="w-12 h-px bg-border" />

        {/* Features */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-3xl py-20 animate-fade-in animation-delay-600">
          <div className="flex flex-col items-center text-center gap-3">
            <Sparkles className="text-muted-foreground" size={22} />
            <h3 className="font-serif font-semibold">Gerado por IA</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Planos de estudo criados sob medida para o seu objetivo e nível de
              conhecimento.
            </p>
          </div>

          <div className="flex flex-col items-center text-center gap-3">
            <Target className="text-muted-foreground" size={22} />
            <h3 className="font-serif font-semibold">Foco no essencial</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Sem distrações. Um caminho claro do início ao domínio do assunto.
            </p>
          </div>

          <div className="flex flex-col items-center text-center gap-3">
            <BookOpen className="text-muted-foreground" size={22} />
            <h3 className="font-serif font-semibold">
              Acompanhe seu progresso
            </h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Marque tópicos concluídos e veja sua evolução dia a dia.
            </p>
          </div>
        </section>
      </div>
    </GuestGuard>
  );
}
