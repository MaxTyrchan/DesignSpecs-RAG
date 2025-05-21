import { HStack, Text, IconButton, Box, Tooltip } from '@chakra-ui/react';
import { X, FileText } from 'lucide-react';
import { FileData } from '../../types/file';
import { format } from 'date-fns';

interface FileAttachmentProps {
  file: FileData;
  onRemove: () => void;
}

const FileAttachment = ({ file, onRemove }: FileAttachmentProps) => {
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  return (
    <HStack
      p={2}
      bg="gray.50"
      borderRadius="md"
      borderWidth="1px"
      borderColor="gray.200"
      spacing={3}
      position="relative"
      overflow="hidden"
      _hover={{
        bg: 'gray.100',
      }}
      transition="all 0.2s"
    >
      <Box color="brand.500">
        <FileText size={20} />
      </Box>
      <Box flex="1" overflow="hidden">
        <Tooltip label={file.name} placement="top">
          <Text fontWeight="medium" fontSize="sm" noOfLines={1}>
            {file.name}
          </Text>
        </Tooltip>
        <HStack spacing={2} fontSize="xs" color="gray.500">
          <Text>{formatFileSize(file.size)}</Text>
          <Text>•</Text>
          <Text>{format(new Date(file.uploadDate), 'MMM d, yyyy')}</Text>
        </HStack>
      </Box>
      <IconButton
        aria-label="Remove file"
        icon={<X size={16} />}
        size="xs"
        variant="ghost"
        onClick={onRemove}
      />
    </HStack>
  );
};

export default FileAttachment;