/**
 * Frontend ExportManager for AI-Driven Testing
 * 
 * Provides export functionality for browser environments with support for:
 * - JSON, HTTP, Markdown, TXT, XML formats
 * - Promise-based API for testability
 * - Mockable file system interface
 * - Browser download functionality
 */

export interface FileSystemInterface {
  writeFile(filename: string, content: string): Promise<void>;
  downloadFile(filename: string, content: string, mimeType: string): Promise<void>;
}

export interface ExportResult {
  success: boolean;
  format: string;
  filename: string;
  message: string;
  error?: string;
}

export interface ExportFormats {
  json: string;
  markdown: string;
  http: string;
  txt: string;
  xml: string;
}

/**
 * Browser-based file system implementation using download links
 */
export class BrowserFileSystem implements FileSystemInterface {
  /**
   * Write file by triggering a browser download
   */
  async writeFile(filename: string, content: string): Promise<void> {
    const mimeType = this.getMimeType(filename);
    await this.downloadFile(filename, content, mimeType);
  }

  /**
   * Download file in browser by creating a temporary download link
   */
  async downloadFile(filename: string, content: string, mimeType: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up the object URL
        setTimeout(() => {
          URL.revokeObjectURL(url);
          resolve();
        }, 100);
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Get MIME type based on file extension
   */
  private getMimeType(filename: string): string {
    const extension = filename.split('.').pop()?.toLowerCase();
    
    switch (extension) {
      case 'json':
        return 'application/json';
      case 'md':
        return 'text/markdown';
      case 'txt':
        return 'text/plain';
      case 'xml':
        return 'application/xml';
      case 'http':
        return 'text/plain';
      default:
        return 'text/plain';
    }
  }
}

/**
 * Mock file system for testing purposes
 */
export class MockFileSystem implements FileSystemInterface {
  public files: Map<string, string> = new Map();
  public downloads: Array<{ filename: string; content: string; mimeType: string }> = [];

  async writeFile(filename: string, content: string): Promise<void> {
    this.files.set(filename, content);
  }

  async downloadFile(filename: string, content: string, mimeType: string): Promise<void> {
    this.downloads.push({ filename, content, mimeType });
  }

  getFile(filename: string): string | undefined {
    return this.files.get(filename);
  }

  getDownloads(): Array<{ filename: string; content: string; mimeType: string }> {
    return [...this.downloads];
  }

  clear(): void {
    this.files.clear();
    this.downloads.splice(0, this.downloads.length);
  }
}

/**
 * Frontend ExportManager class
 */
export class ExportManager {
  private fileSystem: FileSystemInterface;
  private supportedFormats: ExportFormats = {
    json: 'JSON',
    markdown: 'Markdown',
    http: 'HTTP',
    txt: 'Plain Text',
    xml: 'XML'
  };

  constructor(fileSystem?: FileSystemInterface) {
    this.fileSystem = fileSystem || new BrowserFileSystem();
  }

  /**
   * Get list of supported export formats
   */
  getSupportedFormats(): Promise<string[]> {
    return Promise.resolve(Object.keys(this.supportedFormats));
  }

  /**
   * Get format descriptions
   */
  getFormatDescriptions(): Promise<ExportFormats> {
    return Promise.resolve({ ...this.supportedFormats });
  }

  /**
   * Export content in the specified format
   */
  async exportContent(content: string, format: string, customFilename?: string): Promise<ExportResult> {
    try {
      const normalizedFormat = format.toLowerCase();
      
      if (!this.supportedFormats.hasOwnProperty(normalizedFormat)) {
        throw new Error(`Unsupported format: ${format}. Supported formats: ${Object.keys(this.supportedFormats).join(', ')}`);
      }

      const filename = this.generateFilename(customFilename, normalizedFormat);
      const formattedContent = await this.formatContent(content, normalizedFormat);
      
      await this.fileSystem.writeFile(filename, formattedContent);

      return {
        success: true,
        format: normalizedFormat,
        filename,
        message: `Content exported successfully as ${this.supportedFormats[normalizedFormat as keyof ExportFormats]}`
      };
    } catch (error) {
      return {
        success: false,
        format: format.toLowerCase(),
        filename: '',
        message: 'Export failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export content to JSON format
   */
  async exportToJson(content: string, customFilename?: string): Promise<ExportResult> {
    return this.exportContent(content, 'json', customFilename);
  }

  /**
   * Export content to Markdown format
   */
  async exportToMarkdown(content: string, customFilename?: string): Promise<ExportResult> {
    return this.exportContent(content, 'markdown', customFilename);
  }

  /**
   * Export content to HTTP format
   */
  async exportToHttp(content: string, customFilename?: string): Promise<ExportResult> {
    return this.exportContent(content, 'http', customFilename);
  }

  /**
   * Export content to plain text format
   */
  async exportToTxt(content: string, customFilename?: string): Promise<ExportResult> {
    return this.exportContent(content, 'txt', customFilename);
  }

  /**
   * Export content to XML format
   */
  async exportToXml(content: string, customFilename?: string): Promise<ExportResult> {
    return this.exportContent(content, 'xml', customFilename);
  }

  /**
   * Format content according to the specified format
   */
  private async formatContent(content: string, format: string): Promise<string> {
    switch (format) {
      case 'json':
        return this.formatAsJson(content);
      case 'markdown':
        return this.formatAsMarkdown(content);
      case 'http':
        return this.formatAsHttp(content);
      case 'txt':
        return this.formatAsTxt(content);
      case 'xml':
        return this.formatAsXml(content);
      default:
        return content;
    }
  }

  /**
   * Format content as JSON
   */
  private formatAsJson(content: string): string {
    try {
      // Try to parse as JSON first
      const parsed = JSON.parse(content);
      return JSON.stringify(parsed, null, 2);
    } catch {
      // If not valid JSON, wrap in a JSON structure
      return JSON.stringify({
        type: 'exported_content',
        content: content,
        timestamp: new Date().toISOString()
      }, null, 2);
    }
  }

  /**
   * Format content as Markdown
   */
  private formatAsMarkdown(content: string): string {
    // If content is already markdown, return as-is
    if (content.includes('# ') || content.includes('## ') || content.includes('```')) {
      return content;
    }
    
    // Otherwise, wrap in a markdown document
    return `# Exported Content\n\n${content}\n\n---\n*Exported on ${new Date().toLocaleString()}*`;
  }

  /**
   * Format content as HTTP response
   */
  private formatAsHttp(content: string): string {
    const timestamp = new Date().toUTCString();
    return `HTTP/1.1 200 OK\nContent-Type: text/plain\nDate: ${timestamp}\nContent-Length: ${content.length}\n\n${content}`;
  }

  /**
   * Format content as plain text
   */
  private formatAsTxt(content: string): string {
    return content; // Plain text needs no formatting
  }

  /**
   * Format content as XML
   */
  private formatAsXml(content: string): string {
    const timestamp = new Date().toISOString();
    const escapedContent = content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
    
    return `<?xml version="1.0" encoding="UTF-8"?>
<export>
  <metadata>
    <timestamp>${timestamp}</timestamp>
    <type>exported_content</type>
  </metadata>
  <content><![CDATA[${content}]]></content>
</export>`;
  }

  /**
   * Generate filename with appropriate extension
   */
  private generateFilename(customFilename?: string, format?: string): string {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const baseName = customFilename || `export_${timestamp}`;
    
    const extension = this.getFileExtension(format || 'txt');
    
    // Add extension if not already present
    if (!baseName.endsWith(extension)) {
      return `${baseName}${extension}`;
    }
    
    return baseName;
  }

  /**
   * Get file extension for format
   */
  private getFileExtension(format: string): string {
    switch (format.toLowerCase()) {
      case 'json':
        return '.json';
      case 'markdown':
        return '.md';
      case 'http':
        return '.http';
      case 'txt':
        return '.txt';
      case 'xml':
        return '.xml';
      default:
        return '.txt';
    }
  }
}

export default ExportManager;
