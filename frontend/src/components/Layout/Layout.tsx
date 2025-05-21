import { ReactNode } from 'react';
import { Box } from '@chakra-ui/react';
import Navbar from './Navbar';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <Box>
      <Navbar />
      <Box as="main" pt="72px" minH="calc(100vh - 72px)">
        {children}
      </Box>
    </Box>
  );
};

export default Layout;