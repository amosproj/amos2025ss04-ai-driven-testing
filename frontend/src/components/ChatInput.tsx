import React, { useState, useRef } from 'react';
import {Box, TextField, IconButton, Tooltip, Typography} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';

type ChatInputProps = {
  onSend: (message: string) => void;
  onFileUpload?: (files: File[]) => void;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend, onFileUpload }) => {
  const [input, setInput] = useState('');
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput('');
  };

const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  if (e.target.files && e.target.files.length > 0) {
    const filesArray = Array.from(e.target.files).filter(file =>
      file.name.endsWith('.py')
    );

    if (filesArray.length > 0) {
      setUploadedFileNames(filesArray.map(file => file.name));
      onFileUpload?.(filesArray);
    }

    e.target.value = '';
  }
};



  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Box sx={{ position: 'relative' }}>
        <TextField
          label="Nachricht"
          multiline
          minRows={4}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              if (input.trim()) {
                onSend(input);
                setInput('');
                setUploadedFileNames([]);
              }
            }
          }}
          fullWidth
          sx={{
            '& .MuiInputBase-root': {
              paddingRight: '96px',
              paddingBottom: '32px',
              bgcolor: 'common.white',
            },
          }}
        />

        <Tooltip title="Datei anhängen" placement="top">
          <IconButton
            sx={{
              position: 'absolute',
              bottom: 10,
              right: 56,
              bgcolor: 'none',
              '&:hover': {
                bgcolor: 'none',
              },
            }}
            onClick={() => fileInputRef.current?.click()}
          >
            <AttachFileIcon />
          </IconButton>
        </Tooltip>

        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
          accept=".py"
          multiple
        />
    {uploadedFileNames.length > 0 && (
      <Box sx={{ mt: 1, ml: 1 }}>
        <Typography variant="caption" color="text.secondary">
          Hochgeladene Dateien:
        </Typography>
        <ul style={{ margin: 0, paddingLeft: '1rem' }}>
          {uploadedFileNames.map((name, index) => (
            <li key={index}>
              <Typography variant="caption" color="text.secondary">
                {name}
              </Typography>
            </li>
          ))}
        </ul>
      </Box>
    )}




        <Tooltip title="Senden" placement="top">
          <span>
            <IconButton
              type="submit"
              sx={{
                position: 'absolute',
                bottom: 10,
                right: 10,
                bgcolor: 'success.main',
                color: 'common.white',
                border: '1px solid',
                borderColor: 'common.white',
                '&:hover': {
                  bgcolor: 'success.dark',
                },
              }}
              disabled={!input.trim()}
            >
              <SendIcon />
            </IconButton>
          </span>
        </Tooltip>
      </Box>
    </Box>
  );
};

export default ChatInput;
