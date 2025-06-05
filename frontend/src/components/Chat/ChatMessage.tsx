import { Box, Flex, Text, Avatar, Spinner, Image } from "@chakra-ui/react";
import { format } from "date-fns";
import { Message } from "../../types/chat";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CSSProperties } from "react";

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
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </Box>

          {/* Additional tables and images if present */}
          {message.structuredContent && (
            <>
              {/* First table only */}
              {message.structuredContent.tables.length > 0 && (
                <Box mt={6}>
                  <Box mb={4} overflowX="auto">
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
                      {message.structuredContent.tables[0]}
                    </ReactMarkdown>
                  </Box>
                </Box>
              )}

              {/* Images */}
              {message.structuredContent.images.length > 0 && (
                <Box mt={6}>
                  <Text fontSize="sm" color="gray.600" mb={2}>
                    Related Images:
                  </Text>
                  {message.structuredContent.images.map((image, index) => (
                    <Box key={`image-${index}`} mb={4}>
                      <Image
                        src={`data:image/jpeg;base64,${image}`}
                        alt={`Image ${index + 1}`}
                        maxW="100%"
                        borderRadius="md"
                      />
                    </Box>
                  ))}
                </Box>
              )}
            </>
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
