import { ReactElement } from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { FileProvider } from '../context/FileContext';
import { ChatProvider } from '../context/ChatContext';

export function renderWithProviders(ui: ReactElement) {
  return render(
    <BrowserRouter>
      <FileProvider>
        <ChatProvider>
          {ui}
        </ChatProvider>
      </FileProvider>
    </BrowserRouter>
  );
}