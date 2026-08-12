import React from "react";
import {
  Box,
  Text,
  Badge,
  HStack,
  VStack,
  Wrap,
  WrapItem,
  Divider,
} from "@chakra-ui/react";
import { FileText, Hash, Users } from "lucide-react";
import { Message } from "../../types/chat";

interface MetadataSummaryProps {
  message: Message;
}

const MetadataSummary: React.FC<MetadataSummaryProps> = ({ message }) => {
  const { metadataSummary } = message;

  if (!metadataSummary || metadataSummary.total_chunks === 0) {
    return null;
  }

  return (
    <Box
      mt={4}
      p={3}
      bg="blue.50"
      borderRadius="md"
      border="1px solid"
      borderColor="blue.200"
    >
      <VStack align="start" spacing={3}>
        {/* Header */}
        <HStack spacing={2}>
          <FileText size={16} color="#3182CE" />
          <Text fontSize="sm" fontWeight="medium" color="blue.700">
            Source Summary
          </Text>
        </HStack>

        <Divider borderColor="blue.200" />

        {/* Statistics */}
        <HStack spacing={6} wrap="wrap">
          <HStack spacing={2}>
            <Hash size={14} color="#666" />
            <Text fontSize="xs" color="gray.600">
              Chunks:
            </Text>
            <Badge size="sm" colorScheme="blue" variant="solid">
              {metadataSummary.total_chunks}
            </Badge>
          </HStack>

          <HStack spacing={2}>
            <Users size={14} color="#666" />
            <Text fontSize="xs" color="gray.600">
              Documents:
            </Text>
            <Badge size="sm" colorScheme="green" variant="solid">
              {metadataSummary.unique_documents.length}
            </Badge>
          </HStack>

          <HStack spacing={2}>
            <FileText size={14} color="#666" />
            <Text fontSize="xs" color="gray.600">
              Pages:
            </Text>
            <Badge size="sm" colorScheme="purple" variant="solid">
              {metadataSummary.pages_referenced.length}
            </Badge>
          </HStack>
        </HStack>

        {/* Documents */}
        {metadataSummary.unique_documents.length > 0 && (
          <Box>
            <Text fontSize="xs" fontWeight="medium" color="gray.700" mb={2}>
              Documents:
            </Text>
            <Wrap spacing={1}>
              {metadataSummary.unique_documents.map((doc, idx) => (
                <WrapItem key={idx}>
                  <Badge size="sm" colorScheme="blue" variant="outline">
                    {doc}
                  </Badge>
                </WrapItem>
              ))}
            </Wrap>
          </Box>
        )}

        {/* Pages */}
        {metadataSummary.pages_referenced.length > 0 && (
          <Box>
            <Text fontSize="xs" fontWeight="medium" color="gray.700" mb={2}>
              Pages Referenced:
            </Text>
            <Wrap spacing={1}>
              {metadataSummary.pages_referenced.map((page, idx) => (
                <WrapItem key={idx}>
                  <Badge size="sm" colorScheme="purple" variant="outline">
                    {page}
                  </Badge>
                </WrapItem>
              ))}
            </Wrap>
          </Box>
        )}

        {/* Content Types */}
        {metadataSummary.content_types.length > 0 && (
          <Box>
            <Text fontSize="xs" fontWeight="medium" color="gray.700" mb={2}>
              Content Types:
            </Text>
            <Wrap spacing={1}>
              {metadataSummary.content_types.map((type, idx) => (
                <WrapItem key={idx}>
                  <Badge
                    size="sm"
                    colorScheme={
                      type === "table"
                        ? "orange"
                        : type === "image"
                        ? "green"
                        : "gray"
                    }
                    variant="outline"
                  >
                    {type}
                  </Badge>
                </WrapItem>
              ))}
            </Wrap>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default MetadataSummary;
