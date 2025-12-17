"use client";

import { useMessage } from "@/contexts/MessageContext";
import { ToastMessage } from "./toast-message";
import { useState, useEffect } from "react";

export function MessageContainer() {
    const { messages, clear } = useMessage();
    const [displayedMessages, setDisplayedMessages] = useState([]);

    useEffect(() => {
        if (messages.length > 0) {
            const newMessages = messages.map((message, index) => ({
                ...message,
                id: `${Date.now()}-${index}`,
            }));
            setDisplayedMessages(newMessages);

            // Auto-remove message after 5 seconds
            const timer = setTimeout(() => {
                setDisplayedMessages([]);
                clear();
            }, 5000);

            return () => clearTimeout(timer);
        }
    }, [messages, clear]);

    const handleClose = (id) => {
        setDisplayedMessages((prev) =>
            prev.filter((message) => message.id !== id),
        );
        clear();
    };

    return (
        <>
            {displayedMessages.map((message) => (
                <ToastMessage
                    key={message.id}
                    type={message.type}
                    message={message.text}
                    onClose={() => handleClose(message.id)}
                />
            ))}
        </>
    );
}
