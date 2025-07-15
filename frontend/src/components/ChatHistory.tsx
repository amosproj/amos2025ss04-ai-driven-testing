import React from 'react';
import { Paper, Typography, Stack, CircularProgress, Box, Divider } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {response} from "../api";
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';


export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  responseTime?: number;
  coverage_data?: {
    overall_coverage: number;
    line_coverage: number;
    branch_coverage: number;
    covered_lines: number;
    total_lines: number;
    uncovered_lines: number[];
    details: string;
  };
  response?: response;
  attachedFileNames?: string[];
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
      messages.map((msg, idx) => {
        return (
            <Paper
                key={idx}
                variant="outlined"
                sx={{p: 2, bgcolor: msg.role === 'user' ? '#f5faff' : 'background.paper'}}
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
              {msg.attachedFileNames && msg.attachedFileNames.length > 0 && (
              <Box mt={1} sx={{ fontSize: '0.8rem', color: 'text.secondary' }}>
                <Typography variant="caption" fontWeight="bold">
                  Angehängte Dateien:
                </Typography>
                <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
                  {msg.attachedFileNames.map((fileName, index) => (
                    <li key={index}>
                      <Typography variant="caption" color="text.secondary">
                        {fileName}
                      </Typography>
                    </li>
                  ))}
                </ul>
              </Box>
            )}
          </Box>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
          
          {/* Display coverage data if available */}
          {msg.coverage_data && (
            <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1 }}>
                Code Coverage Analysis
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Overall Coverage:</strong> {msg.coverage_data.overall_coverage.toFixed(1)}%
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Line Coverage:</strong> {msg.coverage_data.line_coverage.toFixed(1)}%
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Covered Lines:</strong> {msg.coverage_data.covered_lines}
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Total Lines:</strong> {msg.coverage_data.total_lines}
                  </Typography>
                </Box>
              </Box>
              {msg.coverage_data.uncovered_lines.length > 0 && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  <strong>Uncovered Lines:</strong> {msg.coverage_data.uncovered_lines.join(', ')}
                </Typography>
              )}
              <Divider sx={{ my: 1 }} />
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                {msg.coverage_data.details}
              </Typography>
            </Box>
          )}

          {/* Display module output if available */}
          {msg.role === 'assistant' &&
            msg.response?.modules_used &&
            msg.response?.modules_used.length > 0 &&
            (
              msg.response?.output?.syntax_valid !== undefined ||
              msg.response?.output?.ccc_complexity_output !== undefined ||
              msg.response?.output?.mcc_complexity_output !== undefined ||
              msg.response?.prompt_data?.ccc_complexity_input !== undefined ||
              msg.response?.prompt_data?.mcc_complexity_input !== undefined ||
              msg.response?.prompt_data?.token_count !== undefined
            ) && (
            <Accordion sx={{ mt: 2 }} elevation={0}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="body2" fontWeight="bold">
                  Module Output
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box mt={2}>
                  <Typography variant="body2" fontWeight="bold">Analysis</Typography>

                  {msg.response?.output?.syntax_valid != null && (
                    <Typography variant="body2">
                      Syntax valid: {String(msg.response.output.syntax_valid)}
                    </Typography>
                  )}
                  {msg.response?.prompt_data?.ccc_complexity_input != null  && (
                    <Typography variant="body2">
                      CCC Complexity (Input): {msg.response.prompt_data?.ccc_complexity_input}
                    </Typography>
                  )}
                  {msg.response?.output?.mcc_complexity_output != null  && (
                    <Typography variant="body2">
                      MCC Complexity (Input): {msg.response.prompt_data?.mcc_complexity_input}
                    </Typography>
                  )}
                  {msg.response?.output?.ccc_complexity_output != null  && (
                    <Typography variant="body2">
                      CCC Complexity (Output): {msg.response.output.ccc_complexity_output}
                    </Typography>
                  )}
                  {msg.response?.output?.mcc_complexity_output != null  && (
                    <Typography variant="body2">
                      MCC Complexity (Output): {msg.response.output.mcc_complexity_output}
                    </Typography>
                  )}

                  {msg.response?.prompt_data?.token_count != null && (
                    <Typography variant="body2">
                      Token count: {msg.response.prompt_data.token_count}
                    </Typography>
                  )}
                </Box>
              </AccordionDetails>
            </Accordion>
          )}
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