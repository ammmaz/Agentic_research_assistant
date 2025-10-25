import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(r"C:\Users\wajiz.pk\Documents\agentic-research-rag\.env")
load_dotenv(env_path)

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {'✅ FOUND' if api_key else '❌ MISSING'}")

if api_key:
    try:
        from app.agents.research_agent import ResearchAgent
        agent = ResearchAgent()
        print("✅ ResearchAgent created successfully!")
        
        # Test with a simple research topic
        result = agent.research_topic(
            "artificial intelligence", 
            ["What is AI?", "What are some applications of AI?"]
        )
        print(f"Research success: {result['success']}")
        if result['success']:
            print(f"Output length: {len(result['research_output'])} chars")
            print(f"Sources: {result['sources_used']}")
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")