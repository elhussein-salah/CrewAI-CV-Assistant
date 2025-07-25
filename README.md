# CrewAI CV Assistant

A comprehensive AI-powered CV analysis and job matching system built with CrewAI, Streamlit, and Ollama.

## Features

- **CV Evaluator Agent**: Analyzes CV for ATS compatibility, scoring, and formatting issues
- **CV Improver Agent**: Provides specific improvement suggestions based on job descriptions
- **Skill Recommender Agent**: Identifies skill gaps and recommends learning resources
- **Job Finder Agent**: Searches for relevant job opportunities

## Tech Stack

- **CrewAI**: Multi-agent orchestration framework
- **Streamlit**: Web UI framework
- **Ollama**: Local LLM runtime
- **LangChain**: LLM integration and tools
- **DuckDuckGo Search**: Web search capabilities

## Setup

1. **Install Ollama**:
   ```bash
   # Download from https://ollama.ai/
   # Pull a model (e.g., deepseek-r1:1.5b, Llama 3 or Mistral)
   ollama pull llama3
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Copy `.env.example` to `.env`
   - Configure your preferred Ollama model
   - Optional: Add SerpAPI key for enhanced search

4. **Run Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your CV text in the provided textarea
2. Paste the target job description
3. Click "Analyze CV" to start the agent workflow
4. Review results in organized sections:
   - ATS Evaluation & Score
   - CV Improvement Suggestions
   - Skill Recommendations
   - Job Opportunities

## Project Structure

```
crewai_cv_assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── data/                 # Sample data files
├── agents/               # CrewAI agent definitions
├── prompts/              # Prompt templates
├── tools/                # Custom tools and utilities
├── utils/                # Helper functions
└── config/               # Configuration files
```

## Customization

- **Models**: Change Ollama model in `config/ollama_config.py`
- **Prompts**: Modify agent prompts in `prompts/` directory
- **Search Tools**: Extend search capabilities in `tools/search_tool.py`
