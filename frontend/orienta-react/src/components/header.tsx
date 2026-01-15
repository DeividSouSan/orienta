import { Link } from "react-router";
import { useNavigate, useLocation } from "react-router";

import { useAuth } from "@/hooks/useAuth";

import {
  NavigationMenu,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuGroup,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";

import { LogOut, BookOpen, PlusCircle, Menu, UserRound } from "lucide-react";
import { Button } from "./ui/button";

const routes = [
  { href: "/login", label: "Entrar", delay: "200" },
  { href: "/register", label: "Cadastro", delay: "400" },
];

const authenticatedRoutes = [
  { href: "/dashboard/generate", label: "Gerar Guia", icon: PlusCircle },
  { href: "/dashboard/my-guides", label: "Meus Guias", icon: BookOpen },
];

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  const { isAuthenticated, currentUser, isLoading, logout } = useAuth();

  const pathname = location.pathname;
  const normalizedPathname =
    pathname === "/" ? "/" : pathname.replace(/\/$/, "");

  const isActive = (route) => normalizedPathname === route.href;

  const handleLogout = async () => {
    await fetch("/api/v1/sessions", {
      method: "DELETE",
      credentials: "include",
    });

    logout();
    navigate("/");
  };

  return (
    <header className="flex justify-between items-center top-0 z-50 w-full border bg-white shadow font-serif px-3 sm:px-4">
      <div className="flex items-center h-14 sm:h-16">
        <Link to={isAuthenticated ? "/dashboard" : "/"}>
          <span className="text-lg sm:text-xl">🧭 Orienta</span>
        </Link>
      </div>
      <nav>
        {isLoading ? null : (
          <div className="flex items-center gap-y-10">
            {isAuthenticated ? (
              <>
                <div title="Gerar Guia">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Link to="/dashboard/generate">
                        <PlusCircle size={18} />
                      </Link>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Gerar Guia</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
                <div className="gap-3 sm:gap-8 animate-fade-in">
                  <DropdownMenu>
                    <DropdownMenuTrigger className="px-3 focus:outline-0 sm:px-4 py-1 rounded-sm cursor-pointer text-sm sm:text-base">
                      <Menu />
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="m-2">
                      <DropdownMenuGroup>
                        <DropdownMenuItem className="cursor-pointer flex flex-row gap-2 items-center px-3 sm:px-4 py-2 rounded-xs data-[active=true]:bg-accent data-[active=true]:text-accent-foreground hover:bg-red-50 hover:text-red-600 transition-colors text-sm sm:text-base">
                          <UserRound size={18} />
                          <strong>{currentUser.username}</strong>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        {authenticatedRoutes.map((route) => {
                          const Icon = route.icon;
                          const active = isActive(route);
                          return (
                            <DropdownMenuItem key={route.href} asChild>
                              <Link
                                to={route.href}
                                className={`cursor-pointer flex flex-row gap-2 items-center px-3 sm:px-4 py-2 rounded-xs transition-colors text-sm sm:text-base ${
                                  active
                                    ? "bg-primary text-primary-foreground font-bold"
                                    : "data-[active=true]:bg-accent data-[active=true]:text-accent-foreground hover:bg-accent/50"
                                }`}
                              >
                                <Icon size={18} />
                                {route.label}
                              </Link>
                            </DropdownMenuItem>
                          );
                        })}
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          onClick={handleLogout}
                          className="cursor-pointer flex flex-row gap-2 items-center px-3 sm:px-4 py-2 rounded-xs data-[active=true]:bg-accent data-[active=true]:text-accent-foreground hover:bg-red-50 hover:text-red-600 transition-colors text-sm sm:text-base"
                        >
                          <LogOut size={18} />
                          Sair
                        </DropdownMenuItem>
                      </DropdownMenuGroup>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </>
            ) : (
              <NavigationMenu className="flex gap-2 sm:gap-4">
                {routes.map((route) => (
                  <NavigationMenuLink
                    key={route.href}
                    asChild
                    className={`animate-fade-in animation-delay-${route.delay}`}
                  >
                    <Link to={route.href}>
                      <Button
                        variant={
                          route.href === "/register" ? "default" : "outline"
                        }
                        size="sm"
                      >
                        {route.label}
                      </Button>
                    </Link>
                  </NavigationMenuLink>
                ))}
              </NavigationMenu>
            )}
          </div>
        )}
      </nav>
    </header>
  );
}
