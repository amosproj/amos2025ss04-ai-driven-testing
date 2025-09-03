/**
 * Demo component showing how to use the ExportManager
 */

import React, { useState } from 'react';
import { ExportManager, ExportResult } from './ExportManager';

const ExportDemo: React.FC = () => {
  const [content, setContent] = useState('# Sample Content\n\nThis is some sample content that can be exported in various formats.\n\n```typescript\nconst example = "Hello, World!";\nconsole.log(example);\n```');
  const [format, setFormat] = useState('json');
  const [filename, setFilename] = useState('');
  const [result, setResult] = useState<ExportResult | null>(null);
  const [isExporting, setIsExporting] = useState(false);

  const exportManager = new ExportManager();

  const handleExport = async () => {
    setIsExporting(true);
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

  const handleFormatSpecificExport = async (exportFormat: string) => {
    setIsExporting(true);
    try {
      let exportResult: ExportResult;
      
      switch (exportFormat) {
        case 'json':
          exportResult = await exportManager.exportToJson(content, filename || undefined);
          break;
        case 'markdown':
          exportResult = await exportManager.exportToMarkdown(content, filename || undefined);
          break;
        case 'http':
          exportResult = await exportManager.exportToHttp(content, filename || undefined);
          break;
        case 'txt':
          exportResult = await exportManager.exportToTxt(content, filename || undefined);
          break;
        case 'xml':
          exportResult = await exportManager.exportToXml(content, filename || undefined);
          break;
        default:
          throw new Error(`Unsupported format: ${exportFormat}`);
      }
      
      setResult(exportResult);
    } catch (error) {
      setResult({
        success: false,
        format: exportFormat,
        filename: '',
        message: 'Export failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    } finally {
      setIsExporting(false);
    }
  };

  const clearResult = () => {
    setResult(null);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Export Manager Demo</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <h3>Content to Export</h3>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={10}
          style={{ width: '100%', minHeight: '200px', fontFamily: 'monospace' }}
          placeholder="Enter content to export..."
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Export Settings</h3>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
          <label>
            Format:
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
              <option value="json">JSON</option>
              <option value="markdown">Markdown</option>
              <option value="http">HTTP</option>
              <option value="txt">Plain Text</option>
              <option value="xml">XML</option>
            </select>
          </label>
          
          <label>
            Filename (optional):
            <input
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              placeholder="custom-filename"
            />
          </label>
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Export Actions</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={handleExport}
            disabled={isExporting || !content.trim()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isExporting ? 'not-allowed' : 'pointer'
            }}
          >
            {isExporting ? 'Exporting...' : `Export as ${format.toUpperCase()}`}
          </button>
          
          <button
            onClick={() => handleFormatSpecificExport('json')}
            disabled={isExporting || !content.trim()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isExporting ? 'not-allowed' : 'pointer'
            }}
          >
            Export JSON
          </button>
          
          <button
            onClick={() => handleFormatSpecificExport('markdown')}
            disabled={isExporting || !content.trim()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#17a2b8',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isExporting ? 'not-allowed' : 'pointer'
            }}
          >
            Export Markdown
          </button>
          
          <button
            onClick={() => handleFormatSpecificExport('xml')}
            disabled={isExporting || !content.trim()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#ffc107',
              color: 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: isExporting ? 'not-allowed' : 'pointer'
            }}
          >
            Export XML
          </button>
        </div>
      </div>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Export Result</h3>
          <div
            style={{
              padding: '15px',
              border: `2px solid ${result.success ? '#28a745' : '#dc3545'}`,
              borderRadius: '4px',
              backgroundColor: result.success ? '#d4edda' : '#f8d7da'
            }}
          >
            <div>
              <strong>Status:</strong> {result.success ? 'Success' : 'Failed'}
            </div>
            <div>
              <strong>Format:</strong> {result.format}
            </div>
            {result.filename && (
              <div>
                <strong>Filename:</strong> {result.filename}
              </div>
            )}
            <div>
              <strong>Message:</strong> {result.message}
            </div>
            {result.error && (
              <div>
                <strong>Error:</strong> {result.error}
              </div>
            )}
            <button
              onClick={clearResult}
              style={{
                marginTop: '10px',
                padding: '5px 10px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Clear Result
            </button>
          </div>
        </div>
      )}

      <div style={{ marginTop: '30px' }}>
        <h3>Features</h3>
        <ul>
          <li>✅ Promise-based API for testability</li>
          <li>✅ Supports JSON, Markdown, HTTP, TXT, XML formats</li>
          <li>✅ Mockable file system interface</li>
          <li>✅ Browser download functionality</li>
          <li>✅ Automatic filename generation with timestamps</li>
          <li>✅ Content formatting specific to each export type</li>
          <li>✅ Comprehensive error handling</li>
        </ul>
      </div>
    </div>
  );
};

export default ExportDemo;
