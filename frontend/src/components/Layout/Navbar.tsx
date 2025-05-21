import { useState, useEffect } from 'react';
import { 
  Box, 
  Flex, 
  HStack, 
  IconButton, 
  useDisclosure, 
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  VStack,
  Text,
  Link as ChakraLink
} from '@chakra-ui/react';
import { NavLink, useLocation } from 'react-router-dom';
import { MessageCircle, FileText, BarChart2, Menu } from 'lucide-react';

const NavItem = ({ to, icon, label, isActive }: { to: string; icon: JSX.Element; label: string; isActive: boolean }) => {
  return (
    <ChakraLink
      as={NavLink}
      to={to}
      px={4}
      py={2}
      rounded="md"
      display="flex"
      alignItems="center"
      fontWeight="medium"
      color={isActive ? "brand.500" : "gray.600"}
      bg={isActive ? "brand.50" : "transparent"}
      _hover={{
        textDecoration: 'none',
        bg: 'gray.100',
      }}
      transition="all 0.2s"
    >
      <Box mr={2}>{icon}</Box>
      <Text>{label}</Text>
    </ChakraLink>
  );
};

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { to: '/', icon: <MessageCircle size={20} />, label: 'Chat' },
    { to: '/files', icon: <FileText size={20} />, label: 'Files' },
    { to: '/evaluation', icon: <BarChart2 size={20} />, label: 'Evaluation' },
  ];

  return (
    <Box
      as="nav"
      position="fixed"
      top={0}
      left={0}
      right={0}
      zIndex={10}
      transition="all 0.3s"
      bg={scrolled ? "white" : "rgba(255, 255, 255, 0.8)"}
      backdropFilter={scrolled ? "none" : "blur(10px)"}
      boxShadow={scrolled ? "sm" : "none"}
    >
      <Flex
        h="72px"
        alignItems="center"
        justifyContent="space-between"
        px={{ base: 4, md: 8 }}
      >
        <Flex alignItems="center">
          <Text
            fontSize="xl"
            fontWeight="bold"
            bgGradient="linear(to-r, brand.500, accent.500)"
            bgClip="text"
          >
            RAG Chat
          </Text>
        </Flex>

        {/* Desktop Nav */}
        <HStack spacing={4} display={{ base: 'none', md: 'flex' }}>
          {navItems.map((item) => (
            <NavItem
              key={item.to}
              to={item.to}
              icon={item.icon}
              label={item.label}
              isActive={location.pathname === item.to}
            />
          ))}
        </HStack>

        {/* Mobile Nav Button */}
        <IconButton
          display={{ base: 'flex', md: 'none' }}
          aria-label="Open menu"
          icon={<Menu />}
          onClick={onOpen}
          variant="ghost"
        />
      </Flex>

      {/* Mobile Nav Drawer */}
      <Drawer isOpen={isOpen} placement="right" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Menu</DrawerHeader>
          <DrawerBody>
            <VStack spacing={4} align="stretch">
              {navItems.map((item) => (
                <NavItem
                  key={item.to}
                  to={item.to}
                  icon={item.icon}
                  label={item.label}
                  isActive={location.pathname === item.to}
                />
              ))}
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
};

export default Navbar;