export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  isError?: boolean;
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