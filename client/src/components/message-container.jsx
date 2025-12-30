"use client";

import { useMessage } from "@/hooks/useMessage";
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
        <div className="absolute flex flex-col gap-5 top-20 right-5">
            {displayedMessages.map((message) => (
                <ToastMessage
                    key={message.id}
                    type={message.type}
                    message={message.text}
                    onClose={() => handleClose(message.id)}
                />
            ))}
        </div>
    );
}
