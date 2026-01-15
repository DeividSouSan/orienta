import React, { createContext, ReactNode, useContext, useState } from "react";

type Message = {
  type: "success" | "error";
  text: string;
};

interface MessageContextValue {
  messages: Message[];
  addMessage: (message: Message) => void;
  successMessage: (text: string) => void;
  errorMessage: (text: string) => void;
  clear: () => void;
}

const MessageContext = createContext<MessageContextValue | undefined>(
  undefined,
);

export const MessageProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessage = (message: Message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const successMessage = (text: string): void => {
    setMessages((prevMessages) => [...prevMessages, { type: "success", text }]);
  };

  const errorMessage = (text: string) => {
    setMessages((prevMessages) => [...prevMessages, { type: "error", text }]);
  };

  const clear = () => setMessages([]);

  const value = {
    messages,
    addMessage,
    successMessage,
    errorMessage,
    clear,
  };

  return (
    <MessageContext.Provider value={value}>{children}</MessageContext.Provider>
  );
};

export function useMessage(): MessageContextValue {
  return useContext(MessageContext)!;
}
