export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant" | "system";
  timestamp: Date;
  isError?: boolean;
  structuredContent?: {
    texts: string[];
    tables: string[];
    images: string[];
  };
}

export interface ChatContextType {
  messages: Message[];
  isLoading: boolean;
  activeFiles: string[];
  sendMessage: (content: string) => Promise<void>;
  clearChat: () => void;
  attachFile: (fileId: string) => void;
  removeFile: (fileId: string) => void;
}
