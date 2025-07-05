import React, { useEffect, useState } from 'react';
import ChatInput from './components/ChatInput';
import TopBar from './components/TopBar';
import InfoBar from './components/PrivacyNotice';
import ChatHistory, { ChatMessage } from './components/ChatHistory';
import ModuleSidebar from './components/ModuleSidebar';
import {getModels, sendPrompt, shutdownModel, getModules, Model, Module, response} from './api';
import { Container, Box } from '@mui/material';

const App: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [modules, setModules] = useState<Module[]>([]);
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [uploadedCode, setUploadedCode] = useState<string>('');
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([]);

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

  const handleSendMessage = (message: string) => {
    setMessages((prev) => [...prev, { role: 'user', content: message, attachedFileNames: uploadedFileNames }]);

    setLoading(true);
    console.log('Sende Nachricht:', message);
    if (!selectedModel) return;
    sendPrompt(selectedModel, message, uploadedCode.trim(), selectedModules)
      .then((res) => {
        console.log('Antwort erhalten:', res);
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: res.response_markdown, responseTime: res.total_seconds , response: (res as any) as response },
        ]);
      })
      .catch((err) => {
        console.error('Fehler beim Senden des Prompts:', err);
      })
      .finally(() => {
        setLoading(false);
        setUploadedCode('');
        setUploadedFileNames([])

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
  if (visited.has(module.id)) return [];
  visited.add(module.id);

  const directDeps = modules.filter(m => module.dependencies.includes(m.name));

  const allDeps = directDeps.flatMap(dep => getAllDependencyIds(dep, modules, visited));

  return [...directDeps.map(dep => dep.id), ...allDeps];
};

const getAllDependentIds = (
  moduleId: string,
  modules: Module[],
  visited = new Set<string>()
): string[] => {
  if (visited.has(moduleId)) return [];
  visited.add(moduleId);

  // Find modules that depend on this module
  const directDependents = modules.filter(m => m.dependencies.includes(
    modules.find(mod => mod.id === moduleId)?.name || ''
  ));

  const indirectDependents = directDependents.flatMap(dep =>
    getAllDependentIds(dep.id, modules, visited)
  );

  return [...directDependents.map(m => m.id), ...indirectDependents];
};

const handleModuleToggle = (moduleId: string) => {
  const toggledModule = modules.find(m => m.id === moduleId);
  if (!toggledModule) return;

  const isSelected = selectedModules.includes(moduleId);

  if (isSelected) {
    const dependentIds = getAllDependentIds(moduleId, modules);

    const newSelected = selectedModules.filter(
      id => id !== moduleId && !dependentIds.includes(id)
    );

    setSelectedModules(newSelected);
  } else {
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
        <ChatInput
          onSend={handleSendMessage}
          onFileUpload={(files) => {
              const fileNames = Array.from(files).map(file => file.name);
              setUploadedFileNames(prev => [...prev, ...fileNames]);
              const readers = Array.from(files).map(file => {
                return new Promise<string>((resolve, reject) => {
                  const reader = new FileReader();
                  reader.onload = () => resolve(reader.result as string);
                  reader.onerror = reject;
                  reader.readAsText(file);
                });
              });

              Promise.all(readers).then(contents => {
                const combinedCode = contents.join('\n\n// --- Next File ---\n\n');
                setUploadedCode(prev => prev + '\n' + combinedCode);
              });
            }}

        />
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
