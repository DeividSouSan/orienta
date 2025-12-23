import { MessageContext } from "@/contexts/MessageContext";
import { useContext } from "react";

export const useMessage = () => useContext(MessageContext);
