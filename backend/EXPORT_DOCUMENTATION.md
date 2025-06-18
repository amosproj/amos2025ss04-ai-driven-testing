# Export Functionality Documentation

## Overview

The AI-Driven Testing project now supports exporting LLM responses in multiple formats to enable integration with different projects and workflows.

## Supported Export Formats

### 1. **JSON** (`.json`)
- **Use Case**: API integration, data processing
- **Contains**: Structured metadata, prompt, response with performance metrics
- **Example**: 
```json
{
  "metadata": {
    "timestamp": "2025-06-18T08:24:04.957457",
    "model": {"id": "mistral:7b-instruct", "name": "MISTRAL"},
    "performance": {"loading_time": 3.2, "response_time": 7.8}
  },
  "prompt": {"text": "...", "length": 45},
  "response": {"text": "...", "length": 348}
}
```

### 2. **Markdown** (`.markdown`)
- **Use Case**: Documentation, GitHub issues, wikis
- **Contains**: Formatted text with headers, metadata, code blocks
- **Features**: Human-readable, GitHub-compatible formatting

### 3. **HTTP** (`.http`)
- **Use Case**: API testing, HTTP client testing
- **Contains**: HTTP response format with headers and JSON body
- **Features**: Ready for use with HTTP testing tools

### 4. **Plain Text** (`.txt`)
- **Use Case**: Simple text processing, logging
- **Contains**: Plain text format with clear sections
- **Features**: Maximum compatibility, easy parsing

### 5. **XML** (`.xml`)
- **Use Case**: Enterprise systems, structured data exchange
- **Contains**: Well-formed XML with CDATA sections
- **Features**: Standards-compliant, schema-ready

## Usage

### Command Line Interface

#### Export in specific format:
```bash
python main.py --export_format json
python main.py --export_format xml
python main.py --export_format markdown
```

#### Export in all formats:
```bash
python main.py --export_all
```

#### Combine with modules:
```bash
python main.py --export_format json --modules example_logger export_module
```

### API Usage

#### Direct export endpoint:
```bash
POST /export
{
  "model_id": "mistral:7b-instruct",
  "prompt": "Write unit tests...",
  "response": "Here are unit tests...",
  "loading_time": 3.2,
  "total_time": 7.8,
  "export_format": "json"
}
```

#### Get supported formats:
```bash
GET /export/formats
```

### Programmatic Usage

```python
from export_manager import ExportManager

export_manager = ExportManager()

# Export single format
exported_file = export_manager.export_output(
    response_data, prompt_data, "output", "json"
)

# Export multiple formats
exported_files = export_manager.export_multiple_formats(
    response_data, prompt_data, "output", ["json", "xml", "markdown"]
)
```

## Module Integration

The export functionality integrates seamlessly with the modular plugin system:

```python
# modules/export_module.py
class ExportModule(ModuleBase):
    def applies_after(self) -> bool:
        return True
    
    def process_response(self, response: str, prompt: str) -> str:
        # Automatically export in multiple formats
        # ...existing code...
        return response
```

## File Naming Convention

- **Single format**: `{base_name}.{format}`
- **Multiple formats**: `{base_name}.{format}` for each format
- **Default base name**: `output` (can be customized via `--output_file`)

## Performance Considerations

- **JSON**: Fastest, smallest file size
- **XML**: Larger file size due to markup
- **HTTP**: Medium size, includes headers
- **Markdown**: Human-readable, medium size
- **TXT**: Simple format, good for large responses

## Integration Examples

### CI/CD Pipeline
```yaml
- name: Generate Tests
  run: python main.py --export_format json --output_file ci_output
- name: Upload Artifacts
  uses: actions/upload-artifact@v2
  with:
    name: generated-tests
    path: ci_output.json
```

### External Tool Integration
```python
import json

# Load exported JSON
with open('output.json', 'r') as f:
    test_data = json.load(f)
    
# Extract generated test code
test_code = test_data['response']['text']

# Process with external tools
process_test_code(test_code)
```

## Error Handling

- **Unsupported format**: Raises `ValueError` with supported formats list
- **File write errors**: Graceful handling with error messages
- **Invalid data**: Validation and sanitization of export data

## Testing

Run the test suite to validate export functionality:

```bash
python test_export_manager.py
```

Run the demo to see all formats in action:

```bash
python demo_export.py
```

## Backward Compatibility

The export functionality is fully backward compatible:
- Default behavior unchanged (still exports markdown)
- Existing scripts continue to work
- New functionality is opt-in via CLI flags
