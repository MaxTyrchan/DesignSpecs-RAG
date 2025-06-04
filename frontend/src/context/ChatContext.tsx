import { createContext, useContext, useState, ReactNode } from "react";
import { Message, ChatContextType } from "../types/chat";
import API from "../api/api";

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeFiles, setActiveFiles] = useState<string[]>([]);
  const api = API.getInstance();

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      const response = await api.askQuestion(content);

      // Create AI response message
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.answer,
        timestamp: new Date(),
      };

      setMessages((prevMessages) => [...prevMessages, aiResponse]);
    } catch (error) {
      console.error("Error sending message:", error);
      // Add error message
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: (Date.now() + 1).toString(),
          role: "system",
          content:
            error instanceof Error
              ? error.message
              : "An error occurred while processing your request.",
          timestamp: new Date(),
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setActiveFiles([]);
  };

  const attachFile = (fileId: string) => {
    if (!activeFiles.includes(fileId)) {
      setActiveFiles((prev) => [...prev, fileId]);
    }
  };

  const removeFile = (fileId: string) => {
    setActiveFiles((prev) => prev.filter((id) => id !== fileId));
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        isLoading,
        activeFiles,
        sendMessage,
        clearChat,
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
