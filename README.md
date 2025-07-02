# AI-Driven Testing with Code Coverage Analysis

A comprehensive AI-driven testing platform that integrates Large Language Models (LLMs) with advanced code coverage analysis capabilities.

## Features

- **AI-Powered Code Analysis**: Utilizes multiple LLM models for intelligent code analysis and test generation
- **Code Coverage Analysis**: Real-time code coverage metrics using Python's coverage.py library
- **Interactive Web Interface**: Modern React-based frontend with real-time chat interface
- **Docker Integration**: Fully containerized deployment with Docker Compose
- **Multiple LLM Support**: Supports various models including Mistral, DeepSeek, Qwen, Gemma, Phi4, and TinyLlama

## Architecture

### Backend
- **FastAPI**: High-performance Python API framework
- **Ollama Integration**: Local LLM model management and execution
- **Code Coverage Module**: Advanced coverage analysis with AST fallback
- **Module System**: Extensible architecture for additional analysis modules

### Frontend
- **React + TypeScript**: Modern web application framework
- **Material-UI**: Professional UI component library
- **Real-time Chat**: Interactive interface for code analysis requests
- **Coverage Visualization**: Integrated display of coverage metrics

## Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB+ RAM (for LLM models)
- 10GB+ disk space

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd amos2025ss04-ai-driven-testing
   ```

2. **Start the services**
   ```bash
   docker compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Using the Code Coverage Feature

1. Open the web interface at http://localhost:3000
2. Enter Python code in the message input field
3. Check "Enable Code Coverage Analysis" checkbox
4. Click Send to analyze your code
5. View coverage metrics and analysis results

## Development

### Backend Development
```bash
cd backend
conda env create -f environment.yml
conda activate backend
python -m pytest  # Run tests
```

### Frontend Development
```bash
cd frontend
npm install
npm start  # Development server
npm run build  # Production build
```

### Testing
```bash
# Backend tests
cd backend
python -m pytest test_*.py

# Code coverage tests
python test_code_coverage_analyzer.py
python test_code_coverage_integration.py
```

## API Endpoints

- `GET /models` - List available LLM models
- `POST /prompt` - Analyze code with optional coverage analysis
- `GET /docs` - Interactive API documentation

## Configuration

### Environment Variables
- `IN_DOCKER`: Set to "true" when running in Docker
- `NODE_ENV`: Frontend environment (development/production)

### Model Configuration
Available models are configured in `backend/allowed_models.json`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please create an issue in the repository or contact the development team.
