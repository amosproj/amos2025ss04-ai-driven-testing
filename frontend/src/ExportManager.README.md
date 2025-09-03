# Frontend ExportManager

A TypeScript-based ExportManager for browser environments that provides export functionality for AI-driven testing applications.

## Features

- ✅ **Promise-based API** for testability and async operations
- ✅ **Multiple export formats**: JSON, Markdown, HTTP, TXT, XML
- ✅ **Mockable file system** interface for testing
- ✅ **Browser download functionality** via blob URLs
- ✅ **Automatic filename generation** with timestamps
- ✅ **Content formatting** specific to each export type
- ✅ **Comprehensive error handling**
- ✅ **TypeScript support** with full type definitions

## Installation

The ExportManager is part of the frontend source code. Simply import it:

```typescript
import { ExportManager } from './ExportManager';
```

## Basic Usage

### Simple Export

```typescript
import { ExportManager } from './ExportManager';

const exportManager = new ExportManager();

// Export content as JSON
const result = await exportManager.exportToJson('{"test": "data"}', 'my-file');
console.log(result); // { success: true, format: 'json', filename: 'my-file.json', ... }

// Export content as Markdown
const mdResult = await exportManager.exportToMarkdown('# Title\n\nContent', 'document');
```

### Generic Export

```typescript
// Export with any supported format
const result = await exportManager.exportContent(
  'Content to export',
  'xml',
  'custom-filename'
);
```

### Format-Specific Methods

```typescript
// Each format has its own method
await exportManager.exportToJson(content, filename);
await exportManager.exportToMarkdown(content, filename);
await exportManager.exportToHttp(content, filename);
await exportManager.exportToTxt(content, filename);
await exportManager.exportToXml(content, filename);
```

## File System Interfaces

### BrowserFileSystem (Default)

Uses browser download functionality:

```typescript
import { ExportManager, BrowserFileSystem } from './ExportManager';

const browserFS = new BrowserFileSystem();
const exportManager = new ExportManager(browserFS);

// This will trigger a browser download
await exportManager.exportToTxt('Hello World', 'greeting');
```

### MockFileSystem (For Testing)

Stores files in memory for testing:

```typescript
import { ExportManager, MockFileSystem } from './ExportManager';

const mockFS = new MockFileSystem();
const exportManager = new ExportManager(mockFS);

await exportManager.exportToTxt('Test content', 'test-file');

// Verify the file was created
const content = mockFS.getFile('test-file.txt');
console.log(content); // 'Test content'

// Check downloads
const downloads = mockFS.getDownloads();
console.log(downloads); // [{ filename: 'test-file.txt', content: 'Test content', mimeType: 'text/plain' }]
```

### Custom File System

Implement your own file system:

```typescript
import { FileSystemInterface } from './ExportManager';

class CustomFileSystem implements FileSystemInterface {
  async writeFile(filename: string, content: string): Promise<void> {
    // Save to localStorage, IndexedDB, or send to server
    localStorage.setItem(`export_${filename}`, content);
  }
  
  async downloadFile(filename: string, content: string, mimeType: string): Promise<void> {
    // Custom download logic
    await this.writeFile(filename, content);
  }
}

const customFS = new CustomFileSystem();
const exportManager = new ExportManager(customFS);
```

## Supported Formats

| Format | Extension | Description | Content Processing |
|--------|-----------|-------------|-------------------|
| JSON | `.json` | JavaScript Object Notation | Auto-formats valid JSON, wraps plain text |
| Markdown | `.md` | Markdown document | Preserves existing markdown, wraps plain text |
| HTTP | `.http` | HTTP response format | Formats as HTTP/1.1 response with headers |
| TXT | `.txt` | Plain text | No processing, content as-is |
| XML | `.xml` | XML document | Wraps content in XML structure with metadata |

## API Reference

### ExportManager

#### Constructor
```typescript
new ExportManager(fileSystem?: FileSystemInterface)
```

#### Methods

##### `getSupportedFormats(): Promise<string[]>`
Returns list of supported format names.

##### `getFormatDescriptions(): Promise<ExportFormats>`
Returns format descriptions object.

##### `exportContent(content: string, format: string, customFilename?: string): Promise<ExportResult>`
Generic export method for any supported format.

##### Format-specific methods:
- `exportToJson(content: string, customFilename?: string): Promise<ExportResult>`
- `exportToMarkdown(content: string, customFilename?: string): Promise<ExportResult>`
- `exportToHttp(content: string, customFilename?: string): Promise<ExportResult>`
- `exportToTxt(content: string, customFilename?: string): Promise<ExportResult>`
- `exportToXml(content: string, customFilename?: string): Promise<ExportResult>`

### Types

#### `ExportResult`
```typescript
interface ExportResult {
  success: boolean;
  format: string;
  filename: string;
  message: string;
  error?: string;
}
```

#### `FileSystemInterface`
```typescript
interface FileSystemInterface {
  writeFile(filename: string, content: string): Promise<void>;
  downloadFile(filename: string, content: string, mimeType: string): Promise<void>;
}
```

## Testing

The ExportManager includes comprehensive tests:

```bash
npm test -- ExportManager.test.ts
```

### Testing with MockFileSystem

```typescript
import { ExportManager, MockFileSystem } from './ExportManager';

describe('My export tests', () => {
  let mockFS: MockFileSystem;
  let exportManager: ExportManager;
  
  beforeEach(() => {
    mockFS = new MockFileSystem();
    exportManager = new ExportManager(mockFS);
  });
  
  it('should export content', async () => {
    const result = await exportManager.exportToTxt('test content', 'test');
    
    expect(result.success).toBe(true);
    expect(mockFS.getFile('test.txt')).toBe('test content');
  });
});
```

## React Integration

### Simple Component

```tsx
import React, { useState } from 'react';
import { ExportManager } from './ExportManager';

const ExportComponent: React.FC = () => {
  const [content, setContent] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const exportManager = new ExportManager();

  const handleExport = async (format: string) => {
    setIsExporting(true);
    try {
      const result = await exportManager.exportContent(content, format);
      if (result.success) {
        alert(`Export successful: ${result.filename}`);
      } else {
        alert(`Export failed: ${result.error}`);
      }
    } catch (error) {
      alert(`Export error: ${error.message}`);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Enter content to export..."
      />
      <button
        onClick={() => handleExport('json')}
        disabled={isExporting}
      >
        Export JSON
      </button>
      <button
        onClick={() => handleExport('markdown')}
        disabled={isExporting}
      >
        Export Markdown
      </button>
    </div>
  );
};
```

## Content Formatting Examples

### JSON Export
```typescript
// Input: '{"test": "value"}'
// Output: Formatted JSON with indentation

// Input: 'plain text'
// Output: {"type": "exported_content", "content": "plain text", "timestamp": "2024-01-01T00:00:00.000Z"}
```

### Markdown Export
```typescript
// Input: '# Already markdown'
// Output: '# Already markdown' (unchanged)

// Input: 'plain text'
// Output: '# Exported Content\n\nplain text\n\n---\n*Exported on 1/1/2024, 12:00:00 AM*'
```

### HTTP Export
```typescript
// Input: 'Response body'
// Output: 'HTTP/1.1 200 OK\nContent-Type: text/plain\nDate: Mon, 01 Jan 2024 00:00:00 GMT\nContent-Length: 13\n\nResponse body'
```

### XML Export
```typescript
// Input: 'Content with <tags>'
// Output: XML document with CDATA wrapping and metadata
```

## Error Handling

All methods return `ExportResult` objects with success/failure information:

```typescript
const result = await exportManager.exportContent('content', 'invalid-format');

if (!result.success) {
  console.error('Export failed:', result.error);
  // Handle error appropriately
}
```

## Performance Considerations

- Large content (>1MB) may take longer to process
- Browser downloads are limited by browser security policies
- Consider chunking very large exports
- Use MockFileSystem for testing to avoid actual file operations

## Browser Compatibility

- Modern browsers with Blob and URL.createObjectURL support
- Chrome, Firefox, Safari, Edge (latest versions)
- IE11+ (with polyfills for Promise and modern JavaScript features)

## Examples

See `ExportManager.examples.ts` for comprehensive usage examples including:
- Basic usage patterns
- API response handling
- Testing strategies
- Custom file systems
- Batch operations
- Error handling
- Performance monitoring
