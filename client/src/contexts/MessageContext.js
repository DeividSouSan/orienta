"use client";

import React, { createContext, useState } from "react";

const MessageContext = createContext({
    messages: [],
    addMessage: () => {},
    successMessage: () => {},
    errorMessage: () => {},
    clear: () => {},
});

export const MessageProvider = ({ children }) => {
    const [messages, setMessages] = useState([]);

    const addMessage = (message) => {
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const successMessage = (text) => {
        setMessages((prevMessages) => [
            ...prevMessages,
            { type: "success", text },
        ]);
    };
    const errorMessage = (text) => {
        setMessages((prevMessages) => [
            ...prevMessages,
            { type: "error", text },
        ]);
    };

    const clear = () => {
        setMessages([]);
    };

    const value = {
        messages,
        addMessage,
        successMessage,
        errorMessage,
        clear,
    };

    return (
        <MessageContext.Provider value={value}>
            {children}
        </MessageContext.Provider>
    );
};

export { MessageContext };
