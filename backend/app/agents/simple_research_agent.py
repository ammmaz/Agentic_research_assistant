import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(r"C:\Users\wajiz.pk\Documents\agentic-research-rag\.env")
load_dotenv(env_path)

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key for research: {'✅ FOUND' if api_key else '❌ MISSING'}")

if api_key:
    try:
        from app.agents.research_agent import ResearchAgent
        agent = ResearchAgent()
        print("✅ ResearchAgent created successfully!")
        
        # Test simple research
        result = agent.research_topic("test", ["what is ai?"])
        print(f"Research test: {result['success']}")
        
    except Exception as e:
        print(f"❌ ResearchAgent error: {e}")