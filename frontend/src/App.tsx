import React, { useEffect, useState } from 'react';
import ChatInput from './components/ChatInput';
import TopBar from './components/TopBar';
import InfoBar from './components/PrivacyNotice';
import ChatHistory, { ChatMessage } from './components/ChatHistory';
import { getModels, sendPrompt, shutdownModel, Model } from './api';
import { Container, Box } from '@mui/material';

const App: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // Hole verfügbare Modelle beim Laden der Seite
    getModels()
      .then((data) => {
        setModels(data);
        if (data.length > 0) {
          setSelectedModel(data[0].id);
        }
      })
      .catch((err) => {
        console.error('Fehler beim Laden der Modelle:', err);
      });
  }, []);

  const handleSendMessage = (message: string) => {
    // füge User-Nachricht zum Verlauf hinzu
    setMessages((prev) => [...prev, { role: 'user', content: message }]);

    setLoading(true);
    console.log('Sende Nachricht:', message);
    sendPrompt(selectedModel, message)
      .then((res) => {
        console.log('Antwort erhalten:', res);
        // füge Assistant-Antwort zum Verlauf hinzu
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: res.response_markdown, responseTime: res.total_seconds },
        ]);
      })
      .catch((err) => {
        console.error('Fehler beim Senden des Prompts:', err);
      })
      .finally(() => {
        setLoading(false);

        // Modelle nach jeder Antwort aktualisieren
        getModels()
          .then((data) => {
            setModels(data);
            // falls aktuelles Modell nicht mehr existiert, erstes wählen
            if (!data.some((m) => m.id === selectedModel) && data.length > 0) {
              setSelectedModel(data[0].id);
            }
          })
          .catch((err) => console.error('Fehler beim Aktualisieren der Modelle:', err));
      });
  };

  const handleShutdownModel = () => {
    shutdownModel(selectedModel)
      .then(() => {
        // Nach dem Herunterfahren: Modelle neu laden
        return getModels();
      })
      .then((data) => {
        setModels(data);
        // falls aktuelles Modell nicht mehr existiert, erstes wählen
        if (!data.some((m) => m.id === selectedModel) && data.length > 0) {
          setSelectedModel(data[0].id);
        }
      })
      .catch((err) => console.error('Fehler beim Herunterfahren des Modells:', err));
  };

  return (
    <Box display="flex" flexDirection="column" height="100vh" sx={{ bgcolor: 'grey.100' }}>
      <TopBar
        models={models}
        selectedModel={selectedModel}
        onChangeModel={setSelectedModel}
        onShutdownModel={handleShutdownModel}
      />

      {/* Scrollbarer Bereich (alles außer TopBar) */}
      <Box
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          overflowY: 'auto',
        }}
      >
        <Container
          maxWidth="md"
          sx={{
            flexGrow: 1,
            py: 2,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <ChatHistory messages={messages} loading={loading} />

          <Box
            sx={{
              position: 'sticky',
              bottom: 22,
              bgcolor: 'grey.100',
              pt: 1,
              border: '1px solid #ccc',
              borderRadius: '8px',
              boxShadow: '1px 2px 10px rgba(57, 0, 234, 12.1)',
              p: 1,
            }}
          >
            <InfoBar
              licence={models.find((m) => m.id === selectedModel)?.licence ?? '—'}
              licenceLink={models.find((m) => m.id === selectedModel)?.licence_link ?? 'https://choosealicense.com/licenses/'}
            />

            <ChatInput onSend={handleSendMessage} />
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default App;
