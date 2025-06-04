import { useState } from "react";
import {
  Box,
  Flex,
  Text,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Image,
  HStack,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  Badge,
  Table,
  Tbody,
  Tr,
  Td,
  useToast,
} from "@chakra-ui/react";
import { MoreVertical, Trash2, Info, Download, Eye } from "lucide-react";
import { FileData } from "../../types/file";
import { format } from "date-fns";
import API from "../../api/api";

interface FileCardProps {
  file: FileData;
  onDelete: (fileId: string) => void;
  viewType: "grid" | "list";
}

const FileCard = ({ file, onDelete, viewType }: FileCardProps) => {
  const {
    isOpen: isDetailsOpen,
    onOpen: onDetailsOpen,
    onClose: onDetailsClose,
  } = useDisclosure();
  const {
    isOpen: isViewerOpen,
    onOpen: onViewerOpen,
    onClose: onViewerClose,
  } = useDisclosure();
  const toast = useToast();
  const [isDownloading, setIsDownloading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + " B";
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    else return (bytes / 1048576).toFixed(1) + " MB";
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      const api = API.getInstance();
      const blob = await api.downloadDocument(file.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      toast({
        title: "Download failed",
        description:
          error instanceof Error ? error.message : "Failed to download file",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsDownloading(false);
    }
  };

  const handleView = async () => {
    try {
      const api = API.getInstance();
      const blob = await api.downloadDocument(file.id);
      const url = window.URL.createObjectURL(blob);
      setPdfUrl(url);
      onViewerOpen();
    } catch (error) {
      toast({
        title: "Failed to load PDF",
        description:
          error instanceof Error ? error.message : "Failed to load PDF file",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  // Cleanup URL when viewer modal closes
  const handleViewerClose = () => {
    if (pdfUrl) {
      window.URL.revokeObjectURL(pdfUrl);
      setPdfUrl(null);
    }
    onViewerClose();
  };

  const formattedDate = format(new Date(file.uploadDate), "MMM d, yyyy");

  // PDF thumbnail placeholder
  const pdfThumbnail =
    "https://images.pexels.com/photos/46274/pexels-photo-46274.jpeg?auto=compress&cs=tinysrgb&w=300";

  if (viewType === "grid") {
    return (
      <>
        <Box position="relative">
          <Box
            borderWidth="1px"
            borderRadius="lg"
            bg="white"
            transition="transform 0.2s, box-shadow 0.2s"
            _hover={{
              transform: "translateY(-2px)",
              boxShadow: "md",
            }}
          >
            <Badge
              position="absolute"
              top={2}
              left={2}
              colorScheme="red"
              fontSize="xs"
            >
              PDF
            </Badge>
            <Box p={4} mt={3}>
              <Flex justify="space-between" align="start">
                <Box>
                  <Text fontWeight="semibold" isTruncated title={file.name}>
                    {file.name}
                  </Text>
                  <HStack fontSize="sm" color="gray.500" mt={1} spacing={1}>
                    <Text>{formatFileSize(file.size)}</Text>
                    <Text>•</Text>
                    <Text>{formattedDate}</Text>
                  </HStack>
                </Box>

                <Menu placement="bottom-end" strategy="fixed">
                  <MenuButton
                    as={IconButton}
                    aria-label="Options"
                    icon={<MoreVertical size={16} />}
                    variant="ghost"
                    size="sm"
                  />
                  <MenuList zIndex={1000}>
                    <MenuItem icon={<Eye size={16} />} onClick={handleView}>
                      View PDF
                    </MenuItem>
                    <MenuItem icon={<Info size={16} />} onClick={onDetailsOpen}>
                      View details
                    </MenuItem>
                    <MenuItem
                      icon={<Download size={16} />}
                      onClick={handleDownload}
                      isDisabled={isDownloading}
                    >
                      {isDownloading ? "Downloading..." : "Download"}
                    </MenuItem>
                    <MenuItem
                      icon={<Trash2 size={16} />}
                      onClick={() => onDelete(file.id)}
                      color="red.500"
                    >
                      Delete
                    </MenuItem>
                  </MenuList>
                </Menu>
              </Flex>
            </Box>
          </Box>
        </Box>

        {/* Details Modal */}
        <Modal isOpen={isDetailsOpen} onClose={onDetailsClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>File Details</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Table variant="simple">
                <Tbody>
                  <Tr>
                    <Td fontWeight="medium">Name</Td>
                    <Td>{file.name}</Td>
                  </Tr>
                  <Tr>
                    <Td fontWeight="medium">Size</Td>
                    <Td>{formatFileSize(file.size)}</Td>
                  </Tr>
                  <Tr>
                    <Td fontWeight="medium">Type</Td>
                    <Td>PDF Document</Td>
                  </Tr>
                  <Tr>
                    <Td fontWeight="medium">Uploaded</Td>
                    <Td>{format(new Date(file.uploadDate), "PPP")}</Td>
                  </Tr>
                </Tbody>
              </Table>
            </ModalBody>
            <ModalFooter>
              <Button colorScheme="brand" mr={3} onClick={onDetailsClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>

        {/* PDF Viewer Modal */}
        <Modal isOpen={isViewerOpen} onClose={handleViewerClose} size="6xl">
          <ModalOverlay />
          <ModalContent maxW="90vw" h="90vh">
            <ModalHeader>{file.name}</ModalHeader>
            <ModalCloseButton />
            <ModalBody p={0} h="100%">
              {pdfUrl && (
                <iframe
                  src={pdfUrl}
                  style={{
                    width: "100%",
                    height: "100%",
                    border: "none",
                  }}
                  title={file.name}
                />
              )}
            </ModalBody>
          </ModalContent>
        </Modal>
      </>
    );
  }

  // List view
  return (
    <>
      <Flex
        align="center"
        p={3}
        borderWidth="1px"
        borderRadius="md"
        bg="white"
        transition="background 0.2s"
        _hover={{
          bg: "gray.50",
        }}
      >
        <Box
          w="40px"
          h="40px"
          bg="brand.50"
          borderRadius="md"
          display="flex"
          alignItems="center"
          justifyContent="center"
          color="brand.500"
          mr={4}
          cursor="pointer"
          onClick={handleView}
        >
          PDF
        </Box>

        <Box flex="1" minW="0">
          <Text fontWeight="medium" isTruncated>
            {file.name}
          </Text>
          <HStack fontSize="sm" color="gray.500" spacing={1}>
            <Text>{formatFileSize(file.size)}</Text>
            <Text>•</Text>
            <Text>{formattedDate}</Text>
          </HStack>
        </Box>

        <Menu>
          <MenuButton
            as={IconButton}
            aria-label="Options"
            icon={<MoreVertical size={16} />}
            variant="ghost"
            size="sm"
          />
          <MenuList>
            <MenuItem icon={<Eye size={16} />} onClick={handleView}>
              View PDF
            </MenuItem>
            <MenuItem icon={<Info size={16} />} onClick={onDetailsOpen}>
              View details
            </MenuItem>
            <MenuItem
              icon={<Download size={16} />}
              onClick={handleDownload}
              isDisabled={isDownloading}
            >
              {isDownloading ? "Downloading..." : "Download"}
            </MenuItem>
            <MenuItem
              icon={<Trash2 size={16} />}
              onClick={() => onDelete(file.id)}
              color="red.500"
            >
              Delete
            </MenuItem>
          </MenuList>
        </Menu>
      </Flex>

      {/* Details Modal */}
      <Modal isOpen={isDetailsOpen} onClose={onDetailsClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>File Details</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Table variant="simple">
              <Tbody>
                <Tr>
                  <Td fontWeight="medium">Name</Td>
                  <Td>{file.name}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium">Size</Td>
                  <Td>{formatFileSize(file.size)}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium">Type</Td>
                  <Td>PDF Document</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium">Uploaded</Td>
                  <Td>{format(new Date(file.uploadDate), "PPP")}</Td>
                </Tr>
              </Tbody>
            </Table>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="brand" mr={3} onClick={onDetailsClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* PDF Viewer Modal */}
      <Modal isOpen={isViewerOpen} onClose={handleViewerClose} size="6xl">
        <ModalOverlay />
        <ModalContent maxW="90vw" h="90vh">
          <ModalHeader>{file.name}</ModalHeader>
          <ModalCloseButton />
          <ModalBody p={0} h="100%">
            {pdfUrl && (
              <iframe
                src={pdfUrl}
                style={{
                  width: "100%",
                  height: "100%",
                  border: "none",
                }}
                title={file.name}
              />
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default FileCard;
