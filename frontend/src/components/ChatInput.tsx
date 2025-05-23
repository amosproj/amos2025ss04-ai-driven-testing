import React, { useState } from 'react';
import { Box, TextField, IconButton, Tooltip } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

type ChatInputProps = {
  onSend: (message: string) => void;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input);
    setInput('');
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
  );
};

export default ChatInput;
