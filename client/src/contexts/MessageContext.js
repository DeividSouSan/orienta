"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

const MessageContext = createContext({
    messages: [],
    addMessage: () => {},
    clear: () => {},
});

export const MessageProvider = ({ children }) => {
    const [messages, setMessages] = useState([]);

    const addMessage = (message) => {
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const clear = () => {
        setMessages([]);
    };

    const value = {
        messages,
        addMessage,
        clear,
    };

    return (
        <MessageContext.Provider value={value}>
            {children}
        </MessageContext.Provider>
    );
};

export const useMessage = () => useContext(MessageContext);
