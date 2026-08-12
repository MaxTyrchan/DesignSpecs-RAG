import {
  Box,
  Flex,
  Text,
  Avatar,
  Spinner,
  Image,
  HStack,
  Badge,
} from "@chakra-ui/react";
import { format } from "date-fns";
import { Message } from "../../types/chat";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CSSProperties } from "react";
import { BarChart3 } from "lucide-react";
import MetadataSummary from "./MetadataSummary";

interface ChatMessageProps {
  message: Message;
  isLast?: boolean;
}

const tableStyles: Record<string, CSSProperties> = {
  table: {
    borderCollapse: "collapse",
    width: "100%",
    margin: "1rem 0",
  },
  th: {
    backgroundColor: "#f8f9fa",
    border: "1px solid #dee2e6",
    padding: "0.75rem",
    textAlign: "left",
  },
  td: {
    border: "1px solid #dee2e6",
    padding: "0.75rem",
    textAlign: "left",
  },
};

const ChatMessage = ({ message, isLast }: ChatMessageProps) => {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  const isError = message.isError;

  const renderContent = () => {
    if (isUser) {
      return <Text>{message.content}</Text>;
    }

    if (message.role === "assistant") {
      return (
        <Box>
          {/* Main answer content */}
          <Box mb={4}>
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                table: ({ ...props }) => (
                  <table style={tableStyles.table} {...props} />
                ),
                th: ({ ...props }) => (
                  <th style={tableStyles.th} {...props} />
                ),
                td: ({ ...props }) => (
                  <td style={tableStyles.td} {...props} />
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </Box>

          {/* Additional content if present */}
          {message.structuredContent && (
            <>
              {/* Images */}
              {message.structuredContent.images.length > 0 && (
                <Box mt={6}>
                  <Text fontSize="sm" color="gray.600" mb={2}>
                    Related Images:
                  </Text>
                  {message.structuredContent.images.map((imageItem, index) => (
                    <Box key={`image-${index}`} mb={4}>
                      <Image
                        src={`data:image/jpeg;base64,${imageItem.content}`}
                        alt={`Image ${index + 1}`}
                        maxW="100%"
                        borderRadius="md"
                      />
                    </Box>
                  ))}
                </Box>
              )}

              {/* Text sources metadata */}
              {message.structuredContent.texts.length > 0 && (
                <Box mt={6}>
                  <Text fontSize="sm" color="gray.600" mb={3}>
                    Sources:
                  </Text>
                </Box>
              )}
            </>
          )}

          {/* Metadata Summary */}
          <MetadataSummary message={message} />

          {/* Retrieval Stats (for hybrid search) */}
          {message.retrievalStats && (
            <Box mt={4} pt={3} borderTop="1px" borderColor="gray.200">
              <HStack spacing={2} mb={2}>
                <BarChart3 size={14} />
                <Text fontSize="xs" color="gray.600" fontWeight="medium">
                  Hybrid Search Results
                </Text>
              </HStack>
              <HStack spacing={3}>
                <HStack spacing={1}>
                  <Text fontSize="xs" color="gray.500">
                    Semantic:
                  </Text>
                  <Badge size="sm" colorScheme="gray" variant="subtle">
                    {message.retrievalStats.semantic}
                  </Badge>
                </HStack>
                <HStack spacing={1}>
                  <Text fontSize="xs" color="gray.500">
                    BM25:
                  </Text>
                  <Badge size="sm" colorScheme="orange" variant="subtle">
                    {message.retrievalStats.bm25}
                  </Badge>
                </HStack>
                <HStack spacing={1}>
                  <Text fontSize="xs" color="gray.500">
                    Both:
                  </Text>
                  <Badge size="sm" colorScheme="green" variant="subtle">
                    {message.retrievalStats.both}
                  </Badge>
                </HStack>
              </HStack>
            </Box>
          )}
        </Box>
      );
    }

    return <Text>{message.content}</Text>;
  };

  return (
    <Flex
      direction="column"
      alignItems={isUser ? "flex-end" : "flex-start"}
      mb={4}
      w="100%"
    >
      <Flex alignItems="center" mb={1}>
        {!isUser && (
          <Avatar
            size="xs"
            name={isSystem ? "System" : "Assistant"}
            bg={isSystem ? "gray.500" : "brand.500"}
            color="white"
            mr={2}
          />
        )}
        <Text fontSize="xs" color="gray.500">
          {isUser ? "You" : isSystem ? "System" : "Assistant"} •{" "}
          {format(new Date(message.timestamp), "h:mm a")}
        </Text>
        {isUser && <Avatar size="xs" name="User" bg="gray.400" ml={2} />}
      </Flex>
      <Box
        maxW="80%"
        p={3}
        rounded="lg"
        bg={isUser ? "brand.500" : isError ? "error.500" : "gray.100"}
        color={isUser || isError ? "white" : "gray.800"}
        position="relative"
        boxShadow="sm"
      >
        {renderContent()}
        {isLast && message.role === "assistant" && (
          <Box
            position="absolute"
            bottom="-20px"
            left="0"
            opacity={0}
            animation="fadeOut 0.5s ease-in-out forwards"
          >
            <Text fontSize="xs" color="gray.500">
              Message sent
            </Text>
          </Box>
        )}
      </Box>
    </Flex>
  );
};

export const TypingIndicator = () => {
  return (
    <Flex align="center" my={4}>
      <Avatar size="xs" name="Assistant" bg="brand.500" color="white" mr={2} />
      <Flex
        p={3}
        rounded="lg"
        bg="gray.100"
        align="center"
        justify="center"
        boxShadow="sm"
      >
        <Spinner size="xs" mr={2} color="brand.500" />
        <Text fontSize="sm">Assistant is typing...</Text>
      </Flex>
    </Flex>
  );
};

export default ChatMessage;
