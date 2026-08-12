// Enhanced metadata structure for BaseChunk information
export interface BasechunkMetadata {
  schema_name?: string;
  version?: string;
  doc_items?: Array<{
    self_ref?: string;
    parent?: { $ref: string };
    children?: Array<{ $ref: string }>;
    content_layer?: string;
    label?: string;
    prov?: Array<{
      page_no?: number;
      bbox?: {
        l: number;
        t: number;
        r: number;
        b: number;
        coord_origin?: string;
      };
      charspan?: [number, number];
    }>;
  }>;
  headings?: string[];
  origin?: {
    mimetype?: string;
    binary_hash?: number;
    filename?: string;
  };
}

// Enhanced content item with metadata
export interface ContentItem {
  content: string;
  metadata: {
    chunk_id?: string;
    content_type: string;
    source?: string;
    basechunk_meta?: BasechunkMetadata;
    // Additional metadata fields
    doc_id?: string;
    text_item?: string | number;
  };
}

export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant" | "system";
  timestamp: Date;
  isError?: boolean;
  structuredContent?: {
    texts: ContentItem[];
    tables: ContentItem[];
    images: ContentItem[];
  };
  metadataSummary?: {
    total_chunks: number;
    unique_documents: string[];
    pages_referenced: number[];
    content_types: string[];
  };
  retrievalStats?: {
    semantic: number;
    bm25: number;
    both: number;
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
