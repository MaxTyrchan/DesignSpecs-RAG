import { createContext, useContext, useState, ReactNode } from 'react';
import { FileData, FileContextType } from '../types/file';

const FileContext = createContext<FileContextType | undefined>(undefined);

export const FileProvider = ({ children }: { children: ReactNode }) => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const uploadFile = async (file: File) => {
    if (file.size > 10 * 1024 * 1024) {
      throw new Error('File size exceeds 10MB limit');
    }

    if (file.type !== 'application/pdf') {
      throw new Error('Only PDF files are supported');
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload with progress
      const totalSteps = 10;
      for (let i = 1; i <= totalSteps; i++) {
        await new Promise((resolve) => setTimeout(resolve, 200));
        setUploadProgress((i / totalSteps) * 100);
      }

      // Create file record
      const newFile: FileData = {
        id: Date.now().toString(),
        name: file.name,
        size: file.size,
        type: file.type,
        uploadDate: new Date(),
        url: URL.createObjectURL(file),
      };

      setFiles((prevFiles) => [...prevFiles, newFile]);
      return newFile.id;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const deleteFile = (fileId: string) => {
    setFiles((prevFiles) => prevFiles.filter((file) => file.id !== fileId));
  };

  const getFile = (fileId: string) => {
    return files.find((file) => file.id === fileId);
  };

  return (
    <FileContext.Provider
      value={{
        files,
        isUploading,
        uploadProgress,
        uploadFile,
        deleteFile,
        getFile,
      }}
    >
      {children}
    </FileContext.Provider>
  );
};

export const useFiles = () => {
  const context = useContext(FileContext);
  if (context === undefined) {
    throw new Error('useFiles must be used within a FileProvider');
  }
  return context;
};