/**
 * Test suite for frontend ExportManager
 */

import { ExportManager, MockFileSystem, BrowserFileSystem } from './ExportManager';

describe('ExportManager', () => {
  let exportManager: ExportManager;
  let mockFileSystem: MockFileSystem;

  beforeEach(() => {
    mockFileSystem = new MockFileSystem();
    exportManager = new ExportManager(mockFileSystem);
  });

  afterEach(() => {
    mockFileSystem.clear();
  });

  describe('getSupportedFormats', () => {
    it('should return list of supported formats', async () => {
      const formats = await exportManager.getSupportedFormats();
      expect(formats).toEqual(['json', 'markdown', 'http', 'txt', 'xml']);
    });
  });

  describe('getFormatDescriptions', () => {
    it('should return format descriptions', async () => {
      const descriptions = await exportManager.getFormatDescriptions();
      expect(descriptions).toEqual({
        json: 'JSON',
        markdown: 'Markdown',
        http: 'HTTP',
        txt: 'Plain Text',
        xml: 'XML'
      });
    });
  });

  describe('exportContent', () => {
    it('should export content successfully', async () => {
      const content = 'Test content';
      const result = await exportManager.exportContent(content, 'txt', 'test-file');

      expect(result.success).toBe(true);
      expect(result.format).toBe('txt');
      expect(result.filename).toBe('test-file.txt');
      expect(result.message).toBe('Content exported successfully as Plain Text');
      expect(mockFileSystem.getFile('test-file.txt')).toBe(content);
    });

    it('should handle unsupported format', async () => {
      const content = 'Test content';
      const result = await exportManager.exportContent(content, 'unsupported');

      expect(result.success).toBe(false);
      expect(result.error).toContain('Unsupported format');
    });

    it('should generate filename with timestamp if no custom name provided', async () => {
      const content = 'Test content';
      const result = await exportManager.exportContent(content, 'txt');

      expect(result.success).toBe(true);
      expect(result.filename).toMatch(/^export_.*\.txt$/);
    });
  });

  describe('exportToJson', () => {
    it('should export valid JSON content', async () => {
      const content = '{"test": "value"}';
      const result = await exportManager.exportToJson(content, 'test');

      expect(result.success).toBe(true);
      const exportedContent = mockFileSystem.getFile('test.json');
      expect(exportedContent).toBe(JSON.stringify({"test": "value"}, null, 2));
    });

    it('should wrap non-JSON content in JSON structure', async () => {
      const content = 'Plain text content';
      const result = await exportManager.exportToJson(content, 'test');

      expect(result.success).toBe(true);
      const exportedContent = mockFileSystem.getFile('test.json');
      const parsed = JSON.parse(exportedContent!);
      expect(parsed.type).toBe('exported_content');
      expect(parsed.content).toBe(content);
      expect(parsed.timestamp).toBeDefined();
    });
  });

  describe('exportToMarkdown', () => {
    it('should return markdown content as-is if already formatted', async () => {
      const content = '# Test Title\n\nSome content';
      const result = await exportManager.exportToMarkdown(content, 'test');

      expect(result.success).toBe(true);
      expect(mockFileSystem.getFile('test.md')).toBe(content);
    });

    it('should wrap plain text in markdown structure', async () => {
      const content = 'Plain text content';
      const result = await exportManager.exportToMarkdown(content, 'test');

      expect(result.success).toBe(true);
      const exportedContent = mockFileSystem.getFile('test.md');
      expect(exportedContent).toContain('# Exported Content');
      expect(exportedContent).toContain(content);
    });
  });

  describe('exportToHttp', () => {
    it('should format content as HTTP response', async () => {
      const content = 'Response body';
      const result = await exportManager.exportToHttp(content, 'test');

      expect(result.success).toBe(true);
      const exportedContent = mockFileSystem.getFile('test.http');
      expect(exportedContent).toContain('HTTP/1.1 200 OK');
      expect(exportedContent).toContain('Content-Type: text/plain');
      expect(exportedContent).toContain(`Content-Length: ${content.length}`);
      expect(exportedContent).toContain(content);
    });
  });

  describe('exportToTxt', () => {
    it('should export plain text without modification', async () => {
      const content = 'Plain text content';
      const result = await exportManager.exportToTxt(content, 'test');

      expect(result.success).toBe(true);
      expect(mockFileSystem.getFile('test.txt')).toBe(content);
    });
  });

  describe('exportToXml', () => {
    it('should format content as XML', async () => {
      const content = 'Test content with <tags>';
      const result = await exportManager.exportToXml(content, 'test');

      expect(result.success).toBe(true);
      const exportedContent = mockFileSystem.getFile('test.xml');
      expect(exportedContent).toContain('<?xml version="1.0" encoding="UTF-8"?>');
      expect(exportedContent).toContain('<export>');
      expect(exportedContent).toContain('<metadata>');
      expect(exportedContent).toContain('<content><![CDATA[');
      expect(exportedContent).toContain(content);
    });
  });

  describe('filename generation', () => {
    it('should add extension to filename without extension', async () => {
      const result = await exportManager.exportContent('content', 'json', 'test-file');
      expect(result.filename).toBe('test-file.json');
    });

    it('should not add extension if already present', async () => {
      const result = await exportManager.exportContent('content', 'json', 'test-file.json');
      expect(result.filename).toBe('test-file.json');
    });

    it('should handle case-insensitive formats', async () => {
      const result = await exportManager.exportContent('content', 'JSON', 'test');
      expect(result.success).toBe(true);
      expect(result.format).toBe('json');
    });
  });
});

describe('MockFileSystem', () => {
  let mockFileSystem: MockFileSystem;

  beforeEach(() => {
    mockFileSystem = new MockFileSystem();
  });

  it('should store files in memory', async () => {
    await mockFileSystem.writeFile('test.txt', 'content');
    expect(mockFileSystem.getFile('test.txt')).toBe('content');
  });

  it('should track downloads', async () => {
    await mockFileSystem.downloadFile('test.txt', 'content', 'text/plain');
    const downloads = mockFileSystem.getDownloads();
    expect(downloads).toHaveLength(1);
    expect(downloads[0]).toEqual({
      filename: 'test.txt',
      content: 'content',
      mimeType: 'text/plain'
    });
  });

  it('should clear all data', async () => {
    await mockFileSystem.writeFile('test.txt', 'content');
    await mockFileSystem.downloadFile('test.txt', 'content', 'text/plain');
    
    mockFileSystem.clear();
    
    expect(mockFileSystem.getFile('test.txt')).toBeUndefined();
    expect(mockFileSystem.getDownloads()).toHaveLength(0);
  });
});

describe('BrowserFileSystem', () => {
  let browserFileSystem: BrowserFileSystem;

  beforeEach(() => {
    browserFileSystem = new BrowserFileSystem();
    
    // Mock DOM elements and URL methods
    global.URL.createObjectURL = jest.fn(() => 'blob:test-url');
    global.URL.revokeObjectURL = jest.fn();
    
    // Mock document.createElement and related methods
    const mockLink = {
      href: '',
      download: '',
      style: { display: '' },
      click: jest.fn()
    } as unknown as HTMLAnchorElement;
    
    jest.spyOn(document, 'createElement').mockReturnValue(mockLink);
    jest.spyOn(document.body, 'appendChild').mockImplementation();
    jest.spyOn(document.body, 'removeChild').mockImplementation();
    
    // Mock Blob constructor
    (global as any).Blob = jest.fn().mockImplementation((content: string[], options: BlobPropertyBag) => ({
      size: content[0].length,
      type: options.type
    }));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should create download link for writeFile', async () => {
    await browserFileSystem.writeFile('test.txt', 'content');
    
    expect(global.Blob).toHaveBeenCalledWith(['content'], { type: 'text/plain' });
    expect(global.URL.createObjectURL).toHaveBeenCalled();
    expect(document.createElement).toHaveBeenCalledWith('a');
  });

  it('should handle downloadFile with correct MIME type', async () => {
    await browserFileSystem.downloadFile('test.json', '{"test": true}', 'application/json');
    
    expect(global.Blob).toHaveBeenCalledWith(['{"test": true}'], { type: 'application/json' });
  });
});
