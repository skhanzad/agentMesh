# Citation
```bibtex
@misc{khanzadeh2025agentmeshcooperativemultiagentgenerative,
      title={AgentMesh: A Cooperative Multi-Agent Generative AI Framework for Software Development Automation}, 
      author={Sourena Khanzadeh},
      year={2025},
      eprint={2507.19902},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2507.19902}, 
}
```
# AgentMesh - Cooperative Multi-Agent Generative AI System

A Python application where multiple LLM-powered agents collaborate on software development tasks. Each agent has a distinct role in the development pipeline.

## 🤖 Agent Architecture

- **Planner Agent**: Interprets user tasks and breaks them into subtasks
- **Coder Agent**: Writes Python code based on each subtask
- **Debugger Agent**: Reviews and suggests fixes to generated code
- **Reviewer Agent**: Checks the final version for correctness and improvements

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd agentMesh

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

### 2. Configure API Key

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

#### Interactive Mode
```bash
python main.py --interactive
```

#### Single Task Mode
```bash
python main.py --task "Create a basic calculator app" --output results.json
```

#### Help
```bash
python main.py --help
```

## 📁 Project Structure

```
agentMesh/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── planner_agent.py       # Task breakdown agent
│   ├── coder_agent.py         # Code generation agent
│   ├── debugger_agent.py      # Code review agent
│   └── reviewer_agent.py      # Final validation agent
├── coordinator.py             # Agent workflow coordinator
├── main.py                   # CLI interface
├── requirements.txt           # Python dependencies
├── env_example.txt           # Environment variables template
└── README.md                 # This file
```

## 🔧 Features

- **Modular Architecture**: Each agent is a separate class that can be easily swapped or extended
- **Rich CLI Interface**: Beautiful terminal output with colored panels and progress indicators
- **Comprehensive Logging**: All agent interactions are logged to `agent_mesh.log`
- **Error Handling**: Robust error handling and recovery mechanisms
- **Conversation History**: Complete tracking of all agent interactions
- **JSON Output**: Results can be saved in structured JSON format

## 💡 Usage Examples

### Example 1: Calculator App
```bash
python main.py --task "Create a basic calculator app with GUI"
```

### Example 2: Web Scraper
```bash
python main.py --task "Build a web scraper for news articles"
```

### Example 3: File Manager
```bash
python main.py --task "Develop a simple file manager with basic operations"
```

## 🔄 Development Pipeline

1. **Planning Phase**: User task → Planner Agent breaks down into subtasks
2. **Coding Phase**: Each subtask → Coder Agent generates Python code
3. **Debugging Phase**: Generated code → Debugger Agent reviews and suggests fixes
4. **Review Phase**: All outputs → Reviewer Agent provides final assessment

## 🛠️ Customization

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the required abstract methods
3. Add the agent to the coordinator workflow

Example:
```python
class CustomAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "Your custom system prompt"
    
    def process_message(self, message: Message) -> Message:
        # Your custom processing logic
        pass
```

### Modifying Agent Behavior

Each agent can be customized by:
- Changing the system prompt in `get_system_prompt()`
- Adjusting the LLM model or temperature
- Adding custom processing logic in `process_message()`

## 📊 Output Format

The system generates structured output including:
- Original task description
- Planning breakdown (JSON format)
- Generated Python code for each subtask
- Debugger feedback and suggestions
- Final review and assessment
- Complete conversation history

## 🔍 Logging

All agent interactions are logged to `agent_mesh.log` with timestamps and detailed information about:
- Message sender and recipient
- Message content (truncated for readability)
- Processing time
- Error conditions

## 🚨 Error Handling

The system includes comprehensive error handling for:
- Missing API keys
- Network connectivity issues
- Invalid JSON responses from agents
- LLM API errors
- File I/O operations

## 📝 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for LLM API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with LangChain for LLM integration
- Rich library for beautiful CLI output
- OpenAI GPT models for agent intelligence 
