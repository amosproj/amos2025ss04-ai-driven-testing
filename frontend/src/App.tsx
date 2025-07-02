import React, { useEffect, useState } from 'react';
import ChatInput from './components/ChatInput';
import TopBar from './components/TopBar';
import InfoBar from './components/PrivacyNotice';
import ChatHistory, { ChatMessage } from './components/ChatHistory';
import ModuleSidebar from './components/ModuleSidebar';
import { getModels, sendPrompt, shutdownModel, getModules, Model, Module } from './api';
import { Container, Box } from '@mui/material';

const App: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [modules, setModules] = useState<Module[]>([]);
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    // Hole verfügbare Modelle und Module beim Laden der Seite
    Promise.all([getModels(), getModules()])
      .then(([modelsData, modulesData]) => {
        setModels(modelsData);
        setModules(modulesData);
        if (modelsData.length > 0) {
          setSelectedModel(modelsData[0]);
        }
      })
      .catch((err) => {
        console.error('Fehler beim Laden der Daten:', err);
      });
  }, []);

  const handleSendMessage = (message: string, enableCodeCoverage: boolean = false) => {
    // füge User-Nachricht zum Verlauf hinzu
    setMessages((prev) => [...prev, { role: 'user', content: message }]);

    setLoading(true);
    console.log('Sende Nachricht:', message);
    console.log('Code Coverage enabled:', enableCodeCoverage);
    if (!selectedModel) return;
    sendPrompt(selectedModel, message, message, enableCodeCoverage)
      .then((res) => {
        console.log('Antwort erhalten:', res);
        // füge Assistant-Antwort zum Verlauf hinzu
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: res.response_markdown,
          responseTime: res.total_seconds,
        };
        
        // Add code coverage info if available
        if (res.code_coverage) {
          assistantMessage.codeCoverage = res.code_coverage;
        }
        
        setMessages((prev) => [...prev, assistantMessage]);
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
            if (!selectedModel || !data.some((m) => m.id === selectedModel.id)) {
              setSelectedModel(data[0]);
            }
          })
          .catch((err) => console.error('Fehler beim Aktualisieren der Modelle:', err));
      });
  };

  const handleShutdownModel = () => {
    if (!selectedModel) return;
    shutdownModel(selectedModel.id)
      .then(() => {
        return getModels();
      })
      .then((data) => {
        setModels(data);
        if (!selectedModel || !data.some((m) => m.id === selectedModel.id)) {
          if (data.length > 0) {
            setSelectedModel(data[0]);
          }
        }
      })
      .catch((err) => console.error('Fehler beim Herunterfahren des Modells:', err));
  };

// modules: Module[]
// selectedModules: string[] (array of selected module IDs)

const getAllDependencyIds = (module: Module, modules: Module[], visited = new Set<string>()): string[] => {
  // Prevent infinite loops if cyclic dependencies exist
  if (visited.has(module.id)) return [];
  visited.add(module.id);

  // Find dependencies by name
  const directDeps = modules.filter(m => module.dependencies.includes(m.name));

  // Collect dependencies' IDs recursively
  const allDeps = directDeps.flatMap(dep => getAllDependencyIds(dep, modules, visited));

  // Return unique list of direct dependencies + their dependencies
  return [...directDeps.map(dep => dep.id), ...allDeps];
};

const handleModuleToggle = (moduleId: string) => {
  const toggledModule = modules.find(m => m.id === moduleId);
  if (!toggledModule) return;

  const isSelected = selectedModules.includes(moduleId);

  if (isSelected) {
    // Toggle OFF: remove only the toggled module (optional: remove dependencies)
    const newSelected = selectedModules.filter(id => id !== moduleId);
    setSelectedModules(newSelected);
  } else {
    // Toggle ON: add toggled module + all dependencies recursively

    const dependencyIds = getAllDependencyIds(toggledModule, modules);

    const newSelected = Array.from(new Set([
      ...selectedModules,
      moduleId,
      ...dependencyIds,
    ]));

    setSelectedModules(newSelected);
  }
};


  return (
    <Box display="flex" flexDirection="column" height="100vh" sx={{ bgcolor: 'grey.100' }}>
      <TopBar
        models={models}
        selectedModel={selectedModel?.id || ''}
        onChangeModel={(modelId) => {
          const model = models.find((m) => m.id === modelId);
          if (model) setSelectedModel(model);
        }}
        onShutdownModel={handleShutdownModel}
        onOpenModules={() => setSidebarOpen(true)}
      />

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
              licence={models.find((m) => m.id === selectedModel?.id)?.licence ?? '—'}
              licenceLink={models.find((m) => m.id === selectedModel?.id)?.licence_link ?? 'https://choosealicense.com/licenses/'}
            />

            <ChatInput onSend={handleSendMessage} />
          </Box>
        </Container>
      </Box>

      <ModuleSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        modules={modules}
        selectedModules={selectedModules}
        onModuleToggle={handleModuleToggle}
      />
    </Box>
  );
};

export default App;
