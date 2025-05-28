import React from 'react';
import { Paper, Typography, Stack, CircularProgress, Box } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  responseTime?: number;
}

interface ChatHistoryProps {
  messages: ChatMessage[];
  loading?: boolean;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, loading = false }) => (
  <Stack spacing={2} sx={{ flexGrow: 1, mb: 1, pb: 25 }}>
    {messages.length === 0 ? (
      <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.paper' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="subtitle2" fontWeight="bold">Assistant</Typography>
        </Box>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>Wie kann ich Ihnen heute helfen?</ReactMarkdown>
      </Paper>
    ) : (
      messages.map((msg, idx) => (
        <Paper
          key={idx}
          variant="outlined"
          sx={{ p: 2, bgcolor: msg.role === 'user' ? '#f5faff' : 'background.paper' }}
        >
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
            <Typography variant="subtitle2" fontWeight="bold">
              {msg.role === 'user' ? 'Du' : 'Assistant'}
            </Typography>

            {msg.role === 'assistant' && typeof msg.responseTime === 'number' && (
              <Typography variant="subtitle2" color="text.secondary" whiteSpace="nowrap">
                {msg.responseTime.toFixed(1)} s
              </Typography>
            )}
          </Box>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
        </Paper>
      ))
    )}

    {loading && (
      <Stack direction="row" alignItems="center" spacing={2} sx={{ px: 1 }}>
        <CircularProgress size={24} />
        <Typography variant="body2" color="text.secondary">
          Antwort wird geladen…
        </Typography>
      </Stack>
    )}
  </Stack>
);

export default ChatHistory; 