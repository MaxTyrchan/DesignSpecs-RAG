import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// Define custom theme
const theme = extendTheme({
  colors: {
    brand: {
      50: '#e6f1fe',
      100: '#c6dcfd',
      200: '#a3c6fa',
      300: '#80aff7',
      400: '#5c98f4',
      500: '#3b82f6', // primary blue
      600: '#2f67c4',
      700: '#234c93',
      800: '#183262',
      900: '#0c1931',
    },
    secondary: {
      50: '#e6f9f8',
      100: '#c5f1ee',
      200: '#a1e8e3',
      300: '#7dded7',
      400: '#59d5cc',
      500: '#14b8a6', // secondary teal
      600: '#109386',
      700: '#0c6e65',
      800: '#084a44',
      900: '#042522',
    },
    accent: {
      50: '#f5f3ff',
      100: '#ede9fe',
      200: '#ddd6fe',
      300: '#c4b5fd',
      400: '#a78bfa',
      500: '#8b5cf6', // accent purple
      600: '#7c3aed',
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
    },
    success: {
      500: '#10b981',
    },
    warning: {
      500: '#f59e0b',
    },
    error: {
      500: '#ef4444',
    },
  },
  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'medium',
        borderRadius: 'md',
      },
    },
  },
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <ChakraProvider theme={theme}>
        <App />
      </ChakraProvider>
    </BrowserRouter>
  </StrictMode>
);