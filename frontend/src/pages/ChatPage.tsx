import { useRef, useEffect } from 'react';
import { Box, VStack, Container, Text, useDisclosure } from '@chakra-ui/react';
import ChatMessage, { TypingIndicator } from '../components/Chat/ChatMessage';
import ChatInput from '../components/Chat/ChatInput';
import { useChat } from '../context/ChatContext';

const ChatPage = () => {
  const { messages, isLoading } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { onOpen } = useDisclosure();

  // Scroll to the bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <Container maxW="container.lg" h="calc(100vh - 72px)" display="flex" flexDirection="column" p={0}>
      <Box flex="1" overflow="hidden" position="relative" display="flex" flexDirection="column">
        {/* Welcome message if no messages */}
        {messages.length === 0 && (
          <VStack 
            spacing={6} 
            justify="center" 
            align="center" 
            flex="1" 
            p={4}
            bg="gray.50"
            borderRadius="lg"
            m={4}
          >
            <Text fontSize="2xl" fontWeight="bold" textAlign="center">
              Welcome to RAG Chat
            </Text>
            <Text textAlign="center" maxW="600px" color="gray.600">
              This is a Retrieval-Augmented Generation (RAG) chat application.
              Upload PDFs and ask questions about their content. The AI will use
              the uploaded documents to provide more accurate responses.
            </Text>
            <Text fontSize="lg" fontWeight="medium">
              Start by typing a message or uploading a file!
            </Text>
          </VStack>
        )}

        {/* Messages container */}
        {messages.length > 0 && (
          <Box 
            flex="1" 
            overflowY="auto" 
            p={4} 
            sx={{
              '&::-webkit-scrollbar': {
                width: '8px',
                borderRadius: '8px',
                backgroundColor: 'rgba(0, 0, 0, 0.05)',
              },
              '&::-webkit-scrollbar-thumb': {
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderRadius: '8px',
              },
            }}
          >
            <VStack spacing={4} align="stretch">
              {messages.map((msg, index) => (
                <ChatMessage 
                  key={msg.id}
                  message={msg}
                  isLast={index === messages.length - 1}
                />
              ))}
              {isLoading && <TypingIndicator />}
              <Box ref={messagesEndRef} />
            </VStack>
          </Box>
        )}
        
        {/* Chat input */}
        <ChatInput onAttachFiles={onOpen} />
      </Box>
    </Container>
  );
};

export default ChatPage;