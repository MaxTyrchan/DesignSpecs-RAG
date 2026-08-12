import { Box } from '@chakra-ui/react';
import { Routes, Route } from 'react-router-dom';
import { ChatProvider } from './context/ChatContext';
import { FileProvider } from './context/FileContext';
import Layout from './components/Layout/Layout';
import ChatPage from './pages/ChatPage';
import FilesPage from './pages/FilesPage';
import EvaluationPage from './pages/EvaluationPage';

function App() {
  return (
    <FileProvider>
      <ChatProvider>
        <Box minH="100vh">
          <Layout>
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/files" element={<FilesPage />} />
              <Route path="/evaluation" element={<EvaluationPage />} />
            </Routes>
          </Layout>
        </Box>
      </ChatProvider>
    </FileProvider>
  );
}

export default App;