Agentic Research RAG System

An AI-powered research assistant that can search the web, analyze academic papers, and generate comprehensive research reports using LangChain agents and OpenAI.

https://ai-agent-dashboard.streamlit.app/

🚀 Features

🤖 AI Research Agents: Uses LangChain agents with tool calling

🔍 Multi-Source Research: Web search + Academic papers (arXiv)

📊 Smart Analysis: Data analysis and calculations

📄 Report Generation: Automatic research report creation

⚡ Two Modes: Standard & Advanced research modes

🌐 Web Interface: Streamlit frontend with real-time updates

🛠 Tech Stack
Backend: FastAPI, Python 3.11

AI/ML: LangChain, OpenAI GPT

Frontend: Streamlit

Search: DuckDuckGo, arXiv API

Deployment: Docker, Uvicorn

📋 Prerequisites
Python 3.11

OpenAI API key

(Optional) Serper API key for enhanced search

🚀 Quick Start
1. Clone and Setup
bash
# Navigate to project directory
cd C:\Users\wajiz.pk\Documents\agentic-research-rag

# Create and activate virtual environment (recommended)
python -m venv rag-venv
rag-venv\Scripts\activate  # Windows
2. Install Dependencies
bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies  
cd ../frontend
pip install -r requirements.txt
3. Configure API Keys
Create a .env file in the project root:

bash
# Navigate to project root
cd C:\Users\wajiz.pk\Documents\agentic-research-rag

# Create .env file with your API keys
echo OPENAI_API_KEY=your_openai_api_key_here > .env
echo SERPER_API_KEY=your_serper_key_here >> .env  # Optional
Get your API keys:

OpenAI API Key

Serper API Key (optional)

4. Start the Application
Option A: Using Docker (Recommended)
bash
# From project root
docker-compose up --build
Option B: Manual Start
Terminal 1 - Backend:

bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Terminal 2 - Frontend:

bash
cd frontend
streamlit run app.py
5. Access the Application
Frontend: http://localhost:8501

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs

🎯 Usage
Web Interface
Open http://localhost:8501

Enter your research topic

Add specific research questions

Choose research mode (Standard/Advanced)

Click "Conduct Research"

Research Modes
Standard Mode: Quick research with 3 iterations

Advanced Mode: In-depth research with 5 iterations and multi-source analysis

Multi-Step Research: Advanced research with enhanced methodology