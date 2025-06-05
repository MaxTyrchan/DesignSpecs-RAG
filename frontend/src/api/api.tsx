import { EvaluationMetric, QueryResponsePair } from "../types/evaluation";

interface UploadResponse {
  message: string;
  filename: string;
  fileId: string;
}

interface FileResponse {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadDate: number;
}

export interface QAResponse {
  answer: string;
  context: {
    texts: string[];
    tables: string[];
    images: string[];
  };
}

export interface EvaluationResponse {
  metrics: EvaluationMetric[];
  pairs: QueryResponsePair[];
}

export default class API {
  /** Singleton instance of the API class. */
  private static instance: API | null = null;
  private readonly baseURL = "http://localhost:8000/api";

  private constructor() {}

  static getInstance(): API {
    if (!API.instance) {
      API.instance = new API();
    }
    return API.instance;
  }

  private async fetchWithError<T>(url: string, init?: RequestInit): Promise<T> {
    const response = await fetch(url, {
      ...init,
      headers: {
        ...init?.headers,
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        errorData?.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }

  async listFiles(): Promise<FileResponse[]> {
    try {
      const files = await this.fetchWithError<FileResponse[]>(
        `${this.baseURL}/files`
      );
      return files.map((file) => ({
        ...file,
        uploadDate: file.uploadDate * 1000, // Convert from Unix timestamp to JS timestamp
      }));
    } catch (error) {
      console.error("Error listing files:", error);
      return [];
    }
  }

  async uploadDocument(
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<{ success: boolean; message: string; fileId: string }> {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const xhr = new XMLHttpRequest();
      const promise = new Promise<UploadResponse>((resolve, reject) => {
        xhr.upload.addEventListener("progress", (event) => {
          if (event.lengthComputable && onProgress) {
            const progress = Math.round((event.loaded * 100) / event.total);
            onProgress(progress);
          }
        });

        xhr.addEventListener("load", () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(JSON.parse(xhr.responseText));
          } else {
            reject(new Error(`HTTP error! status: ${xhr.status}`));
          }
        });

        xhr.addEventListener("error", () => {
          reject(new Error("Network error occurred"));
        });

        xhr.addEventListener("abort", () => {
          reject(new Error("Upload aborted"));
        });
      });

      xhr.open("POST", `${this.baseURL}/upload`);
      xhr.send(formData);

      const response = await promise;
      return {
        success: true,
        message: response.message,
        fileId: response.fileId,
      };
    } catch (error) {
      console.error("Error uploading document:", error);
      return {
        success: false,
        message:
          error instanceof Error ? error.message : "Failed to upload document",
        fileId: "",
      };
    }
  }

  async downloadDocument(fileId: string): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/download/${fileId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.blob();
  }

  async askQuestion(question: string): Promise<QAResponse> {
    try {
      return await this.fetchWithError(`${this.baseURL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
    } catch (error) {
      console.error("Error asking question:", error);
      throw error;
    }
  }

  async getEvaluationData(): Promise<EvaluationResponse> {
    try {
      return await this.fetchWithError(`${this.baseURL}/evaluation`);
    } catch (error) {
      console.error("Error fetching evaluation data:", error);
      throw error;
    }
  }

  async healthCheck(): Promise<{ status: string }> {
    try {
      return await this.fetchWithError(`${this.baseURL}/health`);
    } catch (error) {
      console.error("Error checking health:", error);
      throw error;
    }
  }
}
