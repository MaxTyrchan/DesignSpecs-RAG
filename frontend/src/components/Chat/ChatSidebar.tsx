import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  VStack,
  HStack,
  Text,
  Button,
  useToast,
  Box,
  Progress,
  Badge,
} from "@chakra-ui/react";
import { useDropzone } from "react-dropzone";
import { FileText } from "lucide-react";
import { useFile } from "../../context/FileContext";
import { useChat } from "../../context/ChatContext";
import FileAttachment from "./FileAttachment";

interface ChatSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatSidebar = ({ isOpen, onClose }: ChatSidebarProps) => {
  const { uploadFile, isUploading, uploadProgress } = useFile();
  const { activeFiles, attachFile, removeFile } = useChat();
  const { files } = useFile();
  const toast = useToast();

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];

    try {
      if (file.size > 10 * 1024 * 1024) {
        throw new Error("File size exceeds 10MB limit");
      }

      if (file.type !== "application/pdf") {
        throw new Error("Only PDF files are supported");
      }

      const fileId = await uploadFile(file);
      attachFile(fileId);

      toast({
        title: "File uploaded",
        description: `${file.name} has been attached to the chat`,
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Upload failed",
        description:
          error instanceof Error ? error.message : "An error occurred",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    multiple: false,
    disabled: isUploading,
  });

  const attachedFiles = files.filter((file) => activeFiles.includes(file.id));

  return (
    <Drawer isOpen={isOpen} placement="right" onClose={onClose} size="md">
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />
        <DrawerHeader borderBottomWidth="1px">Attach Files</DrawerHeader>

        <DrawerBody>
          <VStack spacing={4} align="stretch">
            <Box
              {...getRootProps()}
              p={6}
              border="2px dashed"
              borderColor={isDragActive ? "brand.500" : "gray.300"}
              borderRadius="md"
              bg={isDragActive ? "brand.50" : "gray.50"}
              textAlign="center"
              transition="all 0.2s"
              _hover={{
                borderColor: "brand.400",
                bg: "brand.50",
              }}
              cursor="pointer"
            >
              <input {...getInputProps()} />
              <FileText
                size={36}
                style={{ margin: "0 auto 12px" }}
                color="#6b7280"
              />
              <Text fontWeight="medium">
                {isDragActive
                  ? "Drop the file here"
                  : "Drag & drop a PDF file here"}
              </Text>
              <Text fontSize="sm" color="gray.500" mt={1}>
                or click to select a file
              </Text>
              <Text fontSize="xs" color="gray.500" mt={2}>
                Maximum file size: 10MB
              </Text>
            </Box>

            {isUploading && (
              <Box>
                <Text fontSize="sm" mb={1}>
                  Uploading...
                </Text>
                <Progress
                  value={uploadProgress}
                  size="sm"
                  colorScheme="brand"
                  borderRadius="full"
                  isAnimated
                />
              </Box>
            )}

            {attachedFiles.length > 0 && (
              <Box>
                <HStack justify="space-between" mb={2}>
                  <Text fontWeight="medium">Attached Files</Text>
                  <Badge colorScheme="brand">{attachedFiles.length}</Badge>
                </HStack>
                <VStack spacing={2} align="stretch">
                  {attachedFiles.map((file) => (
                    <FileAttachment
                      key={file.id}
                      file={file}
                      onRemove={() => removeFile(file.id)}
                    />
                  ))}
                </VStack>
              </Box>
            )}
          </VStack>
        </DrawerBody>

        <DrawerFooter borderTopWidth="1px">
          <Button variant="outline" mr={3} onClick={onClose}>
            Close
          </Button>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
};

export default ChatSidebar;
