import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
  Typography,
  Alert,
  CircularProgress,
  Chip,
  SelectChangeEvent,
} from '@mui/material';
import { ExportManager, ExportResult } from '../ExportManager';

interface ExportDialogProps {
  open: boolean;
  onClose: () => void;
  content: string;
  title?: string;
}

const ExportDialog: React.FC<ExportDialogProps> = ({ open, onClose, content, title = 'Export Content' }) => {
  const [format, setFormat] = useState<string>('json');
  const [filename, setFilename] = useState<string>('');
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [result, setResult] = useState<ExportResult | null>(null);

  const exportManager = new ExportManager();

  const formats = [
    { value: 'json', label: 'JSON', description: 'JavaScript Object Notation' },
    { value: 'markdown', label: 'Markdown', description: 'Markdown document' },
    { value: 'http', label: 'HTTP', description: 'HTTP response format' },
    { value: 'txt', label: 'Plain Text', description: 'Plain text file' },
    { value: 'xml', label: 'XML', description: 'XML document' },
  ];

  const handleFormatChange = (event: SelectChangeEvent<string>) => {
    setFormat(event.target.value);
  };

  const handleExport = async () => {
    setIsExporting(true);
    setResult(null);

    try {
      const exportResult = await exportManager.exportContent(
        content,
        format,
        filename || undefined
      );
      setResult(exportResult);
    } catch (error) {
      setResult({
        success: false,
        format,
        filename: '',
        message: 'Export failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    } finally {
      setIsExporting(false);
    }
  };

  const handleClose = () => {
    setResult(null);
    setFilename('');
    onClose();
  };

  const selectedFormat = formats.find(f => f.value === format);

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          {/* Content Preview */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Content Preview ({content.length} characters)
            </Typography>
            <TextField
              multiline
              rows={4}
              value={content}
              disabled
              fullWidth
              variant="outlined"
              sx={{ 
                '& .MuiInputBase-input': { 
                  fontSize: '0.875rem',
                  fontFamily: 'monospace' 
                }
              }}
            />
          </Box>

          {/* Export Format Selection */}
          <FormControl fullWidth>
            <InputLabel>Export Format</InputLabel>
            <Select
              value={format}
              onChange={handleFormatChange}
              label="Export Format"
            >
              {formats.map((fmt) => (
                <MenuItem key={fmt.value} value={fmt.value}>
                  <Box>
                    <Typography variant="body1">{fmt.label}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {fmt.description}
                    </Typography>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Selected Format Info */}
          {selectedFormat && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip 
                label={selectedFormat.label} 
                color="primary" 
                variant="outlined" 
                size="small"
              />
              <Typography variant="body2" color="text.secondary">
                {selectedFormat.description}
              </Typography>
            </Box>
          )}

          {/* Custom Filename */}
          <TextField
            label="Custom Filename (Optional)"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            fullWidth
            placeholder={`export-${new Date().toISOString().split('T')[0]}`}
            helperText="Leave empty to auto-generate with timestamp"
          />

          {/* Export Result */}
          {result && (
            <Alert 
              severity={result.success ? 'success' : 'error'}
              sx={{ mt: 2 }}
            >
              <Typography variant="body2">
                <strong>Status:</strong> {result.success ? 'Success' : 'Failed'}
              </Typography>
              <Typography variant="body2">
                <strong>Format:</strong> {result.format}
              </Typography>
              {result.filename && (
                <Typography variant="body2">
                  <strong>Filename:</strong> {result.filename}
                </Typography>
              )}
              <Typography variant="body2">
                <strong>Message:</strong> {result.message}
              </Typography>
              {result.error && (
                <Typography variant="body2" color="error">
                  <strong>Error:</strong> {result.error}
                </Typography>
              )}
            </Alert>
          )}

          {/* Export Features */}
          <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
            <Typography variant="subtitle2" gutterBottom>
              Export Features
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              <Chip label="Promise-based API" size="small" />
              <Chip label="Browser Download" size="small" />
              <Chip label="Auto Formatting" size="small" />
              <Chip label="Timestamp Generation" size="small" />
              <Chip label="Error Handling" size="small" />
            </Box>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="secondary">
          Cancel
        </Button>
        <Button 
          onClick={handleExport} 
          color="primary" 
          variant="contained"
          disabled={isExporting || !content.trim()}
          startIcon={isExporting ? <CircularProgress size={20} /> : null}
        >
          {isExporting ? 'Exporting...' : 'Export'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ExportDialog;
