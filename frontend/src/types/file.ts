export interface FileData {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadDate: Date;
}

export interface FileContextType {
  files: FileData[];
  isUploading: boolean;
  uploadProgress: number;
  uploadFile: (file: File) => Promise<string>;
  removeFile: (fileId: string) => void;
  getFile: (fileId: string) => FileData | undefined;
}
