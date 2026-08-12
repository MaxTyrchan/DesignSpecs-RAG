import React, { createContext, useContext, useState, useCallback } from "react";
import { Message, ContentItem } from "../types/chat";
import API, { QAResponse } from "../api/api";

// Helper function to generate metadata summary from context
const generateMetadataSummary = (context: QAResponse["context"]) => {
  const allItems = [...context.texts, ...context.tables, ...context.images];
  const uniqueDocuments = new Set<string>();
  const pagesReferenced = new Set<number>();
  const contentTypes = new Set<string>();

  allItems.forEach((item: ContentItem) => {
    // Extract unique documents
    const filename = item.metadata.basechunk_meta?.origin?.filename;
    if (filename) {
      uniqueDocuments.add(filename);
    }

    // Extract page numbers
    const docItems = item.metadata.basechunk_meta?.doc_items;
    if (docItems) {
      docItems.forEach((docItem) => {
        if (docItem.prov) {
          docItem.prov.forEach((prov) => {
            if (prov.page_no) {
              pagesReferenced.add(prov.page_no);
            }
          });
        }
      });
    }

    // Extract content types
    contentTypes.add(item.metadata.content_type);
  });

  return {
    total_chunks: allItems.length,
    unique_documents: Array.from(uniqueDocuments),
    pages_referenced: Array.from(pagesReferenced).sort((a, b) => a - b),
    content_types: Array.from(contentTypes),
  };
};

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

        // Get response from API - use hybrid if enabled
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
          retrievalStats: response.retrieval_stats,
          metadataSummary: generateMetadataSummary(response.context),
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
        removeFile
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
