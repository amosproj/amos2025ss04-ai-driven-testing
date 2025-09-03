/**
 * Usage examples for the frontend ExportManager
 */

import { ExportManager, MockFileSystem } from './ExportManager';

// Example 1: Basic usage with browser downloads
export const basicUsageExample = async () => {
  const exportManager = new ExportManager();
  
  const content = `
# AI-Driven Test Results

## Test Summary
- Total tests: 42
- Passed: 38
- Failed: 4
- Coverage: 89.5%

## Generated Code
\`\`\`typescript
function calculateSum(a: number, b: number): number {
  return a + b;
}

describe('calculateSum', () => {
  it('should add two numbers correctly', () => {
    expect(calculateSum(2, 3)).toBe(5);
  });
});
\`\`\`
`;

  try {
    // Export as JSON
    const jsonResult = await exportManager.exportToJson(content, 'test-results');
    console.log('JSON export:', jsonResult);

    // Export as Markdown
    const markdownResult = await exportManager.exportToMarkdown(content, 'test-results');
    console.log('Markdown export:', markdownResult);

    // Export as XML
    const xmlResult = await exportManager.exportToXml(content, 'test-results');
    console.log('XML export:', xmlResult);

  } catch (error) {
    console.error('Export failed:', error);
  }
};

// Example 2: Using with API responses
export const apiResponseExample = async () => {
  const exportManager = new ExportManager();
  
  // Simulate API response
  const apiResponse = {
    model: 'gpt-4',
    response: 'Here are the generated unit tests...',
    timestamp: new Date().toISOString(),
    metadata: {
      tokensUsed: 150,
      executionTime: 2.5
    }
  };

  // Export API response as JSON
  const result = await exportManager.exportToJson(
    JSON.stringify(apiResponse),
    'api-response'
  );
  
  console.log('API response exported:', result);
};

// Example 3: Testing with MockFileSystem
export const testingExample = async () => {
  const mockFileSystem = new MockFileSystem();
  const exportManager = new ExportManager(mockFileSystem);
  
  const testContent = 'Test content for unit testing';
  
  // Export content
  await exportManager.exportToTxt(testContent, 'test-file');
  
  // Verify the file was created
  const exportedContent = mockFileSystem.getFile('test-file.txt');
  console.log('Content stored in mock filesystem:', exportedContent);
  
  // Check downloads
  const downloads = mockFileSystem.getDownloads();
  console.log('Downloads tracked:', downloads);
  
  // Clear mock filesystem
  mockFileSystem.clear();
};

// Example 4: Custom file system implementation
export class CustomFileSystem {
  private storage: Map<string, string> = new Map();
  
  async writeFile(filename: string, content: string): Promise<void> {
    // Custom logic - e.g., save to localStorage
    localStorage.setItem(`exported_${filename}`, content);
    this.storage.set(filename, content);
    console.log(`Saved ${filename} to localStorage`);
  }
  
  async downloadFile(filename: string, content: string, mimeType: string): Promise<void> {
    // Custom download logic
    console.log(`Custom download: ${filename} (${mimeType})`);
    await this.writeFile(filename, content);
  }
  
  getFile(filename: string): string | null {
    return localStorage.getItem(`exported_${filename}`);
  }
}

export const customFileSystemExample = async () => {
  const customFS = new CustomFileSystem();
  const exportManager = new ExportManager(customFS);
  
  const content = 'Content saved to localStorage';
  await exportManager.exportToTxt(content, 'custom-storage');
  
  // Retrieve from custom storage
  const retrieved = customFS.getFile('custom-storage.txt');
  console.log('Retrieved from custom storage:', retrieved);
};

// Example 5: Batch export functionality
export const batchExportExample = async () => {
  const exportManager = new ExportManager();
  
  const contents = [
    { name: 'test-1', content: 'First test content' },
    { name: 'test-2', content: 'Second test content' },
    { name: 'test-3', content: 'Third test content' }
  ];
  
  const formats = ['json', 'txt', 'xml'];
  
  // Export each content in all formats
  const results = await Promise.all(
    contents.flatMap(({ name, content }) =>
      formats.map(format =>
        exportManager.exportContent(content, format, `${name}-${format}`)
      )
    )
  );
  
  console.log('Batch export results:', results);
  
  // Count successful exports
  const successCount = results.filter(r => r.success).length;
  console.log(`Successfully exported ${successCount} out of ${results.length} files`);
};

// Example 6: Integration with React component
export const reactIntegrationExample = `
import React, { useState } from 'react';
import { ExportManager } from './ExportManager';

const MyComponent: React.FC = () => {
  const [content, setContent] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const exportManager = new ExportManager();

  const handleExport = async (format: string) => {
    setIsExporting(true);
    try {
      const result = await exportManager.exportContent(content, format);
      if (result.success) {
        alert(\`Export successful: \${result.filename}\`);
      } else {
        alert(\`Export failed: \${result.error}\`);
      }
    } catch (error) {
      alert(\`Export error: \${error.message}\`);
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
`;

// Example 7: Error handling patterns
export const errorHandlingExample = async () => {
  const exportManager = new ExportManager();
  
  try {
    // This will fail due to unsupported format
    const result = await exportManager.exportContent('test', 'unsupported-format');
    
    if (!result.success) {
      console.error('Export failed:', result.error);
      
      // Handle specific error cases
      if (result.error?.includes('Unsupported format')) {
        console.log('Available formats:', await exportManager.getSupportedFormats());
      }
    }
  } catch (error) {
    console.error('Unexpected error:', error);
  }
};

// Example 8: Performance monitoring
export const performanceMonitoringExample = async () => {
  const exportManager = new ExportManager();
  const largeContent = 'x'.repeat(1000000); // 1MB of content
  
  const startTime = performance.now();
  const result = await exportManager.exportToJson(largeContent, 'large-file');
  const endTime = performance.now();
  
  console.log(`Export took ${endTime - startTime} milliseconds`);
  console.log('Export result:', result);
};

// Run examples (uncomment to test)
/*
(async () => {
  console.log('Running ExportManager examples...');
  
  await basicUsageExample();
  await apiResponseExample();
  await testingExample();
  await customFileSystemExample();
  await batchExportExample();
  await errorHandlingExample();
  await performanceMonitoringExample();
  
  console.log('All examples completed!');
})();
*/
