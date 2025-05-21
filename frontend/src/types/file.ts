export interface FileData {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadDate: Date;
  url: string;
}

export interface FileContextType {
  files: FileData[];
  isUploading: boolean;
  uploadProgress: number;
  uploadFile: (file: File) => Promise<string>;
  deleteFile: (fileId: string) => void;
  getFile: (fileId: string) => FileData | undefined;
}