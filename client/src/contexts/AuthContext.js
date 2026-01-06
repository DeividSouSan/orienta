"use client";

import React, { createContext, useState, useEffect } from "react";

const AuthContext = createContext({
    isAuthenticated: false,
    currentUser: null,
    isLoading: true,
    login: () => { },
    logout: () => { },
});

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const login = (userData) => {
        setCurrentUser(userData);
        setIsAuthenticated(true);
    };

    const logout = () => {
        setCurrentUser(null);
        setIsAuthenticated(false);
    };

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch("/api/v1/user", {
                    method: "GET",
                    credentials: "include",
                });

                if (response.ok) {
                    const responseBody = await response.json();
                    login(responseBody.data);
                } else {
                    await fetch("/api/v1/sessions", {
                        method: "DELETE",
                    });
                    logout();
                }
            } catch (error) {
                await fetch("/api/v1/sessions", {
                    method: "DELETE",
                });
                logout();
            } finally {
                setIsLoading(false);
            }
        };

        fetchUser();
    }, []);

    const value = {
        isAuthenticated,
        currentUser,
        isLoading,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};

export { AuthContext };
