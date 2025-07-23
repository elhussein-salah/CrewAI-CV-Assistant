# CrewAI CV Assistant - Complete Documentation

## 🎯 Project Overview

The CrewAI CV Assistant is a sophisticated AI-powered system that helps users improve their CVs and find relevant job opportunities. It leverages multiple specialized AI agents working together to provide comprehensive analysis and recommendations.

### Key Features
- **Multi-Agent Architecture**: 4 specialized AI agents for different tasks
- **Local AI Processing**: Uses Ollama for privacy and control
- **Real-time Analysis**: Instant feedback and recommendations
- **Web Search Integration**: Live job search and learning resource discovery
- **Modern Web UI**: Intuitive Streamlit interface

## 🏗️ System Architecture

### Core Components

1. **AI Agents (CrewAI)**
   - CV Evaluator Agent: ATS compatibility analysis
   - CV Improver Agent: Job-specific optimization
   - Skill Recommender Agent: Gap analysis and learning resources
   - Job Finder Agent: Relevant opportunity discovery

2. **LLM Backend (Ollama)**
   - Local model execution (Llama 3, Mistral, etc.)
   - Privacy-focused processing
   - No external API dependencies

3. **Web Interface (Streamlit)**
   - Responsive design
   - Real-time progress tracking
   - Export functionality

4. **Search Tools (LangChain)**
   - DuckDuckGo integration
   - Learning resource discovery
   - Job board scraping

### Project Structure
```
crewai_cv_assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                     # Environment configuration
├── setup.py                 # Setup and validation script
├── test_components.py       # Component testing
├── start.bat               # Windows startup script
├── README.md               # Project documentation
├── __init__.py             # Package initialization
│
├── data/                   # Sample data
│   ├── sample_cv.txt       # Example CV
│   └── sample_jd.txt       # Example job description
│
├── agents/                 # AI Agent definitions
│   ├── cv_evaluator.py     # ATS evaluation agent
│   ├── cv_improver.py      # CV optimization agent
│   ├── skill_recommender.py # Skill gap analysis agent
│   └── job_finder.py       # Job search agent
│
├── prompts/                # Prompt templates
│   ├── ats_prompt.txt      # ATS evaluation prompts
│   ├── improve_prompt.txt  # CV improvement prompts
│   ├── skills_prompt.txt   # Skill analysis prompts
│   └── job_prompt.txt      # Job search prompts
│
├── tools/                  # Custom tools
│   ├── search_tool.py      # Web search integration
│   └── scraping_utils.py   # Web scraping utilities
│
├── utils/                  # Utility functions
│   ├── pdf_reader.py       # PDF processing
│   ├── text_cleaner.py     # Text preprocessing
│   └── logger.py           # Logging system
│
└── config/                 # Configuration
    ├── crew_config.py      # CrewAI configuration
    └── ollama_config.py    # Ollama LLM configuration
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running
- 8GB+ RAM recommended

### Step 1: Install Ollama
```bash
# Download from https://ollama.ai/
# After installation, pull a model:
ollama pull llama3
# or
ollama pull mistral
```

### Step 2: Clone and Setup
```bash
# Navigate to your project directory
cd d:\NTI\crewai_cv_assistant

# Install dependencies
pip install -r requirements.txt

# Run setup validation
python setup.py
```

### Step 3: Configuration
1. Verify `.env` file settings:
   ```
   OLLAMA_MODEL=llama3
   OLLAMA_BASE_URL=http://localhost:11434
   ```

2. Test components:
   ```bash
   python test_components.py
   ```

### Step 4: Launch Application
```bash
# Method 1: Direct launch
streamlit run app.py

# Method 2: Use startup script (Windows)
start.bat

# Method 3: VS Code task
# Use Ctrl+Shift+P -> "Tasks: Run Task" -> "Run CrewAI CV Assistant"
```

## 📖 User Guide

### Using the Application

1. **Start the Application**
   - Open browser to `http://localhost:8501`
   - Wait for agents to initialize

2. **Input Your Data**
   - **CV Input**: Paste text or upload PDF
   - **Job Description**: Paste target job posting
   - Use sample data buttons for testing

3. **Run Analysis**
   - Click "🚀 Analyze CV" button
   - Wait for all 4 agents to complete
   - Progress bar shows current status

4. **Review Results**
   - **ATS Evaluation**: Compatibility score and feedback
   - **CV Improvements**: Specific optimization suggestions
   - **Skill Development**: Gap analysis and learning resources
   - **Job Opportunities**: Relevant job listings

5. **Export Results**
   - Download complete analysis report
   - Markdown format for easy sharing

### Tips for Best Results

1. **CV Quality**
   - Use clear, well-formatted text
   - Include complete work experience
   - List specific skills and technologies

2. **Job Description**
   - Use complete, detailed job postings
   - Include requirements and responsibilities
   - More detail = better analysis

3. **Review and Iterate**
   - Implement suggestions gradually
   - Test different job descriptions
   - Compare ATS scores before/after changes

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Ollama Configuration
OLLAMA_MODEL=llama3              # Model to use
OLLAMA_BASE_URL=http://localhost:11434  # Ollama server URL

# Optional: Enhanced search
SERPAPI_API_KEY=                 # SerpAPI key (optional)

# Application Settings
APP_TITLE=CrewAI CV Assistant    # App title
DEBUG_MODE=False                 # Debug logging
```

### Model Configuration
Edit `config/ollama_config.py` to:
- Change default model
- Adjust temperature settings
- Modify token limits
- Add new model configurations

### Prompt Customization
Modify files in `prompts/` directory:
- `ats_prompt.txt`: ATS evaluation criteria
- `improve_prompt.txt`: CV improvement focus areas
- `skills_prompt.txt`: Skill analysis approach
- `job_prompt.txt`: Job search strategy

## 🛠️ Development

### Adding New Agents
1. Create agent file in `agents/` directory
2. Follow existing agent patterns
3. Add prompt template in `prompts/`
4. Update main app to include new agent

### Custom Tools
1. Create tool in `tools/` directory
2. Implement search/processing logic
3. Add to agent tool lists
4. Test with `test_components.py`

### Extending Search Capabilities
1. Modify `tools/search_tool.py`
2. Add new search sources
3. Implement result parsing
4. Handle rate limiting

### UI Customization
1. Edit `app.py` for layout changes
2. Modify CSS in the `st.markdown()` sections
3. Add new visualization components
4. Update tab structure

## 🧪 Testing

### Component Testing
```bash
python test_components.py
```

### Manual Testing
1. Load sample data
2. Run full analysis
3. Check all agent outputs
4. Verify export functionality

### Performance Testing
- Monitor Ollama resource usage
- Check response times
- Test with various CV lengths
- Validate with different models

## 📊 Monitoring & Logging

### Log Files
- Location: `logs/` directory
- Format: `cv_assistant_YYYYMMDD.log`
- Levels: DEBUG, INFO, WARNING, ERROR

### Key Metrics
- Agent execution times
- Search query success rates
- User input statistics
- Error frequencies

### Performance Monitoring
```python
from utils.logger import app_logger

# Log custom events
app_logger.info("Custom event message")
app_logger.log_agent_start("AgentName", "TaskDescription")
```

## 🔍 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   ```
   Error: Failed to connect to Ollama
   Solution: Ensure Ollama is running (ollama serve)
   ```

2. **Model Not Found**
   ```
   Error: Model 'llama3' not found
   Solution: Pull model (ollama pull llama3)
   ```

3. **Import Errors**
   ```
   Error: Module not found
   Solution: Install dependencies (pip install -r requirements.txt)
   ```

4. **Search Timeouts**
   ```
   Error: Search request timeout
   Solution: Check internet connection, adjust timeout settings
   ```

5. **Memory Issues**
   ```
   Error: Out of memory
   Solution: Use smaller model, increase system RAM, reduce context
   ```

### Debugging Steps
1. Run `python test_components.py`
2. Check Ollama status: `curl http://localhost:11434/api/version`
3. Verify Python packages: `pip list`
4. Check log files in `logs/` directory
5. Test with sample data first

## 🚀 Performance Optimization

### Speed Improvements
- Use smaller, faster models for development
- Cache frequently used prompts
- Implement parallel agent execution
- Optimize search query strategies

### Memory Optimization
- Limit context window sizes
- Clear agent memory between runs
- Use streaming responses
- Implement result caching

### Scalability Considerations
- Database integration for large-scale usage
- API rate limiting
- User session management
- Result persistence

## 🔒 Security & Privacy

### Data Privacy
- All processing done locally
- No data sent to external APIs (unless SerpAPI used)
- CV data stays on your machine
- Clear session data on close

### Security Best Practices
- Keep Ollama updated
- Use environment variables for secrets
- Validate all user inputs
- Sanitize file uploads

## 📈 Future Enhancements

### Planned Features
- Multi-language support
- Batch CV processing
- Integration with job boards APIs
- Advanced analytics dashboard
- Mobile-responsive design

### Potential Integrations
- LinkedIn API integration
- ATS vendor APIs
- Learning platform APIs
- Email automation
- Calendar scheduling

### Model Improvements
- Fine-tuned domain-specific models
- Multi-modal input support
- Real-time learning from feedback
- Industry-specific optimizations

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests for new features
5. Update documentation

### Code Standards
- Python PEP 8 compliance
- Type hints where applicable
- Comprehensive docstrings
- Error handling
- Logging integration

## 📞 Support

### Getting Help
1. Check this documentation
2. Review troubleshooting section
3. Run diagnostic tests
4. Check log files
5. Create issue with details

### Reporting Issues
Include:
- System information
- Error messages
- Steps to reproduce
- Log file excerpts
- Configuration details

---

## 🎉 Conclusion

The CrewAI CV Assistant provides a comprehensive, AI-powered solution for CV optimization and job searching. With its modular architecture and local processing capabilities, it offers both powerful functionality and privacy protection.

The system is designed to be extensible and customizable, allowing for future enhancements and adaptations to specific use cases. Whether you're a job seeker looking to improve your CV or a developer interested in multi-agent AI systems, this project provides a solid foundation for exploration and growth.

Happy job hunting! 🚀
