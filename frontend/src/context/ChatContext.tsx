import React, { createContext, useContext, useState, useCallback } from "react";
import { Message } from "../types/chat";
import API from "../api/api";

interface ChatContextType {
  messages: Message[];
  isLoading: boolean;
  activeFiles: string[];
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  attachFile: (fileId: string) => void;
  removeFile: (fileId: string) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeFiles, setActiveFiles] = useState<string[]>([]);
  const api = API.getInstance();

  const attachFile = useCallback((fileId: string) => {
    setActiveFiles((prev) => [...prev, fileId]);
  }, []);

  const removeFile = useCallback((fileId: string) => {
    setActiveFiles((prev) => prev.filter((id) => id !== fileId));
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      try {
        // Add user message
        const userMessage: Message = {
          id: Date.now().toString(),
          content,
          role: "user",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        // Get response from API
        const response = await api.askQuestion(content);

        // Create assistant message with structured content
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response.answer,
          role: "assistant",
          timestamp: new Date(),
          structuredContent: {
            texts: response.context.texts || [],
            tables: response.context.tables || [],
            images: response.context.images || [],
          },
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error) {
        // Add error message
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: error instanceof Error ? error.message : "An error occurred",
          role: "system",
          timestamp: new Date(),
          isError: true,
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [api]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setActiveFiles([]);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        isLoading,
        activeFiles,
        sendMessage,
        clearMessages,
        attachFile,
        removeFile,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};
