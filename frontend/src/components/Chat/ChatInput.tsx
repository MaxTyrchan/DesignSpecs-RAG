import { useState, FormEvent, useRef, useEffect } from "react";
import {
  Box,
  Flex,
  Input,
  IconButton,
  useDisclosure,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from "@chakra-ui/react";
import { Send, Trash2 } from "lucide-react";
import { useChat } from "../../context/ChatContext";
import ChatSidebar from "./ChatSidebar";

const ChatInput = () => {
  const [input, setInput] = useState("");
  const { sendMessage, clearChat, isLoading } = useChat();
  const inputRef = useRef<HTMLInputElement>(null);
  const { isOpen, onClose } = useDisclosure();

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    await sendMessage(input);
    setInput("");
  };

  return (
    <Box
      position="sticky"
      bottom={0}
      bg="white"
      p={4}
      borderTopWidth="1px"
      borderTopColor="gray.200"
      width="100%"
    >
      <ChatSidebar isOpen={isOpen} onClose={onClose} />

      <form onSubmit={handleSubmit}>
        <Flex align="center" position="relative">
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            pr="4.5rem"
            bg="gray.50"
            borderColor="gray.300"
            _focus={{
              borderColor: "brand.500",
              boxShadow: "0 0 0 1px var(--chakra-colors-brand-500)",
            }}
            ref={inputRef}
            disabled={isLoading}
          />

          <Menu>
            <MenuButton
              as={IconButton}
              colorScheme="brand"
              icon={<Trash2 size={18} />}
              variant="ghost"
              size="sm"
              position="absolute"
              right="3.5rem"
              aria-label="Clear chat"
              zIndex={1}
            />
            <MenuList>
              <MenuItem onClick={clearChat} color="red.500">
                Clear entire chat
              </MenuItem>
            </MenuList>
          </Menu>

          <IconButton
            type="submit"
            aria-label="Send message"
            icon={<Send />}
            ml={2}
            colorScheme="green"
            isLoading={isLoading}
            isDisabled={!input.trim() || isLoading}
          />
        </Flex>
      </form>
    </Box>
  );
};

export default ChatInput;
