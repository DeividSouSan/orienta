// src/components/Layout.tsx
import { Outlet } from "react-router";
import Header from "@/components/header"; // Importe seus componentes
import { MessageProvider } from "./hooks/useMessage";
import { AuthProvider } from "./hooks/useAuth";
import { MessageContainer } from "./components/message-container";

export function Layout() {
  return (
    <div className="min-h-screen flex flex-col font-sans antialiased">
      <MessageProvider>
        <MessageContainer />
        <AuthProvider>
          <Header />

          <main className="flex-1">
            <Outlet />
          </main>
        </AuthProvider>
      </MessageProvider>
    </div>
  );
}
