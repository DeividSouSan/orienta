"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext({
    isAuthenticated: false,
    user: null,
    loading: true,
    login: () => { },
    logout: () => { },
});

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const login = (userData) => {
        console.log("Dentro do Login: ", userData);
        setUser(userData);
        setIsAuthenticated(true);
    };

    const logout = () => {
        setUser(null);
        setIsAuthenticated(false);
    };

    useEffect(() => {
        console.log("AuthContext: verificando se o usuário está logado.");
        const fetchUser = async () => {
            try {
                const response = await fetch("/api/v1/user", {
                    method: "GET",
                    credentials: "include",
                });

                if (response.ok) {
                    console.log("Usuário foi logado com sucesso.");
                    const userData = await response.json();
                    console.log("Dados do usuário: ", userData);
                    login(userData);
                } else {
                    console.log(
                        "Erro na resposta da API, usuário não foi logado.",
                    );

                    await fetch("/api/v1/sessions", {
                        method: "DELETE",
                        credentials: "include",
                    });
                    logout();
                }
            } catch (error) {
                console.error("Erro ao buscar dados do usuário:", error);

                await fetch("/api/v1/sessions", {
                    method: "DELETE",
                    credentials: "include",
                });
                logout();
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, []);

    const value = {
        isAuthenticated,
        user,
        loading,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
