import React, { useState } from 'react';
import { Box, TextField, IconButton, Tooltip, FormControlLabel, Checkbox } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CodeIcon from '@mui/icons-material/Code';

type ChatInputProps = {
  onSend: (message: string, enableCodeCoverage: boolean) => void;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [input, setInput] = useState('');
  const [enableCodeCoverage, setEnableCodeCoverage] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input, enableCodeCoverage);
    setInput('');
  };

  return (
    <Box>
      <Box sx={{ mb: 1 }}>
        <FormControlLabel
          control={
            <Checkbox
              checked={enableCodeCoverage}
              onChange={(e) => setEnableCodeCoverage(e.target.checked)}
              icon={<CodeIcon />}
              checkedIcon={<CodeIcon />}
            />
          }
          label="Enable Code Coverage Analysis"
        />
      </Box>
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
                onSend(input, enableCodeCoverage);
                setInput('');
              }
            }
          }}
          fullWidth
          sx={{
            '& .MuiInputBase-root': {
              paddingRight: '48px', // Platz für Icon rechts
              paddingBottom: '32px', // Platz für Icon unten
              bgcolor: 'common.white',
            },
          }}
        />
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
    </Box>
  );
};

export default ChatInput;
