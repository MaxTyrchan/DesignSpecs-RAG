import { Box, Flex, Text, Avatar, Spinner } from '@chakra-ui/react';
import { format } from 'date-fns';
import { Message } from '../../types/chat';

interface ChatMessageProps {
  message: Message;
  isLast?: boolean;
}

const ChatMessage = ({ message, isLast }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  const isError = message.isError;

  return (
    <Flex
      direction="column"
      alignItems={isUser ? 'flex-end' : 'flex-start'}
      mb={4}
      w="100%"
    >
      <Flex 
        alignItems="center" 
        mb={1}
      >
        {!isUser && (
          <Avatar 
            size="xs" 
            name={isSystem ? 'System' : 'Assistant'} 
            bg={isSystem ? 'gray.500' : 'brand.500'} 
            color="white"
            mr={2}
          />
        )}
        <Text 
          fontSize="xs" 
          color="gray.500"
        >
          {isUser ? 'You' : isSystem ? 'System' : 'Assistant'} • {format(new Date(message.timestamp), 'h:mm a')}
        </Text>
        {isUser && (
          <Avatar 
            size="xs" 
            name="User" 
            bg="gray.400" 
            ml={2}
          />
        )}
      </Flex>
      <Box
        maxW="80%"
        p={3}
        rounded="lg"
        bg={isUser ? 'brand.500' : isError ? 'error.500' : 'gray.100'}
        color={isUser || isError ? 'white' : 'gray.800'}
        position="relative"
        boxShadow="sm"
      >
        <Text>{message.content}</Text>
        {isLast && message.role === 'assistant' && (
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