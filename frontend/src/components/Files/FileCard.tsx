import { useState } from 'react';
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
  Td
} from '@chakra-ui/react';
import { MoreVertical, Trash2, Info, Download } from 'lucide-react';
import { FileData } from '../../types/file';
import { format } from 'date-fns';

interface FileCardProps {
  file: FileData;
  onDelete: (fileId: string) => void;
  viewType: 'grid' | 'list';
}

const FileCard = ({ file, onDelete, viewType }: FileCardProps) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };
  
  const formattedDate = format(new Date(file.uploadDate), 'MMM d, yyyy');
  
  // PDF thumbnail placeholder
  const pdfThumbnail = "https://images.pexels.com/photos/46274/pexels-photo-46274.jpeg?auto=compress&cs=tinysrgb&w=300";
  
  if (viewType === 'grid') {
    return (
      <>
        <Box
          borderWidth="1px"
          borderRadius="lg"
          overflow="hidden"
          bg="white"
          transition="transform 0.2s, box-shadow 0.2s"
          _hover={{
            transform: 'translateY(-2px)',
            boxShadow: 'md',
          }}
        >
          <Box position="relative" h="150px" bg="gray.100">
            <Image
              src={pdfThumbnail}
              alt={file.name}
              objectFit="cover"
              w="100%"
              h="100%"
            />
            <Badge 
              position="absolute" 
              top={2} 
              right={2} 
              colorScheme="brand"
              fontSize="xs"
            >
              PDF
            </Badge>
          </Box>
          
          <Box p={4}>
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
              
              <Menu>
                <MenuButton
                  as={IconButton}
                  aria-label="Options"
                  icon={<MoreVertical size={16} />}
                  variant="ghost"
                  size="sm"
                />
                <MenuList>
                  <MenuItem icon={<Info size={16} />} onClick={onOpen}>
                    View details
                  </MenuItem>
                  <MenuItem icon={<Download size={16} />}>
                    Download
                  </MenuItem>
                  <MenuItem icon={<Trash2 size={16} />} onClick={() => onDelete(file.id)} color="red.500">
                    Delete
                  </MenuItem>
                </MenuList>
              </Menu>
            </Flex>
          </Box>
        </Box>
        
        <Modal isOpen={isOpen} onClose={onClose}>
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
                    <Td>{format(new Date(file.uploadDate), 'PPP')}</Td>
                  </Tr>
                </Tbody>
              </Table>
            </ModalBody>
            <ModalFooter>
              <Button colorScheme="brand" mr={3} onClick={onClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    );
  } else {
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
            bg: 'gray.50',
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
              <MenuItem icon={<Info size={16} />} onClick={onOpen}>
                View details
              </MenuItem>
              <MenuItem icon={<Download size={16} />}>
                Download
              </MenuItem>
              <MenuItem icon={<Trash2 size={16} />} onClick={() => onDelete(file.id)} color="red.500">
                Delete
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>
        
        <Modal isOpen={isOpen} onClose={onClose}>
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
                    <Td>{format(new Date(file.uploadDate), 'PPP')}</Td>
                  </Tr>
                </Tbody>
              </Table>
            </ModalBody>
            <ModalFooter>
              <Button colorScheme="brand" mr={3} onClick={onClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    );
  }
};

export default FileCard;