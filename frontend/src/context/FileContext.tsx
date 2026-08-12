import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { FileData, FileContextType } from "../types/file";
import API from "../api/api";

const FileContext = createContext<FileContextType | undefined>(undefined);

export const FileProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [files, setFiles] = useState<FileData[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    const loadFiles = async () => {
      const api = API.getInstance();
      const fileList = await api.listFiles();
      setFiles(
        fileList.map((file) => ({
          ...file,
          uploadDate: new Date(file.uploadDate),
        }))
      );
    };

    loadFiles();
  }, []);

  const uploadFile = async (file: File) => {
    if (file.size > 10 * 1024 * 1024) {
      throw new Error("File size exceeds 10MB limit");
    }

    if (file.type !== "application/pdf") {
      throw new Error("Only PDF files are supported");
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Initialize API client
      const api = API.getInstance();

      // Upload file using API with progress tracking
      const result = await api.uploadDocument(file, (progress) => {
        setUploadProgress(progress);
      });

      if (!result.success) {
        throw new Error(result.message);
      }

      // Create file record after successful upload
      const newFile: FileData = {
        id: result.fileId,
        name: file.name,
        size: file.size,
        type: file.type,
        uploadDate: new Date(),
      };

      setFiles((prevFiles: FileData[]) => [...prevFiles, newFile]);
      return newFile.id;
    } catch (error) {
      console.error("Error uploading file:", error);
      throw error;
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const removeFile = (fileId: string) => {
    setFiles((prevFiles: FileData[]) =>
      prevFiles.filter((file: FileData) => file.id !== fileId)
    );
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
        removeFile,
        getFile,
      }}
    >
      {children}
    </FileContext.Provider>
  );
};

export const useFile = () => {
  const context = useContext(FileContext);
  if (context === undefined) {
    throw new Error("useFile must be used within a FileProvider");
  }
  return context;
};
