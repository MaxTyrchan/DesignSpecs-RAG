import {
  Container,
  Box,
  Heading,
  Text,
  useToast,
  Button,
  Flex,
  Spinner,
} from "@chakra-ui/react";
import { Upload } from "lucide-react";
import FileGrid from "../components/Files/FileGrid";
import { useFile } from "../context/FileContext";
import API from "../api/api";

const FilesPage = () => {
  const { files, removeFile: deleteFile, isUploading } = useFile();
  const toast = useToast();
  const api = API.getInstance();

  const handleDelete = (fileId: string) => {
    deleteFile(fileId);

    toast({
      title: "File deleted",
      description: "The file has been successfully deleted",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  const handleAttachClick = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const data = new FormData();
    if (!event.target.files?.length) return;
    data.append("file", event.target.files[0]);
    try {
      const response = await api.uploadDocument(event.target.files[0]);
      return response;
    } catch (err) {
      console.error("Error uploading document:", err);
      return { success: false };
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Box mb={8}>
        <Heading as="h1" size="xl" mb={2}>
          Documents Library
        </Heading>
        <Text color="gray.600">
          Manage your uploaded PDF documents for chat and analysis
        </Text>
      </Box>

      <Flex
        justify="space-between"
        align="center"
        mb={6}
        direction={{ base: "column", md: "row" }}
        gap={4}
      >
        <Box>
          <Text fontWeight="medium">
            {files.length} {files.length === 1 ? "document" : "documents"} in
            your library
          </Text>
          <Text fontSize="sm" color="gray.500">
            PDF files are automatically processed for use in chat
          </Text>
        </Box>

        <Button
          leftIcon={<Upload size={16} />}
          colorScheme="brand"
          isLoading={isUploading}
          loadingText="Uploading..."
          position="relative"
          overflow="hidden"
        >
          Upload Documents
          <input
            type="file"
            id="file-upload"
            name="file-upload"
            accept=".pdf"
            multiple
            onChange={handleAttachClick}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              opacity: 0,
              cursor: "pointer",
              zIndex: 1,
            }}
          />
        </Button>
      </Flex>

      {isUploading && (
        <Flex justify="center" my={8}>
          <Spinner color="brand.500" size="xl" />
        </Flex>
      )}

      {!isUploading && files.length === 0 ? (
        <Box
          p={10}
          borderWidth="2px"
          borderStyle="dashed"
          borderColor="gray.200"
          borderRadius="lg"
          textAlign="center"
        >
          <Text fontSize="lg" fontWeight="medium" mb={4}>
            No documents in your library
          </Text>
          <Text color="gray.600" mb={6}>
            Upload PDF documents from the chat interface to see them here
          </Text>
          <Button
            colorScheme="brand"
            size="md"
            onClick={() => {
              window.location.href = "/";
            }}
          >
            Go to Chat
          </Button>
        </Box>
      ) : (
        <FileGrid files={files} onDelete={handleDelete} />
      )}
    </Container>
  );
};

export default FilesPage;
